"""Pruebas locales reales. Crea una alerta ficticia y solicitudes 404 controladas."""
import json
import os
import subprocess
import sys
import time
import urllib.request
import urllib.error
from datetime import datetime, timezone
from pathlib import Path
from app import conectar

ROOT = Path(__file__).resolve().parent
resultados = []


def peticion(ruta, datos=None, base='http://127.0.0.1', raw=None):
    contenido = raw if raw is not None else (json.dumps(datos).encode() if datos is not None else None)
    req = urllib.request.Request(base + ruta, data=contenido, headers={'Content-Type': 'application/json'})
    try:
        r = urllib.request.urlopen(req, timeout=10)
    except urllib.error.HTTPError as error:
        r = error
    with r:
        body = r.read().decode('utf-8')
        return r.status, {k.lower(): v for k, v in r.headers.items()}, json.loads(body) if 'json' in r.headers.get('Content-Type', '') else body


def comprobar(nombre, condicion, detalle):
    resultados.append({'prueba': nombre, 'resultado': 'PASS' if condicion else 'FAIL', 'detalle': detalle})
    assert condicion, nombre


def auxiliar(hardening):
    env = dict(os.environ, API_PORT='5001', HARDENING=str(hardening))
    p = subprocess.Popen([sys.executable, str(ROOT / 'app.py')], env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                         creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0)
    for _ in range(60):
        try:
            if peticion('/api/health', base='http://127.0.0.1:5001')[0] == 200:
                return p
        except OSError:
            time.sleep(.2)
    p.terminate(); p.wait()
    raise RuntimeError('No inició la API auxiliar de retest')


def main():
    inicio = datetime.now(timezone.utc).isoformat()
    status, headers, html = peticion('/')
    comprobar('Aplicación web por HTTP', status == 200 and 'Falcon Lab' in html, 'GET http://127.0.0.1/ sin autenticación')
    status, _, inventario = peticion('/public-inventory.txt')
    comprobar('Inventario público ficticio', status == 200 and all(x in inventario for x in ('WEB-LAB-01', 'API-LAB-01', 'DB-LAB-01')), 'Archivo público de prueba sin IP ni secretos reales')
    status, _, health = peticion('/api/health')
    comprobar('Web → REST → API → PostgreSQL', status == 200 and health['almacenamiento'] == 'PostgreSQL', health)
    datos = {'titulo': "Prueba local: alerta ficticia O'Brien", 'hostname': 'EQUIPO-QA-LAB', 'severidad': 'alta', 'descripcion': 'Registro ficticio de verificación local automatizada.'}
    status, headers, alerta = peticion('/api/alertas', datos)
    id_alerta = alerta['id']
    comprobar('Recepción anónima', status == 201, {'id': id_alerta, 'request_id': headers.get('x-request-id')})
    with conectar() as db:
        row = db.execute('SELECT titulo FROM alertas WHERE id=%s', (id_alerta,)).fetchone()
        audit = db.execute('SELECT codigo,metodo FROM solicitudes WHERE request_id=%s', (headers['x-request-id'],)).fetchone()
        version = db.execute('SHOW server_version').fetchone()['server_version']
    comprobar('Persistencia real y consulta parametrizada', row['titulo'] == datos['titulo'], {'motor': 'PostgreSQL', 'version': version, 'apostrofe_conservado': True})
    comprobar('Correlación de solicitud', audit['codigo'] == 201 and audit['metodo'] == 'POST', 'X-Request-ID coincide con solicitudes en PostgreSQL')
    for accion in [{'tipo':'clasificar','severidad':'critica'}, {'tipo':'enriquecer','nota':'Contexto de prueba ficticio'}, {'tipo':'escalar','nota':'Escalamiento simulado sin envío'}, {'tipo':'cerrar','nota':'Cierre de prueba'}]:
        status, _, response = peticion(f'/api/alertas/{id_alerta}/acciones', accion)
        comprobar('Acción ' + accion['tipo'], status == 201, {'accion_id': response.get('id')})
    status, _, detalle = peticion(f'/api/alertas/{id_alerta}')
    comprobar('Estado e historial persistidos', detalle['estado'] == 'cerrada' and detalle['severidad'] == 'critica' and len(detalle['acciones']) == 5, {'acciones': len(detalle['acciones'])})
    comprobar('Validación de entrada', peticion('/api/alertas', {'titulo':'incompleta'})[0] == 400, 'Campos obligatorios ausentes → 400')
    comprobar('Límite de cuerpo', peticion('/api/alertas', raw=b'{' + b'x' * 9000)[0] == 413, 'Más de 8192 bytes → 413')
    comprobar('Archivo oculto inaccesible', peticion('/.env')[0] == 404, 'La web solo sirve archivos permitidos')
    for i in range(5):
        comprobar(f'404 controlado {i+1}', peticion('/api/ruta-qa-inexistente')[0] == 404, 'Solo localhost, sin fuerza bruta')
    with conectar() as db:
        detection = db.execute((ROOT / 'deteccion.sql').read_text()).fetchall()
    comprobar('Detección cinco 404 / cinco minutos', any(r['errores_404'] >= 5 for r in detection), 'Ventana temporal evaluada en PostgreSQL; origen local compartido por el proxy')
    p = auxiliar(0)
    try:
        status, before, _ = peticion('/api/alertas', base='http://127.0.0.1:5001')
        comprobar('Línea base de cabeceras', status == 200 and 'x-frame-options' not in before, 'API auxiliar local HARDENING=0; control de laboratorio, no tráfico externo')
    finally:
        p.terminate(); p.wait(timeout=10)
    p = auxiliar(1)
    try:
        status, after, row = peticion(f'/api/alertas/{id_alerta}', base='http://127.0.0.1:5001')
        comprobar('Persistencia tras reiniciar API auxiliar', status == 200 and row['estado'] == 'cerrada', 'Proceso API nuevo; PostgreSQL conserva la alerta y sus acciones')
        comprobar('Retest de cabeceras', after.get('x-frame-options') == 'DENY' and after.get('x-content-type-options') == 'nosniff', {'antes': {k:v for k,v in before.items() if k.startswith('x-')}, 'despues': {k:v for k,v in after.items() if k.startswith('x-')}})
    finally:
        p.terminate(); p.wait(timeout=10)
    informe = {'inicio_utc': inicio, 'fin_utc': datetime.now(timezone.utc).isoformat(), 'entorno': 'Local Windows; pruebas automatizadas por Codex; no pruebas del estudiante ni nube', 'objetivo': '127.0.0.1:80, :5000 y API auxiliar :5001; PostgreSQL :55432', 'pruebas': resultados, 'no_ejecutado': ['Nmap', 'ZAP', 'PCAP', 'Pruebas entre equipos', 'Nginx/Docker en este host']}
    (ROOT / 'evidencia-local.json').write_bytes(json.dumps(informe, ensure_ascii=False, indent=2, default=str).encode('utf-8'))
    print(f'{len(resultados)} comprobaciones PASS. Evidencia: evidencia-local.json')


if __name__ == '__main__':
    main()
