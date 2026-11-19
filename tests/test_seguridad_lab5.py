"""Regresion del control de escritura, sin depender de PostgreSQL."""
import os
import unittest
from unittest.mock import patch, MagicMock
import app

class SeguridadEscritura(unittest.TestCase):
    def setUp(self):
        self.environment = patch.dict(os.environ, {'LAB_API_TOKEN': 'token-ficticio-solo-pruebas'})
        self.environment.start()
        self.database = patch('app.conectar')
        self.connection = self.database.start()
        self.db = self.connection.return_value.__enter__.return_value
        self.db.execute.return_value.fetchone.return_value = {'id': 1, 'titulo': 'Prueba ficticia'}
        self.client = app.crear_api().test_client()
        self.payload = {'titulo': 'Prueba ficticia', 'hostname': 'EQUIPO-LAB', 'severidad': 'baja'}

    def tearDown(self):
        self.database.stop()
        self.environment.stop()

    def test_sin_token_no_inserta_alerta(self):
        response = self.client.post('/api/alertas', json=self.payload)
        self.assertEqual(response.status_code, 401)
        consultas = [str(c.args[0]) for c in self.db.execute.call_args_list]
        self.assertFalse(any('INSERT INTO alertas' in q for q in consultas))

    def test_token_incorrecto_y_unicode_se_rechazan(self):
        for token in ['incorrecto', 'prueba-ñ']:
            self.assertEqual(self.client.post('/api/alertas', json=self.payload,
                             headers={'X-Lab-Token': token}).status_code, 401)

    def test_token_valido_permite_registrar(self):
        self.assertEqual(self.client.post('/api/alertas', json=self.payload,
                         headers={'X-Lab-Token': 'token-ficticio-solo-pruebas'}).status_code, 201)

    def test_acciones_sin_token_se_rechazan(self):
        self.assertEqual(self.client.post('/api/alertas/1/acciones',
                         json={'tipo': 'cerrar'}).status_code, 401)

    def test_sin_configuracion_falla_cerrado(self):
        with patch.dict(os.environ, {'LAB_API_TOKEN': ''}):
            self.assertEqual(self.client.post('/api/alertas', json=self.payload).status_code, 503)

    def test_hardening_desactivado_no_quita_autenticacion(self):
        client = app.crear_api(False).test_client()
        self.assertEqual(client.post('/api/alertas', json=self.payload).status_code, 401)

    def test_lectura_y_salud_siguen_publicas(self):
        self.db.execute.return_value.fetchall.return_value = []
        self.assertEqual(self.client.get('/api/alertas').status_code, 200)
        self.assertEqual(self.client.get('/api/health').status_code, 200)

    def test_error_tambien_tiene_csp(self):
        response = self.client.get('/api/no-existe')
        self.assertEqual(response.status_code, 404)
        self.assertIn("default-src 'none'", response.headers['Content-Security-Policy'])

if __name__ == '__main__':
    unittest.main()
