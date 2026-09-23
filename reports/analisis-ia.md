# Análisis IA de telemetría local anonimizada

**Fecha:** 23-09-2026. **Herramienta:** Codex. **Fuente:** cuatro eventos
reales de `.runtime/web.py.log` generados mediante `curl` contra
127.0.0.1:80 a las 15:13:19Z. El origen se sustituyó por
`CLIENTE-LOCAL`; se omitieron rutas del equipo y cualquier dato de la BD.
Son logs de la web local, **no** `access.log` de Nginx ni PCAP.

| UTC | Origen | Método | Ruta | Código | Bytes | Agente |
|---|---|---|---|---:|---:|---|
| 15:13:19.021Z | CLIENTE-LOCAL | GET | `/` | 200 | 3908 | curl |
| 15:13:19.068Z | CLIENTE-LOCAL | GET | `/styles.css` | 200 | 3720 | curl |
| 15:13:19.270Z | CLIENTE-LOCAL | GET | `/api/health` | 200 | 64 | curl |
| 15:13:19.309Z | CLIENTE-LOCAL | GET | `/ruta-inexistente` | 404 | 34 | curl |

## Prompt usado

> Analiza estos cuatro eventos locales anonimizados. Construye una línea de
> tiempo, separa hechos de inferencias, mapea cada observación relevante a
> STRIDE, propone tres hipótesis defensivas y señala qué evidencia adicional
> falta. No inventes IP, CVE, identidad del actor ni acciones ejecutadas.

## Respuesta de IA y validación humana pendiente del estudiante

**Hechos:** los cuatro GET se recibieron del mismo origen local en menos de un
segundo. Tres respondieron 200 y una ruta inexistente respondió 404. El
`User-Agent` declarado fue curl. Ninguna línea identifica a una persona.

**Inferencias limitadas:** la respuesta 404 puede corresponder a una prueba
controlada o un enlace incorrecto. Con un solo 404 no se dispara la regla de
cinco eventos en cinco minutos. No hay base para afirmar explotación,
intercepción de tráfico ni reconocimiento Nmap.

**STRIDE:** la ruta y estado de `/api/health` son superficie de *Information
Disclosure*; la identidad ausente limita *Repudiation*; una secuencia de 404
podría motivar una hipótesis de enumeración, pero estos datos no la prueban.

**Tres hipótesis para contrastar:** (1) cinco 404 desde un mismo origen dentro
de cinco minutos activan `deteccion.sql`; (2) la API responde 200 únicamente
si PostgreSQL está disponible; (3) un recurso no incluido en la lista estática
se rechaza con 404. Cada una requiere repetir el comando, guardar timestamp y
correlacionar con el evento generado.

**Evidencia faltante:** PCAP filtrado, logs Nginx del host autorizado, Nmap,
reporte ZAP pasivo, contexto del operador y retest remoto. La propuesta de
que una persona concreta o un atacante realizó el 404 **no puede validarse**
con estas líneas. El estudiante debe revisar este análisis antes de atribuirlo
en su entrega personal.
