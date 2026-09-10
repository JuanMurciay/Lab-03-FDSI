"""API REST académica: alertas ficticias de Falcon y PostgreSQL real."""
import json
import os
import uuid
from pathlib import Path
import psycopg
from psycopg.rows import dict_row
from flask import Flask, g, jsonify, request
from werkzeug.exceptions import HTTPException

ROOT = Path(__file__).resolve().parent
SEVERIDADES = {'baja', 'media', 'alta', 'critica'}


def conectar():
    if os.getenv('DATABASE_URL'):
        return psycopg.connect(os.environ['DATABASE_URL'], row_factory=dict_row)
    config = json.loads((ROOT / '.runtime' / 'database.json').read_text())
    return psycopg.connect(**config, row_factory=dict_row)


def inicializar():
    with conectar() as db:
        db.execute((ROOT / 'schema.sql').read_text(encoding='utf-8'))


def texto(datos, campo, maximo=200, obligatorio=True):
    valor = datos.get(campo, '')
    if not isinstance(valor, str) or len(valor) > maximo or (obligatorio and not valor.strip()):
        raise ValueError(f'{campo}: texto válido de hasta {maximo} caracteres requerido')
    return valor.strip()


def cuerpo():
    datos = request.get_json()
    if not isinstance(datos, dict):
        raise ValueError('Se requiere un objeto JSON')
    return datos


def crear_api(hardening=True):
    api = Flask(__name__)
    api.config['MAX_CONTENT_LENGTH'] = 8192
    api.json.ensure_ascii = False

    @api.before_request
    def identificar():
        g.request_id = str(uuid.uuid4())

    @api.after_request
    def registrar(respuesta):
        respuesta.headers['X-Request-ID'] = g.get('request_id', '')
        respuesta.headers['Cache-Control'] = 'no-store'
        if hardening:
            respuesta.headers['X-Content-Type-Options'] = 'nosniff'
            respuesta.headers['X-Frame-Options'] = 'DENY'
            respuesta.headers['Referrer-Policy'] = 'no-referrer'
        try:
            with conectar() as db:
                db.execute('INSERT INTO solicitudes (request_id,origen,metodo,ruta,codigo) VALUES (%s,%s,%s,%s,%s)',
                           (g.request_id, request.remote_addr, request.method, request.path[:500], respuesta.status_code))
        except (psycopg.Error, OSError):
            api.logger.error('No se pudo registrar la solicitud %s', g.get('request_id'))
        return respuesta

    @api.errorhandler(ValueError)
    def dato_invalido(error):
        return jsonify(error=str(error)), 400

    @api.errorhandler(HTTPException)
    def error_http(error):
        return jsonify(error=error.name), error.code

    @api.errorhandler(psycopg.Error)
    def error_db(error):
        api.logger.error('Error de base de datos: %s', type(error).__name__)
        return jsonify(error='No se pudo completar la operación en PostgreSQL'), 503

    @api.get('/api/health')
    def salud():
        with conectar() as db:
            db.execute('SELECT 1')
        return jsonify(estado='ok', almacenamiento='PostgreSQL', modo='simulado')

    @api.get('/api/alertas')
    def listar():
        severidad = request.args.get('severidad', '')
        if severidad and severidad not in SEVERIDADES:
            raise ValueError('Severidad no válida')
        with conectar() as db:
            rows = db.execute("SELECT * FROM alertas WHERE (%s = '' OR severidad = %s) ORDER BY id DESC LIMIT 200", (severidad, severidad)).fetchall()
        return jsonify(rows)

    @api.post('/api/alertas')
    def recibir():
        datos = cuerpo()
        titulo = texto(datos, 'titulo')
        hostname = texto(datos, 'hostname', 100)
        severidad = texto(datos, 'severidad', 10)
        descripcion = texto(datos, 'descripcion', 1000, False)
        if severidad not in SEVERIDADES:
            raise ValueError('Severidad: baja, media, alta o critica')
        with conectar() as db:
            alerta = db.execute('INSERT INTO alertas (titulo,hostname,severidad,descripcion) VALUES (%s,%s,%s,%s) RETURNING *', (titulo, hostname, severidad, descripcion)).fetchone()
            db.execute("INSERT INTO acciones (alerta_id,tipo,nota,request_id) VALUES (%s,'recibir','Alerta ficticia recibida',%s)", (alerta['id'], g.request_id))
        return jsonify(alerta), 201

    @api.get('/api/alertas/<int:identificador>')
    def detalle(identificador):
        with conectar() as db:
            alerta = db.execute('SELECT * FROM alertas WHERE id=%s', (identificador,)).fetchone()
            if alerta is None:
                return jsonify(error='Alerta no encontrada'), 404
            alerta['acciones'] = db.execute('SELECT * FROM acciones WHERE alerta_id=%s ORDER BY id', (identificador,)).fetchall()
        return jsonify(alerta)

    @api.post('/api/alertas/<int:identificador>/acciones')
    def actuar(identificador):
        datos = cuerpo()
        tipo = texto(datos, 'tipo', 20)
        nota = texto(datos, 'nota', 1000, False)
        if tipo not in {'clasificar', 'enriquecer', 'escalar', 'cerrar'}:
            raise ValueError('Acción no válida')
        severidad = texto(datos, 'severidad', 10) if tipo == 'clasificar' else None
        if severidad is not None and severidad not in SEVERIDADES:
            raise ValueError('Severidad no válida')
        if tipo == 'enriquecer' and not nota:
            raise ValueError('Escriba una nota ficticia para enriquecer')
        with conectar() as db:
            alerta = db.execute('SELECT * FROM alertas WHERE id=%s FOR UPDATE', (identificador,)).fetchone()
            if alerta is None:
                return jsonify(error='Alerta no encontrada'), 404
            if tipo == 'clasificar':
                db.execute('UPDATE alertas SET severidad=%s WHERE id=%s', (severidad, identificador))
                nota = f'Severidad: {severidad}. {nota}'.strip()
            if tipo in {'escalar', 'cerrar'}:
                estado = 'escalada' if tipo == 'escalar' else 'cerrada'
                db.execute('UPDATE alertas SET estado=%s WHERE id=%s', (estado, identificador))
            accion = db.execute('INSERT INTO acciones (alerta_id,tipo,nota,request_id) VALUES (%s,%s,%s,%s) RETURNING *', (identificador, tipo, nota, g.request_id)).fetchone()
        return jsonify(accion), 201

    @api.get('/api/acciones')
    def acciones():
        with conectar() as db:
            rows = db.execute('SELECT * FROM acciones ORDER BY id DESC LIMIT 200').fetchall()
        return jsonify(rows)

    return api


if __name__ == '__main__':
    from waitress import serve
    inicializar()
    print('API REST: http://127.0.0.1:5000/api/health', flush=True)
    serve(crear_api(os.getenv('HARDENING', '1') == '1'), host=os.getenv('API_BIND', '127.0.0.1'), port=int(os.getenv('API_PORT', '5000')), ident='LabHTTP')
