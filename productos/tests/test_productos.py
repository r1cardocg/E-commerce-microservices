import pytest
import json
import os

os.environ['INTERNAL_KEY'] = 'ecommerce_internal_key_2026'

from app import create_app
from extensions import db as _db

@pytest.fixture(scope='session')
def app():
    app = create_app()
    app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
    })
    return app

@pytest.fixture(scope='function')
def client(app):
    with app.app_context():
        _db.create_all()
        yield app.test_client()
        _db.session.remove()
        _db.drop_all()

HEADERS = {
    'X-Internal-Key': 'ecommerce_internal_key_2026',
    'Content-Type':   'application/json'
}

class TestSeguridad:
    def test_sin_internal_key_retorna_403(self, client):
        r = client.get('/productos')
        assert r.status_code == 403

    def test_key_incorrecta_retorna_403(self, client):
        r = client.get('/productos', headers={'X-Internal-Key': 'incorrecta'})
        assert r.status_code == 403

class TestListar:
    def test_listar_productos_vacio(self, client):
        r = client.get('/productos', headers=HEADERS)
        assert r.status_code == 200
        assert json.loads(r.data)['productos'] == []

class TestCrear:
    def test_crear_producto_exitoso(self, client):
        payload = {'nombre': 'Laptop Dell', 'precio': 1200.00, 'stock': 50}
        r = client.post('/productos', data=json.dumps(payload), headers=HEADERS)
        assert r.status_code == 201
        data = json.loads(r.data)
        assert data['nombre'] == 'Laptop Dell'
        assert data['activo'] == True

    def test_crear_sin_nombre_retorna_422(self, client):
        r = client.post('/productos', data=json.dumps({'precio': 100.0}), headers=HEADERS)
        assert r.status_code == 422
        assert 'nombre' in json.loads(r.data)['errors']

    def test_crear_sin_precio_retorna_422(self, client):
        r = client.post('/productos', data=json.dumps({'nombre': 'X'}), headers=HEADERS)
        assert r.status_code == 422
        assert 'precio' in json.loads(r.data)['errors']

    def test_crear_precio_negativo_retorna_422(self, client):
        r = client.post('/productos', data=json.dumps({'nombre': 'X', 'precio': -5}), headers=HEADERS)
        assert r.status_code == 422

    def test_crear_body_vacio_retorna_422(self, client):
        r = client.post('/productos', data=json.dumps({}), headers=HEADERS)
        assert r.status_code == 422

class TestObtener:
    def test_obtener_producto_existente(self, client):
        r = client.post('/productos', data=json.dumps({'nombre': 'Mouse', 'precio': 25.0}), headers=HEADERS)
        pid = json.loads(r.data)['id']
        r = client.get(f'/productos/{pid}', headers=HEADERS)
        assert r.status_code == 200

    def test_obtener_no_existe_retorna_404(self, client):
        r = client.get('/productos/9999', headers=HEADERS)
        assert r.status_code == 404

class TestActualizar:
    def test_actualizar_producto(self, client):
        r = client.post('/productos', data=json.dumps({'nombre': 'Teclado', 'precio': 45.0}), headers=HEADERS)
        pid = json.loads(r.data)['id']
        r = client.put(f'/productos/{pid}', data=json.dumps({'precio': 55.0}), headers=HEADERS)
        assert r.status_code == 200
        assert json.loads(r.data)['precio'] == 55.0

    def test_actualizar_no_existe_retorna_404(self, client):
        r = client.put('/productos/9999', data=json.dumps({'precio': 10}), headers=HEADERS)
        assert r.status_code == 404

class TestEliminar:
    def test_eliminar_producto(self, client):
        r = client.post('/productos', data=json.dumps({'nombre': 'Monitor', 'precio': 300.0}), headers=HEADERS)
        pid = json.loads(r.data)['id']
        r = client.delete(f'/productos/{pid}', headers=HEADERS)
        assert r.status_code == 200

    def test_eliminado_no_aparece_en_lista(self, client):
        r = client.post('/productos', data=json.dumps({'nombre': 'Audífonos', 'precio': 80.0}), headers=HEADERS)
        pid = json.loads(r.data)['id']
        client.delete(f'/productos/{pid}', headers=HEADERS)
        r = client.get('/productos', headers=HEADERS)
        ids = [p['id'] for p in json.loads(r.data)['productos']]
        assert pid not in ids