# Informe final - Laboratorio 5: Seguridad de Aplicaciones

**Integrantes:** Juan Sebastián Murcia y Sara Arteaga.  
**Asignatura:** Fundamentos de Seguridad de la Información, FDSI_4L-26022.  
**Fecha:** 18 de noviembre de 2026, hora de Colombia.  
**Proyecto:** Falcon Lab, registro de alertas ficticias de seguridad.  
**Repositorio:** https://github.com/JuanMurciay/Lab-03-FDSI  
**Rama:** [security/lab-fsi](https://github.com/JuanMurciay/Lab-03-FDSI/tree/security/lab-fsi).  
**Línea base:** [6a1f883](https://github.com/JuanMurciay/Lab-03-FDSI/commit/6a1f8839c234bbe5f4258e9868808ac3996cda35).  
**Código corregido y analizado:** [19de2cd](https://github.com/JuanMurciay/Lab-03-FDSI/commit/19de2cd598f566b54620130512de2d90f900f25a).  
**Pull Request de remediación:** [PR #1](https://github.com/JuanMurciay/Lab-03-FDSI/pull/1).

## 1. Resumen

Revisamos el proyecto que ya veníamos usando en los laboratorios. Integramos las herramientas del profesor y comprobamos un problema de acceso: la API aceptaba crear alertas sin pedir ninguna credencial. La corregimos con un token local para las operaciones de escritura. También completamos la política CSP del frontend después de revisar una alerta de ZAP.

La evidencia muestra que una solicitud sin token pasó de recibir 201 a recibir 401. Con el token de prueba, la aplicación sigue guardando la alerta y responde 201. En ZAP dejó de aparecer la alerta 10055 relacionada con la directiva form-action. No concluimos que la aplicación sea completamente segura: todavía hay resultados que necesitan revisión, en especial el almacenamiento de contraseñas locales que señaló CodeQL.

## 2. Alcance y arquitectura

La aplicación usa HTML, CSS y JavaScript en la interfaz, una API de Python con Flask y Waitress, y PostgreSQL para guardar alertas y acciones. Docker Compose conecta el navegador con Nginx, la API y la base de datos. Para el inicio local de Windows existe además web.py, que sirve la interfaz y actúa como intermediario hacia la API.

Flujo principal: navegador -> Nginx o web.py -> API Flask -> PostgreSQL. Las rutas principales son GET /api/health, GET y POST /api/alertas, GET /api/alertas/id, POST /api/alertas/id/acciones y GET /api/acciones.

Antes del cambio no había autenticación en estas operaciones. Después del cambio, las escrituras requieren el encabezado X-Lab-Token. Las consultas siguen siendo públicas porque el contenido es ficticio; esta decisión no sería apropiada para información real. El token compartido identifica a quien conoce el valor, pero no distingue personas ni roles.

El alcance autorizado fue el repositorio propio indicado en la solicitud y dos despliegues temporales de ese mismo código en runners de GitHub Actions. La API y la interfaz se publicaron solo en 127.0.0.1. Se usaron registros inventados y valores efímeros generados durante el job. No se escanearon dominios del inventario de laboratorios anteriores, producción ni servicios de terceros.

Los activos que nos interesa cuidar son la integridad de las alertas, el historial de acciones y las credenciales de la base local. El principal riesgo validado fue que otra persona con acceso al servicio pudiera registrar información sin estar autorizada. Los volúmenes de PostgreSQL creados por esta prueba se eliminaron al terminar; no se utilizaron volúmenes de una instalación existente.

## 3. Herramientas y resultados comprobados

| Control | Ejecución y resultado | Evidencia |
|---|---|---|
| Semgrep, SAST | 2 alertas en la línea base y 2 en la versión final. Se analizaron los resultados; no equivalen automáticamente a vulnerabilidades explotables. | [Workflow](https://github.com/JuanMurciay/Lab-03-FDSI/actions/runs/44429539772), semgrep-antes.json y semgrep-despues.json |
| CodeQL, SAST | Análisis de Python y JavaScript completados. Una alerta abierta de almacenamiento de información sensible en iniciar.py. | [Workflow](https://github.com/JuanMurciay/Lab-03-FDSI/actions/runs/44429539812), [alerta #1](https://github.com/JuanMurciay/Lab-03-FDSI/security/code-scanning/1) |
| Gitleaks | Análisis del historial, sin secretos detectados en la ejecución conservada. No se publicaron valores de credenciales. | [Workflow](https://github.com/JuanMurciay/Lab-03-FDSI/actions/runs/44429539772), results.sarif |
| Dependabot y Dependency Review, SCA | Alertas nativas activadas, sin alertas abiertas al consultar. Dependency Review completó el PR. Configuración semanal de pip y Actions preparada en la rama. | [Workflow](https://github.com/JuanMurciay/Lab-03-FDSI/actions/runs/44429539772), controles-github.json y sca.json |
| OWASP ZAP Baseline, DAST | Cuatro reportes: web y API, antes y después. La alerta CSP 10055 del frontend desapareció. Permanecen otras alertas. | [Workflow](https://github.com/JuanMurciay/Lab-03-FDSI/actions/runs/44429528875), reportes zap-*.html y zap-*.json |
| Validación controlada | POST de una alerta ficticia sin token: 201 antes, 401 después. Token incorrecto: 401. Token de prueba correcto: 201. | http-antes.json y http-despues.json |
| Regresión | Diez pruebas locales aprobadas y job de regresión completado en Actions. | regresion-local.txt y [workflow](https://github.com/JuanMurciay/Lab-03-FDSI/actions/runs/44429539772) |

Los archivos de evidencia están en [evidence/lab5](../evidence/lab5/). El commit de documentación puede ser posterior al commit del código analizado; los enlaces anteriores identifican el código y las ejecuciones utilizados para la comparación.

CodeQL se configuró con un workflow explícito, como permite la presentación del profesor. El estado de Default setup se consultó y no estaba configurado; no se activaron las dos modalidades a la vez. Se activaron secret scanning y push protection nativos. Dependabot alerts ya está habilitado. Las actualizaciones semanales de dependencias comenzarán cuando el archivo dependabot.yml esté en la rama principal; no afirmamos que ya exista un PR automático de actualización.

## 4. Método y decisiones

Primero identificamos el commit original. Luego ejecutamos SAST y detección de secretos, revisamos dependencias, levantamos servicios temporales y aplicamos ZAP Baseline. Complementamos el análisis con una petición POST sencilla, corregimos el código y repetimos las pruebas. No se utilizaron ataques activos ni pruebas de fuerza bruta.

Como no se proporcionó un staging HTTPS propio, usamos la alternativa local permitida por la guía: localhost con Docker. Los contenedores se ejecutaron en el runner de Actions. Conservamos el workflow de staging del kit como opción, pero no configuramos STAGING_URL ni lo presentamos como ejecutado.

Semgrep se ejecuta sin --error para poder revisar las alertas durante la práctica; conserva los resultados y sigue fallando si hay errores de ejecución. ZAP usa -I para no bloquear por advertencias, pero guarda los reportes. Por eso un resultado verde confirma que terminó el proceso, no que todo esté corregido. Las acciones quedaron fijadas por SHA y se añadió una espera de siete días a las actualizaciones, a partir de advertencias que aparecieron durante el análisis inicial.

## 5. Matriz de hallazgos y resultados

| ID | Origen | Resultado | Riesgo estimado | Decisión |
|---|---|---|---|---|
| F-01 | Validación HTTP y revisión de API | Escritura sin autenticación | Medio en el entorno local | Corregido con token y probado antes/después |
| F-02 | ZAP, regla 10055 | CSP del frontend sin form-action | Medio, según ZAP | Corregido; la alerta no aparece en el reescaneo |
| F-03 | CodeQL, py/clear-text-storage-sensitive-data | Contraseña generada para PostgreSQL guardada en archivo local | Alto en la herramienta; medio en este escenario local | Hallazgo real abierto; .gitignore evita publicarlo pero no cifra el archivo |
| F-04 | Semgrep, subprocess | Posible inyección al iniciar procesos | No confirmada; falso positivo para la inyección de shell indicada | Se revisó Popen con lista de argumentos, sin shell y con ejecutables definidos por el programa |
| F-05 | Semgrep, request-host-used | Nginx reenvía Host recibido | Bajo en el alcance probado; requiere revisión al desplegar | El archivo marcado no es el utilizado por Compose y no se confirmó explotación |
| R-06 | SCA y revisión de Flask | Flask 3.1.3 ya corrige GHSA-68rp-wp8r-4726 | No aplica ese aviso a la versión usada | No actualizar a ciegas ni inventar una dependencia vulnerable |

El detalle está en [REPORTE_HALLAZGOS.md](REPORTE_HALLAZGOS.md). Semgrep tuvo inicialmente 19 alertas en la primera integración porque también revisó los YAML nuevos. Después de fijar las acciones y añadir cooldown, la versión final tuvo 2. No se borraron reglas del código. Después de publicar las evidencias, Semgrep también marcó 51 enlaces HTTP de los HTML generados por ZAP; se excluyó únicamente evidence/lab5 mediante .semgrepignore para no analizar reportes como si fueran código de la aplicación. Los reportes siguen publicados y Gitleaks continúa revisando el historial completo.

## 6. Validación manual y remediación

Hipótesis: si una persona envía un POST válido a /api/alertas sin autenticación, la API guarda el registro. Se envió solo un registro ficticio por etapa, con el título Validacion Lab 5 y el equipo EQUIPO-FICTICIO. La respuesta inicial fue 201 y devolvió id 1. Después del cambio, la misma solicitud sin token respondió 401 y no creó la alerta. Una solicitud con un token incorrecto también respondió 401; con el token temporal correcto devolvió 201.

La solución consulta LAB_API_TOKEN en el entorno y usa secrets.compare_digest para compararlo con X-Lab-Token. Si no existe configuración, rechaza la escritura con 503. La interfaz permite introducir el token en un campo de contraseña y lo envía como encabezado. No se guarda en localStorage ni se incluye en el código. El proxy web.py también lo reenvía. El control sigue funcionando aunque se desactiven los encabezados opcionales con HARDENING.

Para F-02 agregamos form-action 'self' en Nginx y web.py. Esa directiva limita a dónde puede enviar formularios el navegador. La API también recibió una CSP restrictiva, aunque ZAP no había marcado ausencia de CSP en las respuestas JSON. No presentamos esa mejora adicional como una vulnerabilidad XSS demostrada.

Las diez pruebas cubren token ausente, incorrecto y válido, caracteres no ASCII, acciones sobre alertas, falta de configuración, HARDENING desactivado, lectura pública, encabezados en errores, CSP del frontend y reenvío del token por el proxy. Las pruebas unitarias usan una base simulada; la comparación HTTP de Actions sí se hizo con PostgreSQL real.

## 7. Revisión de dependencias

requirements.txt fija Flask 3.1.3, Waitress 3.0.2 y psycopg[binary] 3.3.5. Revisamos Flask frente al aviso oficial GHSA-68rp-wp8r-4726: afecta versiones anteriores a 3.1.3 y se corrige en 3.1.3. Además, la API no utiliza sesiones de Flask y ya envía Cache-Control: no-store. Para este aviso concreto, ni la versión ni el flujo revisado justifican reportar una vulnerabilidad presente.

No encontramos una dependencia vulnerable confirmada en las alertas consultadas. Por eso no cambiamos una versión solo para simular una corrección SCA. Dependency Review analiza cambios de dependencias del PR; no sustituye una auditoría completa de todas las versiones transitivas. No hay un lock completo de Python y las imágenes de contenedores no fueron auditadas por un escáner adicional. La configuración de Dependabot incluye pip y GitHub Actions, con revisión semanal.

Fuente de la comparación: [aviso oficial de Flask](https://github.com/pallets/flask/security/advisories/GHSA-68rp-wp8r-4726).

## 8. Resultados de DAST y riesgo residual

En el frontend se registraron 7 tipos de alerta antes y 6 después. La alerta 10055 desapareció al completar CSP. Continúan observaciones de aislamiento entre orígenes, Permissions-Policy, caché de recursos y un atributo HTML que ZAP marca como posible XSS informativo. Una alerta informativa no demuestra ejecución de JavaScript ni robo de información. En la API siguen observaciones sobre Cross-Origin-Resource-Policy y contenido no almacenable; Cache-Control: no-store es intencional para los datos de la API.

El escaneo pasivo no probó todas las acciones de negocio ni rutas autenticadas. Tampoco permite asegurar que no exista XSS, fallas de autorización u otros problemas. La validación manual de F-01 cubre un caso de escritura; no representa un pentest completo. No se intentó reproducir denegación de servicio ni se accedió a información real.

El riesgo residual más importante que dejamos registrado es F-03. CodeQL señala una contraseña local que el programa escribe para inicializar PostgreSQL. Es generada para el laboratorio, pero sigue siendo una credencial funcional. Que .runtime esté ignorado por Git no protege frente a otra persona o proceso que pueda leer ese directorio. Una mejora futura es usar un almacenamiento de secretos del sistema o credenciales con permisos limitados y controles de acceso al archivo.

El token compartido de F-01 es una solución pequeña para este laboratorio. No reemplaza cuentas individuales, roles, caducidad ni auditoría por persona. El servicio debe mantenerse en localhost y usar HTTPS si se publica en un staging propio. Los datos consultables siguen siendo ficticios.

## 9. Conclusiones

Aprendimos que las herramientas miran partes distintas del proyecto. Semgrep y CodeQL revisaron patrones del código; Gitleaks buscó secretos; Dependabot y Dependency Review ayudaron con las dependencias; ZAP observó respuestas de la aplicación en funcionamiento. La falta de autenticación se entendió al revisar el flujo y probarlo, no por contar alertas.

La corrección quedó en un Pull Request y se comprobó con solicitudes y pruebas de regresión. También entendimos que una advertencia debe revisarse con contexto: el aviso de Flask no afecta la versión usada, y usar Popen no significa por sí solo que exista una inyección. Lo que faltó resolver quedó registrado, sin presentar el proyecto como totalmente seguro.

## 10. Evidencias y entrega

- [Pull Request con cambios](https://github.com/JuanMurciay/Lab-03-FDSI/pull/1).
- [SAST, secretos, regresión y revisión de dependencias](https://github.com/JuanMurciay/Lab-03-FDSI/actions/runs/44429539772).
- [CodeQL](https://github.com/JuanMurciay/Lab-03-FDSI/actions/runs/44429539812).
- [DAST y comparación HTTP antes/después](https://github.com/JuanMurciay/Lab-03-FDSI/actions/runs/44429528875).
- [Archivos originales de los resultados](../evidence/lab5/).
- [Guion de sustentación y video](GUION_SUSTENTACION.md).

Se siguió el laboratorio integrador, el kit y la presentación suministrados por el profesor. La guía pide una demostración de cinco minutos y las diapositivas mencionan un video de máximo tres minutos; el guion incluye una versión de tres minutos y una ampliación para la exposición. La grabación de la voz y la presentación de los integrantes queda a cargo del equipo; no se presenta un video inexistente como evidencia.

Las horas de los reportes originales están en UTC. Un registro del 19 de noviembre a las 00:30 UTC corresponde al 18 de noviembre a las 19:30 en Colombia. Se conservaron las fechas reales de ejecución.
