"""Lab 3: alertas ficticias de Falcon. HTTP, sin autenticación ni conexión externa."""
import json
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import urlsplit

alertas = []  # Se vacía cuando se reinicia el proceso.
LOG = Path(__file__).with_name("acciones.jsonl")


class API(BaseHTTPRequestHandler):
    def responder(self, codigo, datos):
        evento = {
            "hora_utc": datetime.now(timezone.utc).isoformat(),
            "origen": self.client_address[0], "metodo": self.command,
            "ruta": self.path, "estado_http": codigo,
        }
        with LOG.open("a", encoding="utf-8") as archivo:
            archivo.write(json.dumps(evento, ensure_ascii=False) + "\n")
        cuerpo = json.dumps(datos, ensure_ascii=False).encode("utf-8")
        self.send_response(codigo)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(cuerpo)))
        self.end_headers()
        self.wfile.write(cuerpo)

    def do_GET(self):
        ruta = urlsplit(self.path).path
        if ruta == "/":
            return self.responder(200, {
                "proyecto": "Automatización de incidentes de CrowdStrike Falcon",
                "modo": "LAB: solo alertas ficticias; sin integración real",
                "rutas": ["GET /alertas", "GET /alertas/1", "POST /alertas", "GET /acciones"],
            })
        if ruta == "/alertas":
            return self.responder(200, alertas)
        if ruta.startswith("/alertas/"):
            identificador = ruta.removeprefix("/alertas/")
            alerta = next((a for a in alertas if str(a["id"]) == identificador), None)
            return self.responder(200, alerta) if alerta else self.responder(404, {"error": "Alerta no encontrada"})
        if ruta == "/acciones":
            eventos = [json.loads(linea) for linea in LOG.read_text(encoding="utf-8").splitlines()] if LOG.exists() else []
            return self.responder(200, eventos)
        self.responder(404, {"error": "Ruta no encontrada"})

    def do_POST(self):
        if urlsplit(self.path).path != "/alertas":
            return self.responder(404, {"error": "Ruta no encontrada"})
        if self.headers.get_content_type() != "application/json":
            return self.responder(415, {"error": "Use Content-Type: application/json"})
        try:
            longitud = int(self.headers.get("Content-Length", "0"))
            if not 0 < longitud <= 4096:
                return self.responder(400, {"error": "Se requiere JSON de 1 a 4096 bytes"})
            datos = json.loads(self.rfile.read(longitud))
        except (ValueError, UnicodeDecodeError):
            return self.responder(400, {"error": "JSON o longitud no válidos"})
        campos = ("titulo", "hostname", "severidad")
        if not isinstance(datos, dict) or any(
            not isinstance(datos.get(c), str) or not datos[c].strip() or len(datos[c]) > 200
            for c in campos
        ):
            return self.responder(400, {"error": "titulo, hostname y severidad deben ser textos de 1 a 200 caracteres"})
        if datos["severidad"] not in ("baja", "media", "alta", "critica"):
            return self.responder(400, {"error": "Severidad permitida: baja, media, alta o critica"})
        alerta = {c: datos[c] for c in campos}
        alerta.update({
            "id": len(alertas) + 1,
            "fuente": "CrowdStrike Falcon - SIMULADO",
            "estado": "nueva",
            "hora_utc": datetime.now(timezone.utc).isoformat(),
        })
        alertas.append(alerta)
        self.responder(201, alerta)


if __name__ == "__main__":
    print("LAB local en http://127.0.0.1:5000 | Ctrl+C para detener")
    HTTPServer(("127.0.0.1", 5000), API).serve_forever()
