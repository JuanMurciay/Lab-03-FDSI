# Despliegue y evidencia en Ubuntu asignado

**Ejecutar únicamente tras recibir del docente `TARGET_IP`, `LAB_CIDR`,
ventana y permiso de sudo.** Los comandos son un procedimiento, no resultados
de ejecución. Responsable y hora UTC deben quedar junto a cada salida. Si se
dice **STOP-LAB**, detener inmediatamente. No hacer Active Scan, DoS, fuerza
bruta, MITM ni pruebas contra otros hosts.

## A. Preparación y línea base (Builder)

En el host Ubuntu asignado:

```bash
export TARGET_IP=IP_ASIGNADA
export LAB_CIDR=CIDR_AUTORIZADO
export TARGET_URL="http://$TARGET_IP"
date -u +%Y-%m-%dT%H:%M:%SZ
hostnamectl
hostname
whoami
pwd
ip -br address
uname -a
git clone https://github.com/JuanMurciay/Lab-03-FDSI.git /opt/lab3
git -C /opt/lab3 status
git -C /opt/lab3 log --oneline -5
find /opt/lab3 -maxdepth 3 -type f | sort
```

Confirmar IP, CIDR y que no es producción antes de continuar. Guardar salidas
en `evidence/blue/host-baseline.txt` sin secretos. Si `/opt/lab3` no es
escribible, usar `sudo git clone` y configurar propiedad de forma explícita.

Instalar paquetes oficiales de Ubuntu y crear usuario de servicio:

```bash
sudo apt update
sudo apt install -y nginx postgresql python3 python3-venv curl tcpdump ufw
sudo useradd --system --no-create-home --shell /usr/sbin/nologin lab3api
sudo -u postgres psql -c "CREATE ROLE falcon_app LOGIN;"
sudo -u postgres psql -c "CREATE DATABASE falcon_lab OWNER falcon_app;"
sudo -u postgres psql
```

Dentro de `psql`, ejecutar `\password falcon_app`, escribir una contraseña
local aleatoria dos veces y salir con `\q`. No colocarla en la terminal,
captura, repositorio ni reporte. Crear `/etc/lab3-api.env` con editor seguro;
contendrá una línea `DATABASE_URL=postgresql://falcon_app:VALOR_LOCAL@127.0.0.1:5432/falcon_lab`.
Si la contraseña contiene caracteres reservados de URL, codificarlos o usar
una contraseña alfanumérica. Proteger y verificar permisos **sin mostrar el
contenido**:

```bash
sudo chmod 600 /etc/lab3-api.env
sudo chown root:root /etc/lab3-api.env
sudo stat -c '%a %U:%G %n' /etc/lab3-api.env
sudo mkdir -p /var/www/muvautomation
sudo cp /opt/lab3/index.html /opt/lab3/styles.css /opt/lab3/web.js /opt/lab3/public-inventory.txt /var/www/muvautomation/
sudo chown -R root:www-data /var/www/muvautomation
sudo chmod 755 /var/www/muvautomation
sudo chmod 644 /var/www/muvautomation/index.html /var/www/muvautomation/styles.css /var/www/muvautomation/web.js /var/www/muvautomation/public-inventory.txt
stat -c '%a %U:%G %n' /var/www/muvautomation /var/www/muvautomation/*
sudo python3 -m venv /opt/lab3/.venv
sudo /opt/lab3/.venv/bin/pip install -r /opt/lab3/requirements.txt
sudo cp /opt/lab3/nginx/lab3-api.service /etc/systemd/system/lab3-api.service
sudo cp /opt/lab3/nginx/muvautomation-baseline.conf /etc/nginx/sites-available/muvautomation
sudo ln -s /etc/nginx/sites-available/muvautomation /etc/nginx/sites-enabled/muvautomation
sudo rm -f /etc/nginx/sites-enabled/default
sudo systemctl daemon-reload
sudo nginx -t
sudo systemctl enable --now postgresql lab3-api
```

Antes de habilitar el servicio HTTP, configurar UFW para el CIDR asignado y
mantener el puerto SSH **real** por el que se administra la instancia. Si no
es el puerto estándar, ajustar la regla OpenSSH antes de `ufw enable`.
Confirmar también la regla equivalente del proveedor cloud.

```bash
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow OpenSSH
sudo ufw allow from "$LAB_CIDR" to any port 80 proto tcp
sudo ufw enable
sudo ufw status numbered
sudo systemctl enable --now nginx
nginx -v
systemctl status nginx --no-pager
systemctl status lab3-api --no-pager
sudo nginx -t
sudo ss -lntp | grep -E ':80|:5000'
curl -I http://127.0.0.1/
curl -i http://127.0.0.1/api/health
```

`nginx -t` debe ser exitoso antes de cualquier reload. La API debe escuchar
solo en 127.0.0.1:5000. Nginx sirve el puerto 80 restringido por el CIDR.

Guardar URL, navegador, HTTP status, configuración efectiva (`sudo nginx -T`
puede revelar otras rutas: revisar antes de compartir), permisos, extractos
anonimizados de `access.log`/`error.log` y estado UFW. El docente debe
confirmar el alcance antes de Red Team.

## B. Hipótesis antes de cada prueba

| Amenaza | Hipótesis | Acción autorizada | Esperado | Evidencia |
|---|---|---|---|---|
| Information Disclosure | HTTP revela rutas y contenido ficticio | `curl -i "$TARGET_URL/"` y PCAP propio | HTTP 200 y GET legible | curl + PCAP filtrado |
| Information Disclosure | Cabeceras exponen tecnología | `curl -I "$TARGET_URL/"`, ZAP pasivo | headers/banners observables | respuesta + reporte HTML |
| Repudiation | Solicitud sin identidad es atribuible solo a origen/hora | GET único y comparar log | misma hora/ruta/código | comando + access.log |
| Tampering | HTTP carece de integridad en tránsito | inspección de protocolo, sin MITM | esquema `http://` | configuración + captura propia |
| Denial of Service | Rutas API inexistentes repetidas generan señal | cinco GET 404 manuales, sin carga masiva | regla dispara | cinco timestamps + log |

Antes de cada acción completar el responsable, origen, destino, hora UTC y
ventana autorizada. La tabla no registra un resultado realizado.

## C. Red Team (Kali, solo IP asignada)

```bash
mkdir -p evidence/red
date -u +%Y-%m-%dT%H:%M:%SZ | tee evidence/red/start.txt
nmap -Pn -sV -p 80 "$TARGET_IP" -oA evidence/red/nmap_port80
curl -i "$TARGET_URL/" | tee evidence/red/curl_home.txt
curl -I "$TARGET_URL/public-inventory.txt" | tee evidence/red/curl_headers.txt
```

Anotar host, puerto, producto que Nmap **realmente** identifique, status,
headers y recursos visibles. En ZAP: Manual Explore solo `TARGET_URL`, navegar
sitio e inventario ficticio, revisar Alerts/Sites, exportar reporte HTML a
`reports/zap-passive/`; no ejecutar Active Scan. Una cabecera ausente es
observación hasta validar su riesgo.

## D. Blue Team: PCAP, logs, detección y cronología

En el servidor, durante 60 s y solo para tráfico del propio laboratorio:

```bash
export RED_IP=IP_ESTACION_KALI_ASIGNADA
sudo timeout 60 tcpdump -i any -nn -s0 -w /tmp/lab3-http.pcap "host $RED_IP and host $TARGET_IP and tcp port 80"
sudo tail -n 50 /var/log/nginx/access.log
sudo tail -n 30 /var/log/nginx/error.log
sudo journalctl -u nginx --since '20 minutes ago' --no-pager
```

El filtro limita cliente Red Team y servidor asignados; confirmar ambas IP
antes de capturar y no grabar tráfico ajeno. En la ventana Red Team
solicita `/`, `/public-inventory.txt` y una ruta ficticia inexistente. Abrir el PCAP
con Wireshark, filtro `http`, y documentar solo tráfico propio. El PCAP está
excluido de Git por defecto; revisar/anonimizar antes de cualquier entrega.

Correlacionar al menos tres eventos con hora UTC, IP origen, método, ruta,
status, bytes y User-Agent. Un SYN de Nmap puede no figurar en access.log.
Tras autorización, efectuar exactamente cinco GET a una ruta **API**
inexistente, uno por comando, y evaluar la regla en la BD:

```bash
for i in 1 2 3 4 5; do date -u +%Y-%m-%dT%H:%M:%SZ; curl -i "$TARGET_URL/api/ruta-qa-inexistente"; done
sudo -u postgres psql -d falcon_lab -f /opt/lab3/deteccion.sql
```

`deteccion.sql` lee la tabla `solicitudes` de la API; un 404 puramente
estático de Nginx solo aparece en access.log y no activa esta consulta.
Comparar las cinco líneas Nginx con los cinco registros de la API. La API
puede registrar la IP del proxy en vez del cliente, lo que limita la
atribución. Explicar falsos positivos de enlaces rotos/proxy compartido.
No automatizar bloqueo.

| UTC | Acción Red | Línea Blue / PCAP | Interpretación |
|---|---|---|---|
| Pendiente | Nmap TCP/80 | Pendiente | SYN puede quedar fuera de access.log |
| Pendiente | GET `/` | Pendiente | Correlación HTTP 200 |
| Pendiente | GET `/public-inventory.txt` | Pendiente | Archivo ficticio visible |
| Pendiente | GET ruta inexistente | Pendiente | HTTP 404 y regla |

## E. Corrección y retest

Comparar commit/configuración previa con `nginx/muvautomation-ubuntu.conf`:
`server_tokens off`, `autoindex off`, cabeceras `nosniff`, `DENY` y
`no-referrer`, y denegación de rutas ocultas. Reducir campos de demostración
que no hagan falta. Validar y repetir exactamente las observaciones:

```bash
sudo cp /opt/lab3/nginx/muvautomation-ubuntu.conf /etc/nginx/sites-available/muvautomation
sudo nginx -t
sudo systemctl reload nginx
mkdir -p evidence/retest
date -u +%Y-%m-%dT%H:%M:%SZ | tee evidence/retest/start.txt
nmap -Pn -sV -p 80 "$TARGET_IP" -oA evidence/retest/nmap_port80
curl -I "$TARGET_URL/" | tee evidence/retest/headers_after.txt
curl -i "$TARGET_URL/.git/config" | tee evidence/retest/hidden_path.txt
```

La ruta oculta debe denegarse (403 o 404), la versión no aparecer en el
banner, las cabeceras sí y HTTP seguirá sin TLS. Documentar **antes,
después, causa y riesgo residual**. Solo tras completar evidencias reales,
reflexión individual y revisión del equipo:

```bash
git status
git add .
git commit -m "lab3: public HTTP baseline, telemetry and initial hardening"
git tag lab-3
git show --stat --oneline lab-3
```
