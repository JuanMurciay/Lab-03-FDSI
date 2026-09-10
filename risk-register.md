# Matriz de riesgos — Falcon Lab

Escala académica: probabilidad (P) e impacto (I) de 1 a 3. Riesgo = P × I.
1–2 bajo; 3–4 medio; 6–9 alto. Valoración de diseño, no CVSS ni estadísticas observadas.

| ID | Amenaza / vulnerabilidad | STRIDE | P | I | Nivel | Control y estado |
|---|---|---|---:|---:|---|---|
| R1 | Lectura de alertas en tránsito por HTTP | Information Disclosure | 3 | 3 | Alto 9 | Solo datos ficticios/loopback; HTTPS pendiente Lab 4 |
| R2 | Consulta y enumeración anónimas de alertas | Information Disclosure | 3 | 2 | Alto 6 | Comprobado; autenticación/autorización pendientes Lab 4 |
| R3 | Creación de alertas falsas o cambio anónimo de estado | Tampering | 3 | 3 | Alto 9 | Comprobado; validación aplicada, identidad/roles pendientes |
| R4 | No poder atribuir acciones a una persona | Repudiation | 3 | 2 | Alto 6 | Correlación comprobada; riesgo mitigado parcialmente, identidad pendiente |
| R5 | Entrada que altere SQL | Tampering | 2 | 3 | Alto 6 | Consultas parametrizadas; caso con apóstrofe comprobado; no pentest completo |
| R6 | Interpretar datos de alerta como HTML/script | Tampering | 2 | 3 | Alto 6 | textContent y CSP implementados; revisión de código, no ZAP |
| R7 | Exponer credenciales o archivos del servidor | Information Disclosure | 2 | 3 | Alto 6 | Lista de archivos permitidos, .gitignore; /.env devuelve 404 |
| R8 | Consultas repetidas / crecimiento de registros | Denial of Service | 2 | 2 | Medio 4 | Límite de cuerpo y lista; cuotas, retención y rate limit pendientes |

Equipo responsable: Juan Sebstian Murcia Yanquen y Sara Viviana Arteaga Rodriguez, con revisión pendiente
del docente. HTTP y acceso anónimo se conservan por el alcance explícito del Lab 3;
esta decisión académica no implica aceptación para producción. La base Docker utiliza
el usuario inicializador y debe separar roles antes de un despliegue productivo.
