"""Inicio local Windows: instala dependencias, PostgreSQL y levanta web + API."""
import base64
import hashlib
import json
import os
import secrets
import socket
import subprocess
import sys
import tarfile
import time
import urllib.request
import urllib.error
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RUNTIME = ROOT / '.runtime'
RUNTIME.mkdir(exist_ok=True)
FLAGS = subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0


def run(args, **kwargs):
    result = subprocess.run([str(a) for a in args], capture_output=True, creationflags=FLAGS, **kwargs)
    if result.stdout:
        print(result.stdout.decode('utf-8', errors='replace'), flush=True)
    if result.stderr:
        print(result.stderr.decode('utf-8', errors='replace'), flush=True)
    result.check_returncode()
    return result


def esperar(url, proceso):
    for _ in range(60):
        if proceso.poll() is not None:
            raise RuntimeError('Un servicio terminó. Consulta los logs en .runtime.')
        try:
            with urllib.request.urlopen(url, timeout=1) as respuesta:
                if respuesta.status == 200:
                    return
        except (OSError, urllib.error.URLError):
            time.sleep(.5)
    raise RuntimeError('El servicio no respondió a tiempo. Consulta .runtime.')


def main():
    if os.name != 'nt':
        raise SystemExit('Este inicio automático es para Windows. En Linux usa Docker Compose o el procedimiento del README.')
    if sys.version_info < (3, 12):
        raise SystemExit('Usa Python 3.12 o superior para el inicio automático.')
    web_port = int(os.getenv('WEB_PORT', '80'))
    try:
        with urllib.request.urlopen(f'http://127.0.0.1:{web_port}/api/health', timeout=1) as r:
            activo = json.load(r)
        if activo.get('almacenamiento') == 'PostgreSQL' and activo.get('modo') == 'simulado':
            print(f'Falcon Lab ya está funcionando: http://127.0.0.1:{web_port}', flush=True)
            return
    except (OSError, ValueError):
        pass
    for port in (web_port, 5000):
        with socket.socket() as prueba:
            try:
                prueba.bind(('127.0.0.1', port))
            except OSError:
                raise SystemExit(f'El puerto {port} está ocupado. No se modificó el servicio existente.')
    # Aísla dependencias; nunca instala paquetes en el Python global del estudiante.
    if sys.prefix == sys.base_prefix:
        python = ROOT / '.venv' / 'Scripts' / 'python.exe'
        if not python.exists():
            run([sys.executable, '-m', 'venv', ROOT / '.venv'])
        run([python, '-m', 'pip', 'install', '-r', ROOT / 'requirements.txt'])
        raise SystemExit(subprocess.call([str(python), str(Path(__file__).resolve())]))
    import psycopg
    from psycopg import sql
    pg = RUNTIME / 'postgres' / 'package' / 'native' / 'bin'
    if not (pg / 'pg_ctl.exe').exists():
        print('Descargando PostgreSQL 17.10 para Windows (solo la primera vez)…', flush=True)
        url = 'https://registry.npmjs.org/@embedded-postgres/windows-x64/17.10.0-beta.17'
        metadata = json.load(urllib.request.urlopen(url, timeout=30))
        data = urllib.request.urlopen(metadata['dist']['tarball'], timeout=120).read()
        digest = 'sha512-' + base64.b64encode(hashlib.sha512(data).digest()).decode()
        if digest != metadata['dist']['integrity']:
            raise RuntimeError('La integridad del paquete PostgreSQL no coincide')
        archive = RUNTIME / 'postgres.tgz'
        archive.write_bytes(data)
        with tarfile.open(archive) as paquete:
            paquete.extractall(RUNTIME / 'postgres', filter='data')
    cluster = RUNTIME / 'pgdata'
    admin_file = RUNTIME / 'admin.json'
    if not admin_file.exists():
        admin_file.write_text(json.dumps({'password': secrets.token_urlsafe(24)}))
    admin = json.loads(admin_file.read_text())
    if not (cluster / 'PG_VERSION').exists():
        cluster.mkdir(parents=True, exist_ok=True)
        pwfile = RUNTIME / 'init-password.txt'
        pwfile.write_text(admin['password'], encoding='utf-8')
        try:
            run([pg / 'initdb.exe', '-D', cluster, '-U', 'postgres', '--auth=scram-sha-256', '--encoding=UTF8', '--locale=C', '--pwfile', pwfile])
        finally:
            pwfile.unlink(missing_ok=True)
    pg_iniciado = False
    with socket.socket() as prueba:
        prueba.settimeout(1)
        puerto_pg_ocupado = prueba.connect_ex(('127.0.0.1', 55432)) == 0
    if not puerto_pg_ocupado:
        # Ejecutar el servidor directamente también funciona en terminales restringidas.
        with (RUNTIME / 'postgres.log').open('a', encoding='utf-8') as log:
            subprocess.Popen([str(pg / 'postgres.exe'), '-D', str(cluster), '-h', '127.0.0.1', '-p', '55432'], stdout=log, stderr=log, creationflags=FLAGS)
        pg_iniciado = True
    # Tras un cierre inesperado PostgreSQL puede tardar más de 30 s en
    # recuperar datos. Un puerto abierto tampoco significa que ya esté listo.
    for intento in range(360):
        try:
            with psycopg.connect(host='127.0.0.1', port=55432, dbname='postgres', user='postgres', password=admin['password'], connect_timeout=1):
                break
        except psycopg.OperationalError:
            if intento == 359:
                raise
            time.sleep(.5)
    dbfile = RUNTIME / 'database.json'
    if not dbfile.exists():
        dbfile.write_text(json.dumps({'host': '127.0.0.1', 'port': 55432, 'dbname': 'falcon_lab', 'user': 'falcon_app', 'password': secrets.token_urlsafe(24)}))
    config = json.loads(dbfile.read_text())
    with psycopg.connect(host='127.0.0.1', port=55432, dbname='postgres', user='postgres', password=admin['password'], autocommit=True) as db:
        if not db.execute('SELECT 1 FROM pg_roles WHERE rolname=%s', (config['user'],)).fetchone():
            db.execute(sql.SQL('CREATE ROLE {} LOGIN PASSWORD {}').format(sql.Identifier(config['user']), sql.Literal(config['password'])))
        if not db.execute('SELECT 1 FROM pg_database WHERE datname=%s', (config['dbname'],)).fetchone():
            db.execute(sql.SQL('CREATE DATABASE {} OWNER {}').format(sql.Identifier(config['dbname']), sql.Identifier(config['user'])))
    procesos = []
    logs = []
    try:
        for archivo, url in [('app.py', 'http://127.0.0.1:5000/api/health'), ('web.py', 'http://127.0.0.1:' + os.getenv('WEB_PORT', '80') + '/')]:
            log = (RUNTIME / (archivo + '.log')).open('a', encoding='utf-8')
            logs.append(log)
            proceso = subprocess.Popen([sys.executable, '-u', str(ROOT / archivo)], cwd=ROOT, stdout=log, stderr=log, creationflags=FLAGS)
            procesos.append(proceso)
            esperar(url, proceso)
        print('LISTO: http://127.0.0.1:' + os.getenv('WEB_PORT', '80') + ' | API: http://127.0.0.1:5000/api/alertas', flush=True)
        print('PostgreSQL guarda los datos en .runtime/pgdata. Ctrl+C detiene los servicios.', flush=True)
        while all(p.poll() is None for p in procesos):
            time.sleep(1)
    except KeyboardInterrupt:
        print('Deteniendo servicios…')
    finally:
        for p in procesos:
            if p.poll() is None:
                p.terminate()
                p.wait(timeout=10)
        for log in logs:
            log.close()
        if pg_iniciado:
            estado = subprocess.run([str(pg / 'pg_ctl.exe'), '-D', str(cluster), 'status'], capture_output=True, creationflags=FLAGS)
            if estado.returncode == 0:
                run([pg / 'pg_ctl.exe', '-D', cluster, '-m', 'fast', '-w', 'stop'])


if __name__ == '__main__':
    main()
