"""Web local: archivos estáticos y proxy REST hacia la API separada."""
import os
import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from flask import Flask, request, Response, send_from_directory
from waitress import serve

ROOT = Path(__file__).resolve().parent
web = Flask(__name__)
web.config['MAX_CONTENT_LENGTH'] = 8192
BACKEND = os.getenv('API_URL', 'http://127.0.0.1:5000')

@web.get('/')
def inicio():
    return send_from_directory(ROOT, 'index.html')

@web.get('/<name>')
def archivo(name):
    if name not in {'styles.css', 'web.js', 'public-inventory.txt'}:
        return {'error': 'Recurso no encontrado'}, 404
    return send_from_directory(ROOT, name)

@web.route('/api/<path:ruta>', methods=['GET', 'POST'])
def api(ruta):
    req = Request(BACKEND + request.full_path.rstrip('?'), data=request.get_data() if request.method == 'POST' else None,
                  method=request.method, headers={'Content-Type': request.content_type or 'application/json'})
    try:
        upstream = urlopen(req, timeout=10)
    except HTTPError as error:
        upstream = error
    except URLError:
        return {'error': 'API no disponible. Comprueba que está encendida.'}, 503
    with upstream:
        response = Response(upstream.read(), status=upstream.code, content_type=upstream.headers.get('Content-Type'))
        response.headers['X-Request-ID'] = upstream.headers.get('X-Request-ID', '')
        return response

@web.after_request
def controles(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['Referrer-Policy'] = 'no-referrer'
    response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self'; style-src 'self'; frame-ancestors 'none'; base-uri 'none'"
    response.headers['Cache-Control'] = 'no-store'
    print(json.dumps({
        'utc': datetime.now(timezone.utc).isoformat(),
        'origen': request.remote_addr,
        'metodo': request.method,
        'ruta': request.path[:500],
        'codigo': response.status_code,
        'bytes': response.content_length,
        'user_agent': request.headers.get('User-Agent', '')[:200],
    }, ensure_ascii=False), flush=True)
    return response

if __name__ == '__main__':
    port = int(os.getenv('WEB_PORT', '80'))
    print(f'Aplicación web: http://127.0.0.1:{port}', flush=True)
    serve(web, host='127.0.0.1', port=port, ident='LabHTTP')
