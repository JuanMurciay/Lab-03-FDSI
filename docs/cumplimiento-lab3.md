# Cumplimiento de la guía Laboratorio 3 (revisión 23-09-2026)

**Fuente:** `Laboratorio_3_HTTP_Red_Blue_Team (1).pdf`, 11 páginas. La columna
"comprobado" indica evidencia producida, no trabajo que se espera realizar.
No hay IP, CIDR, ventana ni servidor Ubuntu asignados al equipo.

| Requisito de la guía | Estado | Evidencia o acción restante |
|---|---|---|
| Prototipo HTTP anónimo con datos ficticios | **Comprobado local** | `README.md`, `index.html`, `app.py`, `evidencia-local.json` |
| GitHub público, clonación, archivos y commit | **Comprobado** | `evidence/local/verificacion-2026-09-23.md` |
| URL HTTP de instancia Ubuntu en CIDR autorizado | **Pendiente** | Docente debe asignar IP/CIDR/ventana; luego ejecutar `docs/despliegue-ubuntu.md` |
| Host Ubuntu, Nginx, UFW, permisos y logs | **Configurado en archivos; sin ejecución** | `nginx/muvautomation-ubuntu.conf`, `nginx/lab3-api.service`; Compose validó sintaxis, no arrancó daemon |
| DFD con dos límites y STRIDE | **Documentado** | `diagrams/dfd-lab3.png`, README y `risk-register.md` |
| Hipótesis previa con comando, esperado y evidencia | **Preparado** | Tabla en `docs/despliegue-ubuntu.md`; completar antes de cada prueba real |
| Nmap puerto 80, curl, superficie observada | **Pendiente** | `evidence/red/`, solo IP autorizada |
| ZAP Manual Explore pasivo y reporte HTML | **Pendiente** | `reports/zap-passive/`, sin Active Scan |
| PCAP filtrado de HTTP | **Pendiente** | `evidence/blue/`, solo tráfico propio del ejercicio |
| Correlación de al menos tres eventos Nginx | **Pendiente** | Línea temporal UTC, acceso/error log y comandos Red Team |
| Regla 5 respuestas 404/5 minutos | **Comprobada localmente** | `deteccion.sql`, `evidencia-local.json`; validar también en Nginx real |
| Hardening y reducción de exposición | **Comprobado local; Nginx pendiente** | Cabeceras y ruta oculta en local; inventario antes/después en `docs/reduccion-contenido.md`; `nginx -t`/retest en servidor |
| Comparación antes/después | **Parcial** | API auxiliar local en `ENTREGA.md`; falta retest Red/Blue remoto |
| Registro de riesgos y estados | **Documentado** | `risk-register.md` |
| Prompt/respuesta de IA anonimizados y validación | **Documentado** | `reports/analisis-ia.md`; solo datos ficticios |
| Reflexión individual ≤250 palabras | **Pendiente del estudiante** | Escribir después de su práctica y defensa oral |
| Etiqueta final `lab-3` | **Pendiente** | Crear sobre commit final cuando las evidencias externas sean reales |

La estructura esperada está representada por `app/`, `nginx/`, `diagrams/`,
`evidence/red/`, `evidence/blue/` y `reports/zap-passive/`. Los README de
carpetas vacías explican lo que falta; no sustituyen evidencias.

## Cinco preguntas de análisis de la guía

1. Red Team puede observar sin explotar: puerto, banner, código HTTP, rutas,
   cabeceras y datos ficticios públicos. La observación real de un host Ubuntu
   aún debe registrarse.
2. Un SYN de Nmap puede no aparecer en `access.log` porque Nginx registra
   peticiones HTTP recibidas, no todos los paquetes de red. Validar con PCAP.
3. Ocultar versión, denegar rutas ocultas y agregar cabeceras reduce exposición;
   no cifra HTTP. TLS pertenece al Lab 4.
4. Para distinguir `curl` legítimo hacen falta alcance/ventana autorizados,
   origen, hora, ruta, frecuencia, código, correlación con el comando y
   contexto del operador. Un User-Agent por sí solo no basta.
5. Se priorizan Spoofing, Elevation of Privilege e Information Disclosure en
   Lab 4 mediante identidad, roles y TLS. La conclusión de IA no verificable
   sobre logs reales se registra en `reports/analisis-ia.md`.
