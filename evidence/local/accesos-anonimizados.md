# Correlación local de cuatro solicitudes HTTP

Comprobación por Codex el **23-09-2026, 15:13:18–15:13:19 UTC**. Origen y
destino reales: 127.0.0.1:80, sustituidos aquí por `CLIENTE-LOCAL` y
`WEB-LOCAL`. Comandos: `curl -sS -o NUL -w ...` a `/`, `/styles.css`,
`/api/health` y `/ruta-inexistente`, uno por ruta. El extracto procede de
`.runtime/web.py.log`, no de Nginx. Solo contiene datos ficticios.

| UTC | Origen → destino | Método | Ruta | HTTP | Bytes | Correlación |
|---|---|---|---|---:|---:|---|
| 15:13:19.021Z | CLIENTE-LOCAL → WEB-LOCAL | GET | `/` | 200 | 3908 | Primera solicitud curl |
| 15:13:19.068Z | CLIENTE-LOCAL → WEB-LOCAL | GET | `/styles.css` | 200 | 3720 | Segunda solicitud curl |
| 15:13:19.270Z | CLIENTE-LOCAL → WEB-LOCAL | GET | `/api/health` | 200 | 64 | Tercera solicitud curl; web → API → BD |
| 15:13:19.309Z | CLIENTE-LOCAL → WEB-LOCAL | GET | `/ruta-inexistente` | 404 | 34 | Cuarta solicitud curl |

Interpretación: las cuatro salidas `curl` coincidieron con ruta y código del
registro web en menos de un segundo. Esto prueba telemetría local, **no**
correlación de Blue Team en Ubuntu. Un solo 404 no cumple el umbral de cinco
respuestas 404 en cinco minutos. No se capturó PCAP ni se ejecutó Nmap.
