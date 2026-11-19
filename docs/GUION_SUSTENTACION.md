# Guion de video y sustentación - Lab 5

**Juan Sebastián Murcia y Sara Arteaga.** Versión de video: máximo tres minutos. Los textos son una guía para explicar con palabras propias; las pantallas deben corresponder a las ejecuciones reales enlazadas.

## 0:00-0:25. Proyecto y alcance - Juan Sebastián

"Continuamos con Falcon Lab, nuestra aplicación de alertas ficticias. Tiene una interfaz web, una API en Python y PostgreSQL. En este laboratorio revisamos únicamente nuestro repositorio. Las pruebas se hicieron en localhost dentro de GitHub Actions, sin datos de personas ni ataques a otros sistemas."

Mostrar el repositorio y la rama security/lab-fsi.

## 0:25-0:55. Pipeline y resultados - Sara

"Integramos Semgrep y CodeQL para revisar el código, Gitleaks para buscar secretos y Dependabot para las dependencias. También usamos ZAP con la aplicación encendida. Que un job esté verde significa que se ejecutó; por eso revisamos los reportes y no solo el color."

Mostrar [Actions](https://github.com/JuanMurciay/Lab-03-FDSI/actions), una ejecución de SAST y la alerta abierta de CodeQL. Aclarar que el archivo de actualizaciones semanales debe llegar a main para que Dependabot lo utilice.

## 0:55-1:40. Problema, corrección y prueba - Juan Sebastián

"Encontramos que era posible registrar alertas sin identificarse. En la prueba inicial enviamos una alerta inventada sin token y respondió 201. Agregamos una validación antes de las escrituras. Después, la misma solicitud recibió 401; con el token de prueba sí respondió 201. Si no hay token configurado, la escritura tampoco queda abierta."

Mostrar http-antes.json, http-despues.json y el cambio en app.py dentro del [PR](https://github.com/JuanMurciay/Lab-03-FDSI/pull/1). No mostrar el valor del token.

## 1:40-2:15. ZAP y segunda corrección - Sara

"ZAP encontró una directiva faltante en CSP. Añadimos form-action para limitar el destino de los formularios. La alerta 10055 aparecía antes y dejó de aparecer después. Eso mejora una configuración, pero no significa que hayamos demostrado o descartado todos los casos de XSS."

Mostrar los reportes ZAP antes y después. Abrir la prueba del frontend y el resultado de las diez pruebas.

## 2:15-2:55. Límites y aprendizaje - ambos

"Dejamos abierta una alerta real de CodeQL sobre contraseñas locales en texto plano. También revisamos una alerta de Semgrep sobre Popen: en ese caso no se usa shell y los argumentos vienen del programa. El token compartido es una solución sencilla para este laboratorio, no un sistema completo de usuarios. Aprendimos a identificar, corregir y volver a comprobar, dejando registradas las limitaciones."

Cerrar mostrando el informe y los enlaces a las evidencias. Reservar cinco segundos para terminar antes de los tres minutos.

## Ampliación para la demostración de cinco minutos

Usar los dos minutos adicionales para explicar la diferencia entre SAST y DAST, la comparación de Flask 3.1.3 con el aviso oficial y el riesgo residual de las consultas públicas con datos ficticios. Mostrar cómo el test cubre que un token incorrecto no escriba en la base. No realizar una nueva prueba sobre producción durante la exposición.

## Antes de grabar

Abrir los reportes descargados y el PR. Mantener ocultos .env, .runtime y cualquier token. Grabar la voz y las pantallas del equipo; este guion no reemplaza el video solicitado en las diapositivas.
