# Configuración Nginx

`nginx.conf` corresponde al contenedor de `compose.yaml` (host `api`, raíz
`/usr/share/nginx/html`). `muvautomation-baseline.conf` es la línea base
deliberada de la ronda autorizada y `muvautomation-ubuntu.conf` es el
hardening en Ubuntu con API en loopback. `lab3-api.service` inicia la API. No son
evidencia de un servidor ya desplegado; el procedimiento está en
`../docs/despliegue-ubuntu.md`.
