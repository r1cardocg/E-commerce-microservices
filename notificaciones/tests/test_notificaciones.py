import pytest
import json
import os

os.environ['INTERNAL_KEY'] = 'ecommerce_internal_key_2026'

from app import app as flask_app

@pytest.fixture
def client():
    flask_app.config['TESTING'] = True
    with flask_app.test_client() as client:
        yield client

HEADERS = {
    'X-Internal-Key': 'ecommerce_internal_key_2026',
    'Content-Type':   'application/json'
}

class TestSeguridad:
    def test_sin_internal_key_retorna_403(self, client):
        r = client.get('/notificaciones')
        assert r.status_code == 403

    def test_key_incorrecta_retorna_403(self, client):
        r = client.get('/notificaciones', headers={'X-Internal-Key': 'incorrecta'})
        assert r.status_code == 403

class TestListar:
    def test_listar_notificaciones(self, client):
        r = client.get('/notificaciones', headers=HEADERS)
        assert r.status_code == 200
        data = json.loads(r.data)
        assert 'notificaciones' in data
        assert isinstance(data['notificaciones'], list)

    def test_listar_filtrando_por_usuario(self, client):
        r = client.get('/notificaciones?usuario_id=1', headers=HEADERS)
        assert r.status_code == 200

class TestCrear:
    def test_crear_notificacion_exitosa(self, client):
        payload = {
            'usuario_id': 1,
            'tipo':       'orden_confirmada',
            'mensaje':    'Tu orden fue confirmada'
        }
        r = client.post('/notificaciones', data=json.dumps(payload), headers=HEADERS)
        assert r.status_code == 201
        data = json.loads(r.data)
        assert data['tipo']    == 'orden_confirmada'
        assert data['leida']   == False
        assert '_id'           in data

    def test_crear_sin_usuario_id_retorna_422(self, client):
        payload = {'tipo': 'orden_confirmada', 'mensaje': 'Test'}
        r = client.post('/notificaciones', data=json.dumps(payload), headers=HEADERS)
        assert r.status_code == 422
        assert 'usuario_id' in json.loads(r.data)['errors']

    def test_crear_sin_tipo_retorna_422(self, client):
        payload = {'usuario_id': 1, 'mensaje': 'Test'}
        r = client.post('/notificaciones', data=json.dumps(payload), headers=HEADERS)
        assert r.status_code == 422
        assert 'tipo' in json.loads(r.data)['errors']

    def test_crear_sin_mensaje_retorna_422(self, client):
        payload = {'usuario_id': 1, 'tipo': 'orden_confirmada'}
        r = client.post('/notificaciones', data=json.dumps(payload), headers=HEADERS)
        assert r.status_code == 422
        assert 'mensaje' in json.loads(r.data)['errors']

    def test_crear_body_vacio_retorna_422(self, client):
        r = client.post('/notificaciones', data=json.dumps({}), headers=HEADERS)
        assert r.status_code == 422

class TestMarcarLeida:
    def test_marcar_leida_exitoso(self, client):
        # Crear primero
        payload = {
            'usuario_id': 1,
            'tipo':       'pago_completado',
            'mensaje':    'Tu pago fue procesado'
        }
        r = client.post('/notificaciones', data=json.dumps(payload), headers=HEADERS)
        nid = json.loads(r.data)['_id']

        # Marcar como leída
        r = client.patch(f'/notificaciones/{nid}/leer', headers=HEADERS)
        assert r.status_code == 200
        assert json.loads(r.data)['message'] == 'Notificación marcada como leída'

    def test_marcar_leida_no_existe_retorna_404(self, client):
        r = client.patch('/notificaciones/000000000000000000000000/leer', headers=HEADERS)
        assert r.status_code == 404

class TestEliminar:
    def test_eliminar_notificacion(self, client):
        payload = {
            'usuario_id': 1,
            'tipo':       'envio_realizado',
            'mensaje':    'Tu pedido fue enviado'
        }
        r = client.post('/notificaciones', data=json.dumps(payload), headers=HEADERS)
        nid = json.loads(r.data)['_id']

        r = client.delete(f'/notificaciones/{nid}', headers=HEADERS)
        assert r.status_code == 200
        assert json.loads(r.data)['message'] == 'Notificación eliminada'

    def test_eliminar_no_existe_retorna_404(self, client):
        r = client.delete('/notificaciones/000000000000000000000000', headers=HEADERS)
        assert r.status_code == 404