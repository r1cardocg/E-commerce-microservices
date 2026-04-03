# Sistema E-commerce con Microservicios

**Ingeniería de Software II — Entrega #1**
**Estudiante:** Ricardo Calderon Garcia

---

## Descripción General

Sistema de e-commerce distribuido basado en arquitectura de microservicios. Un API Gateway central (Laravel) autentica usuarios mediante JWT y enruta las solicitudes a microservicios especializados. Todas las peticiones externas pasan obligatoriamente por el Gateway.

---

## Diagrama de Arquitectura

```
+---------------------------------------------------------------------+
|                      CLIENTE / THUNDER CLIENT                       |
|                 (HTTP Requests + JWT Bearer Token)                  |
+-----------------------------+---------------------------------------+
                              |  HTTP + JWT
                              v
+---------------------------------------------------------------------+
|                     API GATEWAY (Laravel)                           |
|                     PHP 8.3 -- Puerto 8000                          |
|                     Base de datos: MySQL                            |
|                                                                     |
|   +-------------------------------------------------------------+   |
|   |  Autenticacion JWT (tymon/jwt-auth)                         |   |
|   |  POST /api/register   -> Registrar usuario                  |   |
|   |  POST /api/login      -> Obtener token JWT                  |   |
|   |  POST /api/logout     -> Invalidar token                    |   |
|   |  POST /api/forgot-password -> Recuperacion                  |   |
|   |  POST /api/reset-password  -> Resetear contrasena           |   |
|   +-------------------------------------------------------------+   |
|                                                                     |
|   +-------------------------------------------------------------+   |
|   |  Proxy / Router interno                                     |   |
|   |  Agrega X-Internal-Key en cada peticion a microservicios    |   |
|   |  Redirige segun ruta: /usuarios, /productos, etc.           |   |
|   +-------------------------------------------------------------+   |
+--+----------+-------------+-----------+-----------+----------------+
   |          |             |           |           |
   v          v             v           v           v
+--------+ +--------+ +----------+ +--------+ +---------------+
|USUARIOS| |PRODUCTS| | ORDENES  | | PAGOS  | |NOTIFICACIONES |
|Django  | | Flask  | | Express  | |Laravel | |    Flask      |
| :8001  | | :8002  | |  :8003   | | :8004  | |    :8005      |
+---+----+ +---+----+ +----+-----+ +---+----+ +------+--------+
    |           |          |           |              |
    v           v          v           v              v
+--------+ +--------+ +----------+ +--------+ +---------------+
|Postgres| | MySQL  | | MongoDB  | | MySQL  | |   MongoDB     |
+--------+ +--------+ +----------+ +--------+ +---------------+
```

---

## Seguridad

### Capa 1 - Cliente al Gateway (JWT)

| Elemento    | Detalle                                        |
|-------------|------------------------------------------------|
| Algoritmo   | HS256 (HMAC SHA-256)                           |
| Header      | Authorization: Bearer token                    |
| Expiracion  | 60 minutos (configurable en JWT_TTL)           |
| Libreria    | tymon/jwt-auth para Laravel                    |

### Capa 2 - Gateway a Microservicios (X-Internal-Key)

| Elemento    | Detalle                                        |
|-------------|------------------------------------------------|
| Mecanismo   | Header HTTP personalizado                      |
| Header      | X-Internal-Key: clave_secreta                  |
| Rechazo     | Microservicio devuelve 403 Forbidden           |

Los microservicios no son accesibles desde el exterior sin la clave interna.

---

## Estructura del Proyecto

```
E-commerce-microservices/
|
+-- Gateway/                          # Laravel -- Puerto 8000
|   +-- app/
|   |   +-- Http/
|   |   |   +-- Controllers/
|   |   |   |   +-- AuthController.php
|   |   |   |   +-- UsuarioController.php
|   |   |   |   +-- ProductoController.php
|   |   |   |   +-- OrdenController.php
|   |   |   |   +-- PagoController.php
|   |   |   |   +-- NotificacionController.php
|   |   |   +-- Middleware/
|   |   |       +-- JwtMiddleware.php
|   |   +-- Services/
|   |       +-- MicroserviceProxy.php
|   +-- routes/api.php
|   +-- tests/Feature/AuthTest.php
|   +-- .env
|
+-- usuarios/                         # Django -- Puerto 8001
|   +-- usuarios/
|   |   +-- models.py
|   |   +-- views.py
|   |   +-- middleware.py
|   |   +-- urls.py
|   +-- tests/test_usuarios.py
|   +-- settings.py
|   +-- manage.py
|   +-- .env
|
+-- productos/                        # Flask -- Puerto 8002
|   +-- app.py
|   +-- config.py
|   +-- models.py
|   +-- routes.py
|   +-- middleware.py
|   +-- tests/test_productos.py
|   +-- .env
|
+-- ordenes/                          # Express -- Puerto 8003
|   +-- server.js
|   +-- src/
|   |   +-- app.js
|   |   +-- routes/ordenes.js
|   |   +-- middlewares/internalKey.js
|   |   +-- models/Orden.js
|   +-- tests/ordenes.test.js
|   +-- package.json
|   +-- .env
|
+-- pagos/                            # Laravel -- Puerto 8004
|   +-- app/
|   |   +-- Http/Controllers/PagoController.php
|   |   +-- Http/Middleware/InternalKeyMiddleware.php
|   |   +-- Models/Pago.php
|   +-- routes/api.php
|   +-- tests/Feature/PagoTest.php
|   +-- .env
|
+-- notificaciones/                   # Flask -- Puerto 8005
|   +-- app.py
|   +-- routes.py
|   +-- middleware.py
|   +-- database.py
|   +-- tests/test_notificaciones.py
|   +-- .env
|
+-- tests/
|   +-- performance/
|   |   +-- locustfile.py
|   +-- security/
|       +-- security_test.py
|
+-- .github/workflows/ci.yml
+-- docker-compose.yml
+-- .gitignore
+-- README.md
```

---

## Tecnologias

| Servicio        | Framework     | Base de datos | Puerto |
|-----------------|---------------|---------------|--------|
| API Gateway     | Laravel 12    | MySQL         | 8000   |
| Usuarios        | Django 5      | PostgreSQL    | 8001   |
| Productos       | Flask 3       | MySQL         | 8002   |
| Ordenes         | Express 4     | MongoDB       | 8003   |
| Pagos           | Laravel 12    | MySQL         | 8004   |
| Notificaciones  | Flask 3       | MongoDB       | 8005   |

---

## Prerequisitos

| Herramienta  | Version minima | Uso                          |
|--------------|----------------|------------------------------|
| PHP          | 8.3            | Gateway y Pagos              |
| Composer     | 2.x            | Dependencias PHP             |
| Python       | 3.11           | Usuarios, Productos, Notif.  |
| Node.js      | 18             | Ordenes                      |
| MySQL        | 8.0            | Gateway, Productos, Pagos    |
| PostgreSQL   | 17             | Usuarios                     |
| MongoDB      | 7              | Ordenes, Notificaciones      |
| Git          | 2.x            | Control de versiones         |
| Locust       | 2.x            | Pruebas de rendimiento       |

---

## Instalacion y Despliegue

### 1. Clonar el repositorio

```bash
git clone https://github.com/TU_USUARIO/E-commerce-microservices.git
cd E-commerce-microservices
```

---

### 2. API Gateway - Laravel (Puerto 8000)

```bash
cd Gateway
composer install
```

Configurar .env:
```env
APP_NAME=EcommerceGateway
APP_URL=http://localhost:8000

DB_CONNECTION=mysql
DB_HOST=127.0.0.1
DB_PORT=3306
DB_DATABASE=gateway_db
DB_USERNAME=root
DB_PASSWORD=

JWT_SECRET=
JWT_TTL=60

USUARIOS_URL=http://localhost:8001
PRODUCTOS_URL=http://localhost:8002
ORDENES_URL=http://localhost:8003
PAGOS_URL=http://localhost:8004
NOTIFICACIONES_URL=http://localhost:8005

INTERNAL_KEY=EcommerceSecretKey
```

```bash
php artisan key:generate
php artisan jwt:secret
php artisan migrate
php artisan serve --port=8000
```

Verificar: GET http://localhost:8000/up debe responder 200 OK

---

### 3. Usuarios - Django (Puerto 8001)

```bash
cd usuarios
python -m venv venv
source venv/Scripts/activate    # Windows
pip install -r requirements.txt
```

Crear base de datos en PostgreSQL:
```sql
CREATE DATABASE usuarios_db;
```

Configurar .env:
```env
DJANGO_SECRET_KEY=django-insecure-change-this
DEBUG=True
DB_NAME=usuarios_db
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=127.0.0.1
DB_PORT=5432
INTERNAL_KEY=EcommerceSecretKey
```

```bash
python manage.py migrate
python manage.py runserver 0.0.0.0:8001
```

Verificar: GET http://localhost:8001/usuarios con X-Internal-Key: EcommerceSecretKey debe responder 200

---

### 4. Productos - Flask (Puerto 8002)

```bash
cd productos
python -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt
```

Crear base de datos en MySQL:
```sql
CREATE DATABASE productos_db;
```

Configurar .env:
```env
PORT=8002
DB_USER=root
DB_PASSWORD=
DB_HOST=127.0.0.1
DB_PORT=3306
DB_NAME=productos_db
INTERNAL_KEY=EcommerceSecretKey
```

```bash
python app.py
```

Verificar: GET http://localhost:8002/productos con X-Internal-Key debe responder 200

---

### 5. Ordenes - Express (Puerto 8003)

```bash
cd ordenes
npm install
```

Configurar .env:
```env
PORT=8003
MONGO_URI=mongodb://127.0.0.1:27017/ordenes_db
INTERNAL_KEY=EcommerceSecretKey
```

```bash
npm start
```

Verificar: la terminal debe mostrar "Microservicio Ordenes corriendo en puerto 8003" y "MongoDB conectado"

---

### 6. Pagos - Laravel (Puerto 8004)

```bash
cd pagos
composer install
```

Crear base de datos en MySQL:
```sql
CREATE DATABASE pagos_db;
```

Configurar .env:
```env
APP_NAME=PagosService
APP_URL=http://localhost:8004

DB_CONNECTION=mysql
DB_HOST=127.0.0.1
DB_PORT=3306
DB_DATABASE=pagos_db
DB_USERNAME=root
DB_PASSWORD=

INTERNAL_KEY=EcommerceSecretKey
```

```bash
php artisan key:generate
php artisan migrate
php artisan serve --port=8004
```

Verificar: GET http://localhost:8004/api/pagos con X-Internal-Key debe responder 200

---

### 7. Notificaciones - Flask (Puerto 8005)

```bash
cd notificaciones
python -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt
```

Configurar .env:
```env
PORT=8005
MONGO_URI=mongodb://127.0.0.1:27017/
MONGO_DB=notificaciones_db
INTERNAL_KEY=EcommerceSecretKey
```

```bash
python app.py
```

Verificar: GET http://localhost:8005/notificaciones con X-Internal-Key debe responder 200

---

## Verificacion del Sistema Completo

Con todos los servicios corriendo, ejecuta este flujo en Thunder Client:

```
1. Registrar usuario
POST http://localhost:8000/api/register
Body: {"name":"Test","email":"test@example.com","password":"password123","password_confirmation":"password123"}

2. Login - copiar el token de la respuesta
POST http://localhost:8000/api/login
Body: {"email":"test@example.com","password":"password123"}

3. Crear producto (usar token del paso 2)
POST http://localhost:8000/api/productos
Authorization: Bearer <token>
Body: {"nombre":"Laptop Dell","precio":1200,"stock":50,"categoria":"Tecnologia"}

4. Crear orden
POST http://localhost:8000/api/ordenes
Authorization: Bearer <token>
Body: {"usuario_id":1,"productos":[{"producto_id":"1","nombre":"Laptop Dell","cantidad":1,"precio_unitario":1200}]}

5. Procesar pago
POST http://localhost:8000/api/pagos
Authorization: Bearer <token>
Body: {"usuario_id":1,"orden_id":"<_id de la orden>","monto":1200,"metodo_pago":"tarjeta_credito"}

6. Crear notificacion
POST http://localhost:8000/api/notificaciones
Authorization: Bearer <token>
Body: {"usuario_id":1,"tipo":"orden_confirmada","mensaje":"Tu orden fue confirmada"}
```

---

## Endpoints Documentados

Todas las rutas protegidas requieren: Authorization: Bearer token
Los microservicios directamente requieren: X-Internal-Key: EcommerceSecretKey

### API Gateway - localhost:8000

#### Rutas Publicas

| Metodo | Endpoint               | Descripcion                   |
|--------|------------------------|-------------------------------|
| POST   | /api/register          | Registrar nuevo usuario       |
| POST   | /api/login             | Iniciar sesion - retorna JWT  |
| POST   | /api/forgot-password   | Enviar enlace de recuperacion |
| POST   | /api/reset-password    | Resetear contrasena con token |

#### Rutas Protegidas

| Metodo | Endpoint                      | Proxy destino     | Descripcion              |
|--------|-------------------------------|-------------------|--------------------------|
| POST   | /api/logout                   | --                | Cerrar sesion            |
| GET    | /api/me                       | --                | Datos del usuario auth   |
| GET    | /api/usuarios                 | Django :8001      | Listar usuarios          |
| GET    | /api/usuarios/{id}            | Django :8001      | Obtener usuario          |
| PUT    | /api/usuarios/{id}            | Django :8001      | Actualizar usuario       |
| DELETE | /api/usuarios/{id}            | Django :8001      | Desactivar usuario       |
| GET    | /api/productos                | Flask :8002       | Listar productos         |
| POST   | /api/productos                | Flask :8002       | Crear producto           |
| GET    | /api/productos/{id}           | Flask :8002       | Obtener producto         |
| PUT    | /api/productos/{id}           | Flask :8002       | Actualizar producto      |
| DELETE | /api/productos/{id}           | Flask :8002       | Eliminar producto        |
| GET    | /api/ordenes                  | Express :8003     | Listar ordenes           |
| POST   | /api/ordenes                  | Express :8003     | Crear orden              |
| GET    | /api/ordenes/{id}             | Express :8003     | Obtener orden            |
| PUT    | /api/ordenes/{id}             | Express :8003     | Actualizar orden         |
| DELETE | /api/ordenes/{id}             | Express :8003     | Cancelar orden           |
| GET    | /api/pagos                    | Laravel :8004     | Listar pagos             |
| POST   | /api/pagos                    | Laravel :8004     | Procesar pago            |
| GET    | /api/pagos/{id}               | Laravel :8004     | Obtener pago             |
| GET    | /api/notificaciones           | Flask :8005       | Listar notificaciones    |
| POST   | /api/notificaciones           | Flask :8005       | Crear notificacion       |
| PATCH  | /api/notificaciones/{id}/leer | Flask :8005       | Marcar como leida        |
| DELETE | /api/notificaciones/{id}      | Flask :8005       | Eliminar notificacion    |

---

### Usuarios - localhost:8001

| Metodo | Endpoint            | Descripcion        | Validaciones                  |
|--------|---------------------|--------------------|-------------------------------|
| GET    | /usuarios           | Listar activos     | --                            |
| POST   | /usuarios           | Crear usuario      | nombre y email requeridos     |
| GET    | /usuarios/{id}      | Obtener usuario    | 404 si no existe              |
| PUT    | /usuarios/{id}      | Actualizar usuario | --                            |
| DELETE | /usuarios/{id}      | Soft delete        | Cambia activo=False           |

---

### Productos - localhost:8002

| Metodo | Endpoint            | Descripcion        | Validaciones                         |
|--------|---------------------|--------------------|--------------------------------------|
| GET    | /productos          | Listar productos   | Solo productos activos               |
| POST   | /productos          | Crear producto     | nombre y precio requeridos, precio>=0|
| GET    | /productos/{id}     | Obtener producto   | 404 si no existe                     |
| PUT    | /productos/{id}     | Actualizar         | --                                   |
| DELETE | /productos/{id}     | Soft delete        | Cambia activo=False                  |

---

### Ordenes - localhost:8003

| Metodo | Endpoint            | Descripcion        | Validaciones                          |
|--------|---------------------|--------------------|---------------------------------------|
| GET    | /ordenes            | Listar ordenes     | Query param: ?usuario_id=1            |
| POST   | /ordenes            | Crear orden        | usuario_id y productos[] requeridos   |
| GET    | /ordenes/{id}       | Obtener orden      | 404 si no existe                      |
| PUT    | /ordenes/{id}       | Actualizar estado  | estado debe ser valor valido          |
| DELETE | /ordenes/{id}       | Cancelar orden     | Cambia estado a "cancelada"           |

Estados validos: pendiente, confirmada, enviada, entregada, cancelada

---

### Pagos - localhost:8004

| Metodo | Endpoint        | Descripcion      | Validaciones                                      |
|--------|-----------------|------------------|---------------------------------------------------|
| GET    | /api/pagos      | Listar pagos     | Query param: ?usuario_id=1                        |
| POST   | /api/pagos      | Procesar pago    | usuario_id, orden_id, monto>0, metodo_pago valido |
| GET    | /api/pagos/{id} | Obtener pago     | 404 si no existe                                  |

Metodos validos: tarjeta_credito, tarjeta_debito, paypal, transferencia

---

### Notificaciones - localhost:8005

| Metodo | Endpoint                        | Descripcion           | Validaciones                         |
|--------|---------------------------------|-----------------------|--------------------------------------|
| GET    | /notificaciones                 | Listar notificaciones | Query param: ?usuario_id=1           |
| POST   | /notificaciones                 | Crear notificacion    | usuario_id, tipo, mensaje requeridos |
| PATCH  | /notificaciones/{id}/leer       | Marcar como leida     | 404 si no existe                     |
| DELETE | /notificaciones/{id}            | Eliminar              | 404 si no existe                     |

---

## Pruebas

### Unitarias

```bash
# Gateway (Laravel)
cd Gateway && php artisan test

# Usuarios (Django)
cd usuarios
source venv/Scripts/activate
python -m pytest tests/test_usuarios.py -v

# Productos (Flask)
cd productos
source venv/Scripts/activate
python -m pytest tests/test_productos.py -v

# Ordenes (Express)
cd ordenes && npm test

# Pagos (Laravel)
cd pagos && php artisan test

# Notificaciones (Flask)
cd notificaciones
source venv/Scripts/activate
python -m pytest tests/test_notificaciones.py -v
```

### Rendimiento (Locust)

```bash
pip install locust

# Con interfaz web
cd tests/performance
locust -f locustfile.py
# Abrir http://localhost:8089

# Sin interfaz
locust -f locustfile.py --headless -u 50 -r 5 --run-time 2m
```

Incluye pruebas de capacidad (10 a 100 usuarios), carga sostenida (20 usuarios) y estres (200 usuarios).

### Seguridad

```bash
pip install requests pytest
pytest tests/security/security_test.py -v
```

---

## Bases de Datos

| Servicio        | Motor      | Base de datos       |
|-----------------|------------|---------------------|
| Gateway         | MySQL      | gateway_db          |
| Usuarios        | PostgreSQL | usuarios_db         |
| Productos       | MySQL      | productos_db        |
| Ordenes         | MongoDB    | ordenes_db          |
| Pagos           | MySQL      | pagos_db            |
| Notificaciones  | MongoDB    | notificaciones_db   |

---

## Variables de Entorno

| Variable             | Servicio       | Descripcion                         |
|----------------------|----------------|-------------------------------------|
| JWT_SECRET           | Gateway        | Clave para firmar tokens JWT        |
| JWT_TTL              | Gateway        | Tiempo de vida del token (minutos)  |
| INTERNAL_KEY         | Todos          | Clave compartida gateway-servicios  |
| USUARIOS_URL         | Gateway        | URL del microservicio Django        |
| PRODUCTOS_URL        | Gateway        | URL del microservicio Flask         |
| ORDENES_URL          | Gateway        | URL del microservicio Express       |
| PAGOS_URL            | Gateway        | URL del microservicio Laravel pagos |
| NOTIFICACIONES_URL   | Gateway        | URL del microservicio Flask notif.  |
| MONGO_URI            | Ordenes/Notif. | URI de conexion a MongoDB           |