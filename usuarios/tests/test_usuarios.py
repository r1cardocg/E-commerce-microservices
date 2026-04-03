import pytest
import json
import os
import django

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
os.environ['INTERNAL_KEY'] = 'ecommerce_internal_key_2026'

django.setup()

from django.test import TestCase, Client
from usuarios.models import Usuario

HEADERS = {'HTTP_X_INTERNAL_KEY': 'ecommerce_internal_key_2026'}

class TestSeguridad(TestCase):
    def setUp(self):
        self.client = Client()

    def test_sin_internal_key_retorna_403(self):
        r = self.client.get('/usuarios')
        self.assertEqual(r.status_code, 403)

    def test_key_incorrecta_retorna_403(self):
        r = self.client.get('/usuarios', HTTP_X_INTERNAL_KEY='incorrecta')
        self.assertEqual(r.status_code, 403)


class TestListar(TestCase):
    def setUp(self):
        self.client = Client()

    def test_listar_usuarios_vacio(self):
        r = self.client.get('/usuarios', **HEADERS)
        self.assertEqual(r.status_code, 200)
        data = json.loads(r.content)
        self.assertIn('usuarios', data)
        self.assertEqual(data['usuarios'], [])


class TestCrear(TestCase):
    def setUp(self):
        self.client = Client()

    def test_crear_usuario_exitoso(self):
        payload = {
            'nombre':    'Ana García',
            'email':     'ana@example.com',
            'telefono':  '3001234567',
            'direccion': 'Calle 10'
        }
        r = self.client.post(
            '/usuarios',
            data=json.dumps(payload),
            content_type='application/json',
            **HEADERS
        )
        self.assertEqual(r.status_code, 201)
        data = json.loads(r.content)
        self.assertEqual(data['email'], 'ana@example.com')
        self.assertTrue(data['activo'])

    def test_crear_sin_nombre_retorna_422(self):
        payload = {'email': 'test@example.com'}
        r = self.client.post(
            '/usuarios',
            data=json.dumps(payload),
            content_type='application/json',
            **HEADERS
        )
        self.assertEqual(r.status_code, 422)
        data = json.loads(r.content)
        self.assertIn('nombre', data['errors'])

    def test_crear_sin_email_retorna_422(self):
        payload = {'nombre': 'Sin Email'}
        r = self.client.post(
            '/usuarios',
            data=json.dumps(payload),
            content_type='application/json',
            **HEADERS
        )
        self.assertEqual(r.status_code, 422)
        data = json.loads(r.content)
        self.assertIn('email', data['errors'])

    def test_crear_body_vacio_retorna_422(self):
        r = self.client.post(
            '/usuarios',
            data=json.dumps({}),
            content_type='application/json',
            **HEADERS
        )
        self.assertEqual(r.status_code, 422)

    def test_email_duplicado_retorna_422(self):
        Usuario.objects.create(nombre='Existente', email='dup@example.com')
        payload = {'nombre': 'Nuevo', 'email': 'dup@example.com'}
        r = self.client.post(
            '/usuarios',
            data=json.dumps(payload),
            content_type='application/json',
            **HEADERS
        )
        self.assertEqual(r.status_code, 422)


class TestObtener(TestCase):
    def setUp(self):
        self.client = Client()

    def test_obtener_usuario_existente(self):
        u = Usuario.objects.create(nombre='Carlos', email='carlos@example.com')
        r = self.client.get(f'/usuarios/{u.pk}', **HEADERS)
        self.assertEqual(r.status_code, 200)
        data = json.loads(r.content)
        self.assertEqual(data['email'], 'carlos@example.com')

    def test_obtener_no_existe_retorna_404(self):
        r = self.client.get('/usuarios/9999', **HEADERS)
        self.assertEqual(r.status_code, 404)


class TestActualizar(TestCase):
    def setUp(self):
        self.client = Client()

    def test_actualizar_usuario(self):
        u = Usuario.objects.create(nombre='Luis', email='luis@example.com')
        payload = {'nombre': 'Luis Updated', 'telefono': '3109999999'}
        r = self.client.put(
            f'/usuarios/{u.pk}',
            data=json.dumps(payload),
            content_type='application/json',
            **HEADERS
        )
        self.assertEqual(r.status_code, 200)
        data = json.loads(r.content)
        self.assertEqual(data['nombre'], 'Luis Updated')

    def test_actualizar_no_existe_retorna_404(self):
        r = self.client.put(
            '/usuarios/9999',
            data=json.dumps({'nombre': 'X'}),
            content_type='application/json',
            **HEADERS
        )
        self.assertEqual(r.status_code, 404)


class TestEliminar(TestCase):
    def setUp(self):
        self.client = Client()

    def test_desactivar_usuario(self):
        u = Usuario.objects.create(nombre='Maria', email='maria@example.com')
        r = self.client.delete(f'/usuarios/{u.pk}', **HEADERS)
        self.assertEqual(r.status_code, 200)
        u.refresh_from_db()
        self.assertFalse(u.activo)

    def test_desactivado_no_aparece_en_lista(self):
        u = Usuario.objects.create(nombre='Pedro', email='pedro@example.com')
        self.client.delete(f'/usuarios/{u.pk}', **HEADERS)
        r = self.client.get('/usuarios', **HEADERS)
        emails = [x['email'] for x in json.loads(r.content)['usuarios']]
        self.assertNotIn('pedro@example.com', emails)

    def test_eliminar_no_existe_retorna_404(self):
        r = self.client.delete('/usuarios/9999', **HEADERS)
        self.assertEqual(r.status_code, 404)