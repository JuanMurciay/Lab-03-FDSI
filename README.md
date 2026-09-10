# Lab 3 — Automatización de incidentes de CrowdStrike Falcon

**Estudiantes:**

- Juan Sebstian Murcia Yanquen.
- Sara Viviana Arteaga Rodriguez.

**Opción 1 · Entrega local**

Prototipo académico con la arquitectura solicitada:

**Usuario anónimo → HTTP → Aplicación web → REST → API pública → PostgreSQL.**

Solo utiliza alertas ficticias. No se conecta a CrowdStrike ni necesita tokens Falcon.
La API es pública en el sentido de que no exige autenticación; en esta entrega está
disponible únicamente en el equipo local, no en Internet.

## Abrir y ejecutar en Windows

Requisito: Python 3.12 o superior y conexión a Internet para la primera instalación.
En este equipo también puedes hacer doble clic en **INICIAR.cmd**: detecta el Python
incluido con Codex. Si no existe, utiliza el lanzador `py` de una instalación de Python.
Descarga el repositorio, abre una terminal en su carpeta y ejecuta:

```powershell
python iniciar.py
```

El iniciador crea un entorno virtual, instala tres dependencias, prepara PostgreSQL
17.10 para Windows y arranca ambos servicios. No instala un servicio global de Windows.

- Aplicación: http://127.0.0.1/ (HTTP, puerto 80).
- API directa: http://127.0.0.1:5000/api/alertas.
- PostgreSQL: 127.0.0.1:55432, con contraseña local aleatoria.

Mantén la terminal abierta; Ctrl+C detiene los servicios y conserva la base de datos.
Si el puerto 80 está ocupado, usa `$env:WEB_PORT='8080'` antes de iniciar y abre
http://127.0.0.1:8080. No elimines `.runtime/pgdata` si deseas conservar tus datos.
`.runtime/` contiene credenciales y archivos locales: está excluida de Git y del ZIP.

## Demostración de cinco minutos

1. Pulsa **Completar ejemplo** y después **Registrar alerta**.
2. Verifica que la alerta aparece en la bandeja y que tiene un ID.
3. Selecciónala y añade una nota con **Añadir contexto ficticio**.
4. Cambia su severidad, escálala de forma simulada y consulta el historial.
5. Reinicia con `python iniciar.py`: la alerta y sus acciones continúan en PostgreSQL.

El escalamiento solo cambia el estado; no envía correos, tickets ni acciones a terceros.
El enriquecimiento es una nota manual. La clasificación cambia la severidad seleccionada;
no existe un motor de IA ni una integración SOAR real.

## Qué entregar

- [Informe: requisitos, DFD, riesgos y controles](ENTREGA.md).
- [Diagrama de flujo de datos](dfd-lab3.png).
- [Matriz de riesgos](risk-register.md).
- [Evidencia de 22 comprobaciones locales reales](evidencia-local.json).
- Código de aplicación web, API, SQL y procedimiento de reproducción en este repositorio.

La versión inicial solo guardaba alertas en memoria. La versión actual incorpora interfaz
web y PostgreSQL real, conforme a la arquitectura indicada posteriormente por el docente.

## Archivos principales

| Archivo | Función |
|---|---|
| `index.html`, `styles.css`, `web.js` | Interfaz web; consume REST con fetch |
| `web.py` | Servidor HTTP local y proxy hacia la API |
| `app.py` | API REST con Flask y consultas SQL parametrizadas |
| `schema.sql` | Tablas alertas, acciones y solicitudes |
| `iniciar.py` | Inicio automático en Windows |
| `INICIAR.cmd` | Acceso por doble clic en Windows |
| `requirements.txt` | Dependencias fijadas |
| `verificar.py`, `deteccion.sql` | Pruebas locales y detección defensiva |
| `compose.yaml`, `Dockerfile`, `nginx.conf` | Alternativa Docker/Nginx para reproducir después |

## API REST

| Método y ruta | Resultado |
|---|---|
| GET `/api/health` | Comprueba conexión real con PostgreSQL |
| GET `/api/alertas` | Lista hasta 200 alertas, opcional `?severidad=alta` |
| POST `/api/alertas` | Recibe una alerta ficticia y registra la acción |
| GET `/api/alertas/{id}` | Detalle e historial |
| POST `/api/alertas/{id}/acciones` | clasificar, enriquecer, escalar o cerrar |
| GET `/api/acciones` | Últimas 200 acciones |

Ejemplo PowerShell, sin autenticación:

```powershell
Invoke-RestMethod -Method Post -Uri http://127.0.0.1/api/alertas -ContentType 'application/json; charset=utf-8' -InFile alerta-ejemplo.json
Invoke-RestMethod http://127.0.0.1/api/alertas
```

## Verificación

Con el sistema encendido, en otra terminal:

```powershell
.\.venv\Scripts\python.exe verificar.py
```

La prueba crea una alerta ficticia, registra acciones, provoca cinco 404 locales y
levanta temporalmente una segunda API en 5001 para comprobar el antes/después y la
persistencia al reiniciarla. Actualiza `evidencia-local.json`. No ejecutarla contra terceros.
Las evidencias suministradas corresponden a comprobaciones automatizadas de Codex; no
se atribuyen al estudiante ni sustituyen su demostración propia.

## Alternativa Docker (no ejecutada en este equipo)

Requiere Docker y Compose. Copia `.env.example` a `.env`, define una contraseña larga
alfanumérica local y ejecuta `docker compose up --build`. La web queda en localhost:80,
la API en localhost:5000 y PostgreSQL solo en la red de contenedores. No uses
`docker compose down -v` si necesitas conservar el volumen. La imagen oficial crea el
usuario de inicialización con privilegios elevados; antes de un despliegue real debe
separarse el usuario administrador del usuario de la API. El inicio Windows ya los separa.

## Alcance de la entrega

Se entrega el prototipo local funcional y el análisis de requisitos, DFD, riesgos y
controles. No se afirma que se completó la ronda entre equipos del laboratorio de tres
horas. Nmap, ZAP, PCAP, firewall de una instancia y retest Nginx quedan pendientes del
entorno autorizado. HTTPS e identidad se reservan para Lab 4. No se crea la etiqueta
final `lab-3` como si esas actividades ya estuvieran realizadas.


## Referencias

- Guía docente Laboratorio_3_HTTP_Red_Blue_Team.pdf y arquitectura facilitada en las fotos.
- [CrowdStrike Alerts](https://developer.crowdstrike.com/api-reference/collections/alerts/#postaggregatesalertsv1): referencia conceptual, no contrato implementado. El endpoint enlazado corresponde a agregaciones.
- [Flask](https://flask.palletsprojects.com/en/stable/), [Psycopg](https://www.psycopg.org/psycopg3/docs/) y [PostgreSQL](https://www.postgresql.org/docs/17/).
- [Distribución portable PostgreSQL utilizada por el iniciador](https://github.com/leinelissen/embedded-postgres): versión fijada y checksum SHA-512 comprobado contra el registro.
