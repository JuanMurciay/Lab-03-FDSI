# Evidencia local verificable — 23-09-2026

Responsable de esta comprobación: Codex, asistente de desarrollo; no se atribuye al estudiante.
Origen y destino HTTP: 127.0.0.1 (solo loopback). No se escaneó ningún host externo.
Inicio UTC: 2026-09-23T15:16:05Z
Entorno: Windows; Python http.server 8080 sirve una carpeta temporal con solo index.html, styles.css y web.js.
La aplicación funcional separada usa HTTP 80 → API 5000 → PostgreSQL 55432.

### `git status --short --branch`
UTC: 2026-09-23T15:16:05Z · origen: este equipo · destino: repositorio local · responsable: Codex.
```text
## main...origin/main
M  ENTREGA.md
M  README.md
A  app/README.md
M  compose.yaml
R  dfd-lab3.png -> diagrams/dfd-lab3.png
A  docs/cumplimiento-lab3.md
AM docs/despliegue-ubuntu.md
A  evidence/blue/README.md
A  evidence/local/accesos-anonimizados.md
A  evidence/local/verificacion-2026-09-23.md
A  evidence/red/README.md
A  evidence/retest/README.md
M  evidencia-local.json
M  iniciar.py
A  nginx/README.md
A  nginx/lab3-api.service
A  nginx/muvautomation-baseline.conf
A  nginx/muvautomation-ubuntu.conf
R  nginx.conf -> nginx/nginx.conf
A  reports/analisis-ia.md
A  reports/zap-passive/README.md
M  risk-register.md
AM scripts/capturar-local.ps1
M  verificar.py
M  web.py
```

### `git log --oneline -5`
UTC: 2026-09-23T15:16:05Z · origen: este equipo · destino: repositorio local · responsable: Codex.
```text
4a49045 lab3: web HTTP, API REST y PostgreSQL local
70b3649 Update student names and formatting in README
adf0ba4 lab3: retirar inventario genérico; usar API Falcon
da66279 lab3: prototipo inicial de alertas Falcon ficticias
a57b1e1 lab3: sitio HTTP e inventario ficticio
```

### `git ls-files (equivalente seguro de find para archivos versionados)`
UTC: 2026-09-23T15:16:05Z · origen: este equipo · destino: repositorio local · responsable: Codex.
```text
.dockerignore
.env.example
.gitattributes
.gitignore
Dockerfile
ENTREGA.md
INICIAR.cmd
README.md
alerta-ejemplo.json
app.py
app/README.md
compose.yaml
deteccion.sql
diagrams/dfd-lab3.png
docs/cumplimiento-lab3.md
docs/despliegue-ubuntu.md
evidence/blue/README.md
evidence/local/accesos-anonimizados.md
evidence/local/verificacion-2026-09-23.md
evidence/red/README.md
evidence/retest/README.md
evidencia-local.json
index.html
iniciar.py
nginx/README.md
nginx/lab3-api.service
nginx/muvautomation-baseline.conf
nginx/muvautomation-ubuntu.conf
nginx/nginx.conf
reports/analisis-ia.md
reports/zap-passive/README.md
requirements.txt
risk-register.md
schema.sql
scripts/capturar-local.ps1
styles.css
verificar.py
web.js
web.py
```

### `git -C CLON rev-parse --short HEAD; git -C CLON remote get-url origin; Test-Path CLON/index.html`
UTC: 2026-09-23T15:16:05Z · origen: este equipo · destino: clon local obtenido de github.com/JuanMurciay/Lab-03-FDSI · responsable: Codex.
```text
4a49045
https://github.com/JuanMurciay/Lab-03-FDSI.git
True
```

### `find . -maxdepth 3 -type f (clon limpio)`
UTC: 2026-09-23T15:16:06Z · origen: este equipo · destino: clon local obtenido de GitHub · responsable: Codex.
```text
./.dockerignore
./.env.example
./.git/config
./.git/description
./.git/HEAD
./.git/hooks/applypatch-msg.sample
./.git/hooks/commit-msg.sample
./.git/hooks/fsmonitor-watchman.sample
./.git/hooks/post-update.sample
./.git/hooks/pre-applypatch.sample
./.git/hooks/pre-commit.sample
./.git/hooks/pre-merge-commit.sample
./.git/hooks/pre-push.sample
./.git/hooks/pre-rebase.sample
./.git/hooks/pre-receive.sample
./.git/hooks/prepare-commit-msg.sample
./.git/hooks/push-to-checkout.sample
./.git/hooks/sendemail-validate.sample
./.git/hooks/update.sample
./.git/index
./.git/info/exclude
./.git/logs/HEAD
./.git/packed-refs
./.git/shallow
./.gitattributes
./.gitignore
./alerta-ejemplo.json
./app.py
./compose.yaml
./deteccion.sql
./dfd-lab3.png
./Dockerfile
./ENTREGA.md
./evidencia-local.json
./index.html
./INICIAR.cmd
./iniciar.py
./nginx.conf
./README.md
./requirements.txt
./risk-register.md
./schema.sql
./styles.css
./verificar.py
./web.js
./web.py
```

### `curl -I http://127.0.0.1:8080/`
UTC: 2026-09-23T15:16:06Z · origen: este equipo · destino: 127.0.0.1:8080 · responsable: Codex.
```text
HTTP/1.0 200 OK
Server: SimpleHTTP/0.6 Python/3.12.14
Date: Wed, 23 Sep 2026 15:16:06 GMT
Content-type: text/html
Content-Length: 3908
Last-Modified: Wed, 23 Sep 2026 14:59:56 GMT
```

### `curl -i http://127.0.0.1:8080/ (primeras líneas y longitud)`
UTC: 2026-09-23T15:16:06Z · origen: este equipo · destino: 127.0.0.1:8080 · responsable: Codex.
```text
HTTP/1.0 200 OK
Server: SimpleHTTP/0.6 Python/3.12.14
Date: Wed, 23 Sep 2026 15:16:06 GMT
Content-type: text/html
Content-Length: 3908
Last-Modified: Wed, 23 Sep 2026 14:59:56 GMT

<!doctype html>
<html lang="es">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Falcon Lab · Alertas de seguridad</title><link rel="stylesheet" href="/styles.css"><script src="/web.js" defer></script></head>
Caracteres recibidos: 4082
```

### `curl -I http://127.0.0.1/`
UTC: 2026-09-23T15:16:06Z · origen: este equipo · destino: 127.0.0.1:80 · responsable: Codex.
```text
HTTP/1.1 200 OK
Accept-Ranges: bytes
Cache-Control: no-store
Content-Disposition: inline; filename=index.html
Content-Length: 3908
Content-Security-Policy: default-src 'self'; script-src 'self'; style-src 'self'; frame-ancestors 'none'; base-uri 'none'
Content-Type: text/html; charset=utf-8
Date: Wed, 23 Sep 2026 15:16:06 GMT
Etag: "1789004651.1981564-3908-2679251934"
Last-Modified: Thu, 10 Sep 2026 01:44:11 GMT
Referrer-Policy: no-referrer
Server: LabHTTP
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
```

### `curl -i http://127.0.0.1/api/health`
UTC: 2026-09-23T15:16:06Z · origen: este equipo · destino: 127.0.0.1:80 → API local → PostgreSQL · responsable: Codex.
```text
HTTP/1.1 200 OK
Cache-Control: no-store
Content-Length: 64
Content-Security-Policy: default-src 'self'; script-src 'self'; style-src 'self'; frame-ancestors 'none'; base-uri 'none'
Content-Type: application/json
Date: Wed, 23 Sep 2026 15:16:06 GMT
Referrer-Policy: no-referrer
Server: LabHTTP
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-Request-Id: 1e05c5a5-b771-4f1f-b599-3ca37f8980eb

{"almacenamiento":"PostgreSQL","estado":"ok","modo":"simulado"}
```

Fin UTC: 2026-09-23T15:16:06Z

Interpretación: la página estática respondió 200; la aplicación y la API respondieron 200 en el host local. El repositorio público se clonó y contiene index.html. No se midió acceso desde otra máquina.
