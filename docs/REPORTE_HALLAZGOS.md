# Reporte de hallazgos - Lab 5

**Integrantes:** Juan Sebastián Murcia y Sara Arteaga.  
**Proyecto:** Falcon Lab. **Fecha:** 18 de noviembre de 2026.  
**Repositorio:** https://github.com/JuanMurciay/Lab-03-FDSI. **Línea base:** 6a1f8839c234bbe5f4258e9868808ac3996cda35.  
**Versión corregida:** 19de2cd598f566b54620130512de2d90f900f25a. **PR:** https://github.com/JuanMurciay/Lab-03-FDSI/pull/1.  
**Entorno:** localhost en contenedores temporales del propio repositorio, con datos ficticios.

## F-01. Operaciones de escritura sin autenticación

- **Origen y categoría:** revisión de app.py y validación HTTP, CWE-306, ausencia de autenticación en funciones importantes.
- **Riesgo:** medio en la instalación local. Estimamos probabilidad 2 e impacto 3 en una escala de 1 a 3: 2 x 3 = 6. Otra persona o proceso con acceso al servicio podía insertar alertas y llamar a las acciones sin credencial. Publicarlo en red aumentaría la exposición.
- **Evidencia inicial:** POST /api/alertas con un objeto JSON ficticio y sin X-Lab-Token respondió 201. El archivo http-antes.json conserva la respuesta.
- **Impacto:** principalmente integridad de las alertas y del historial. No se demostró extracción de datos ni se hizo una prueba de agotamiento de recursos.
- **Corrección:** exigir LAB_API_TOKEN en el entorno y validar X-Lab-Token antes de escribir. El frontend lo solicita en memoria y web.py lo reenvía. Sin configuración, la escritura se rechaza.
- **Validación posterior:** sin token 401; token incorrecto 401; token temporal correcto 201. Diez pruebas de regresión pasan. Se comprobó con PostgreSQL real en Actions y por separado con dobles de prueba en los tests.
- **Estado:** corregido en https://github.com/JuanMurciay/Lab-03-FDSI/pull/1; evidencia en https://github.com/JuanMurciay/Lab-03-FDSI/actions/runs/44429528875 y evidence/lab5/http-*.json.
- **Límite:** no se implementaron cuentas ni roles; las consultas de datos ficticios permanecen públicas.

## F-02. Política CSP sin la directiva form-action

- **Origen:** ZAP Baseline, regla 10055, CSP: Failure to Define Directive with No Fallback.
- **Riesgo:** medio según ZAP. Nuestra estimación fue probabilidad 2 e impacto 2: 4. Es una configuración incompleta; no demuestra por sí sola que exista XSS.
- **Evidencia:** ZAP señaló que faltaba form-action. Esta directiva no hereda la restricción de default-src. La configuración afectada estaba en nginx/nginx.conf y también se ajustó la alternativa web.py.
- **Impacto posible:** falta una restricción del navegador sobre el destino de los formularios, relevante si otra falla permite alterar el contenido. No se intentó enviar información a ningún tercero.
- **Corrección:** añadir form-action 'self' al frontend. La API recibió form-action 'none' dentro de una política restrictiva.
- **Resultado:** la regla 10055 aparece en zap-web-antes.json y no aparece en zap-web-despues.json de la ejecución final. La prueba de regresión comprueba las dos configuraciones del frontend.
- **Estado:** corregido en el mismo PR. Quedan otras alertas DAST registradas.

## F-03. Contraseña de PostgreSQL almacenada en texto plano local

- **Origen:** CodeQL, py/clear-text-storage-sensitive-data, iniciar.py, línea 95 en el código analizado. CWE-312.
- **Riesgo:** alto según la herramienta; medio en el escenario local que evaluamos. Probabilidad 2 e impacto 2: 4. La contraseña es generada para PostgreSQL del laboratorio y no es un secreto de un servicio real externo, pero sí tiene valor para acceder a la base local.
- **Evidencia minimizada:** el programa escribe la contraseña en un archivo de .runtime. No copiamos el valor, no abrimos credenciales existentes y no publicamos el archivo generado.
- **Impacto:** confidencialidad y posible acceso a la base si otra persona o proceso puede leer el directorio.
- **Decisión:** verdadero positivo abierto. .gitignore reduce el riesgo de publicarlo en Git; no cifra ni limita por sí mismo quién puede leerlo. El borrado del archivo temporal después de usarlo reduce la duración de una de las copias, pero no resuelve las demás.
- **Recomendación:** evaluar el almacén de secretos del sistema y permisos mínimos en los archivos locales. No se modificó este flujo para mantener una remediación pequeña y comprobable.
- **Evidencia:** https://github.com/JuanMurciay/Lab-03-FDSI/security/code-scanning/1 y evidence/lab5/codeql-resumen.json.

## F-04. Posible inyección al iniciar procesos

- **Origen:** Semgrep, dangerous-subprocess-use-tainted-env-args, iniciar.py, línea 134.
- **Resultado:** alerta de auditoría con severidad ERROR en el reporte. Para la inyección de shell descrita se consideró un falso positivo en el flujo revisado.
- **Justificación:** Popen recibe una lista de argumentos, no se usa shell=True y los ejecutables y archivos salen del propio programa. El puerto configurable modifica la URL de espera, no construye un comando de shell. No identificamos entrada HTTP que seleccione un ejecutable.
- **Decisión:** no añadir escapes de shell a una lista que no pasa por shell. No se eliminó la regla ni se ocultó la alerta. Esto no descarta otros riesgos de procesos locales o archivos modificados.
- **Evidencia:** ambos reportes Semgrep y revisión del bloque de inicio. No se ejecutó ningún comando malicioso.

## F-05. Reenvío del encabezado Host en una configuración alternativa

- **Origen:** Semgrep, request-host-used, nginx/muvautomation-ubuntu.conf, línea 17.
- **Riesgo estimado:** bajo en el entorno probado; probabilidad 1 e impacto 2: 2. Se mantiene para revisión de despliegue.
- **Contexto:** esa configuración reenvía $host a la API y permite un nombre de servidor genérico. El Compose del laboratorio usa nginx/nginx.conf, que es otro archivo. No confirmamos que la aplicación genere enlaces sensibles o decisiones de autorización a partir de Host.
- **Decisión:** no llamarlo explotación confirmada ni descartarlo automáticamente como falso positivo. Revisar nombres de servidor y hosts permitidos antes de un despliegue propio fuera de localhost.
- **Evidencia:** resultados Semgrep y comparación de los archivos de Nginx; no se atacó el dominio de laboratorios previos.

## R-06. Dependencia revisada: Flask 3.1.3

- **Control:** Dependabot alerts y Dependency Review, más lectura del aviso oficial GHSA-68rp-wp8r-4726.
- **Versión y alcance:** el proyecto fija Flask 3.1.3. El aviso afecta versiones anteriores a 3.1.3 y trata de respuestas con sesiones y caché. La aplicación no usa sesiones de Flask y la API envía no-store.
- **Resultado:** aviso no aplicable a la versión actual. No fue una alerta emitida por Dependabot ni un falso positivo automático; fue una comparación manual de versiones.
- **Medida:** mantener la versión fijada y revisar futuros avisos con Dependabot. No se inventó una dependencia vulnerable ni se degradó una biblioteca para producir evidencia.
- **Limitación:** cero alertas abiertas y una revisión de cambios aprobada no certifican todas las dependencias transitivas o imágenes de contenedor.
- **Fuente:** https://github.com/pallets/flask/security/advisories/GHSA-68rp-wp8r-4726.

## Criterio de riesgo

Usamos probabilidad e impacto de 1 a 3 para ordenar los resultados: 1-2 bajo, 3-6 medio y 9 alto. Es una valoración simple del escenario local, no un cálculo CVSS. Se conserva por separado la severidad que informa cada herramienta. No se ejecutaron pruebas destructivas para subir o bajar una clasificación.

## Reflexión final

Las herramientas ayudaron a ubicar patrones, pero tuvimos que revisar cómo se usa el código. La evidencia más clara fue observar un registro aceptado sin token y comprobar el rechazo después del cambio. Mantener los resultados pendientes en el reporte nos parece más útil que afirmar que todo está seguro porque terminó el pipeline.
