"""Peticiones inocuas solo contra localhost; crea una alerta ficticia por etapa."""
import json
import os
import sys
import urllib.request
import urllib.error
from pathlib import Path

etapa, salida = sys.argv[1:]
assert etapa in {'antes', 'despues'}
url = 'http://127.0.0.1:5000'
payload = {'titulo': 'Validacion Lab 5', 'hostname': 'EQUIPO-FICTICIO', 'severidad': 'baja'}

def pedir(path, data=None, token=None):
    headers = {'Content-Type': 'application/json'}
    if token:
        headers['X-Lab-Token'] = token
    req = urllib.request.Request(url + path, data=json.dumps(data).encode() if data else None, headers=headers)
    try:
        respuesta = urllib.request.urlopen(req, timeout=10)
    except urllib.error.HTTPError as error:
        respuesta = error
    with respuesta:
        return {'codigo': respuesta.status, 'cuerpo': json.load(respuesta),
                'csp': respuesta.headers.get('Content-Security-Policy')}

resultados = {'etapa': etapa, 'destino': url, 'datos': 'solo ficticios'}
resultados['salud'] = pedir('/api/health')
resultados['escritura_sin_token'] = pedir('/api/alertas', payload)
if etapa == 'despues':
    resultados['escritura_token_incorrecto'] = pedir('/api/alertas', payload, 'incorrecto')
    resultados['escritura_autorizada'] = pedir('/api/alertas', payload, os.environ['LAB_API_TOKEN'])
Path(salida).write_text(json.dumps(resultados, indent=2, ensure_ascii=False), encoding='utf-8')
assert resultados['salud']['codigo'] == 200
assert resultados['escritura_sin_token']['codigo'] == (201 if etapa == 'antes' else 401)
if etapa == 'despues':
    assert resultados['escritura_token_incorrecto']['codigo'] == 401
    assert resultados['escritura_autorizada']['codigo'] == 201
    assert resultados['salud']['csp'] is not None
print(json.dumps(resultados, indent=2, ensure_ascii=False))
