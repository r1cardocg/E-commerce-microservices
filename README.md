# Sistema E-commerce con Microservicios

**Ingeniería de Software II — Entrega #1**  
Ricardo Calderon Garcia  

---

## Descripción General

Sistema de e-commerce distribuido basado en arquitectura de microservicios. Un **API Gateway** central (Laravel) autentica usuarios mediante JWT y enruta las solicitudes a microservicios especializados.

---

## Diagrama de Arquitectura

```
┌─────────────────────────────────────────────────────────────────────┐
│                      CLIENTE / THUNDER CLIENT                       │
│                 (HTTP Requests + JWT Bearer Token)                  │
└─────────────────────────────┬───────────────────────────────────────┘
                              │  HTTP + JWT
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                     API GATEWAY (Laravel)                           │
│                     PHP 8.3 — Puerto 8000                           │
│                     Base de datos: MySQL                            │
│                                                                     │
│   ┌─────────────────────────────────────────────────────────────┐   │
│   │  Autenticación JWT (tymon/jwt-auth)                         │   │
│   │  • Genera tokens en /api/login                              │   │
│   │  • Valida tokens en rutas protegidas                        │   │
│   │  • Invalida tokens en /api/logout                           │   │
│   │  • Recuperación de contraseña /api/forgot-password          │   │
│   └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│   ┌─────────────────────────────────────────────────────────────┐   │
│   │  Proxy / Router interno                                     │   │
│   │  • Agrega header: X-Internal-Key: {clave_secreta}           │   │
│   │  • Redirige peticiones a microservicios                     │   │
│   └─────────────────────────────────────────────────────────────┘   │
└───┬──────────┬──────────────┬─────────────┬───────────┬─────────────┘
    │          │              │             │           │
    ▼          ▼              ▼             ▼           ▼
┌────────┐ ┌────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────┐
│USUARIOS│ │PRODUCTOS│ │ ÓRDENES  │ │  PAGOS   │ │NOTIFICACIONES│
│Django  │ │ Flask  │ │ Express  │ │ Laravel  │ │    Flask     │
│:8001   │ │ :8002  │ │  :8003   │ │  :8004   │ │    :8005     │
└───┬────┘ └───┬────┘ └────┬─────┘ └────┬─────┘ └──────┬───────┘
    │          │           │            │              │
    ▼          ▼           ▼            ▼              ▼
┌────────┐ ┌────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────┐
│Postgres│ │ MySQL  │ │ MongoDB  │ │  MySQL   │ │   MongoDB    │
└────────┘ └────────┘ └──────────┘ └──────────┘ └──────────────┘
```

---

## Tecnologías

| Servicio        | Framework      | Base de datos | Puerto |
|-----------------|----------------|---------------|--------|
| API Gateway     | Laravel 12     | MySQL         | 8000   |
| Usuarios        | Django 5       | PostgreSQL    | 8001   |
| Productos       | Flask 3        | MySQL         | 8002   |
| Órdenes         | Express 4      | MongoDB       | 8003   |
| Pagos           | Laravel 12     | MySQL         | 8004   |
| Notificaciones  | Flask 3        | MongoDB       | 8005   |

---

## Seguridad

### Capa 1: Cliente → Gateway (JWT)

| Elemento    | Detalle                                     |
|-------------|---------------------------------------------|
| Algoritmo   | HS256 (HMAC SHA-256)                        |
| Header      | `Authorization: Bearer <token>`             |
| Expiración  | 60 minutos (configurable)                   |
| Librería    | `tymon/jwt-auth` para Laravel               |

### Capa 2: Gateway → Microservicios (X-Internal-Key)

| Elemento    | Detalle                                     |
|-------------|---------------------------------------------|
| Mecanismo   | Header HTTP personalizado                   |
| Header      | `X-Internal-Key: <clave_secreta>`           |
| Rechazo     | Microservicio devuelve `403 Forbidden`      |

> Los microservicios **nunca** son accesibles directamente desde el exterior sin la clave interna.

---

## Estructura del Proyecto

```
e-commerce-microservices/
│
├── Gateway/                        # Laravel — Puerto 8000
│   ├── app/Http/Controllers/
│   │   ├── AuthController.php      # register, login, logout, me, forgot/reset password
│   │   ├── UsuarioController.php   # proxy → Django :8001
│   │   ├── ProductoController.php  # proxy → Flask :8002
│   │   ├── OrdenController.php     # proxy → Express :8003
│   │   ├── PagoController.php      # proxy → Laravel :8004
│   │   └── NotificacionController.php # proxy → Flask :8005
│   ├── app/Http/Middleware/
│   │   └── JwtMiddleware.php
│   ├── app/Services/
│   │   └── MicroserviceProxy.php
│   ├── routes/api.php
│   └── .env
│
├── usuarios/                       # Django — Puerto 8001
│   ├── usuarios/
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── middleware.py
│   │   └── urls.py
│   ├── settings.py
│   ├── manage.py
│   └── .env
│
├── productos/                      # Flask — Puerto 8002
│   ├── app.py
│   ├── config.py
│   ├── models.py
│   ├── routes.py
│   ├── middleware.py
│   └── .env
│
├── ordenes/                        # Express — Puerto 8003
│   ├── server.js
│   ├── src/
│   │   ├── app.js
│   │   ├── routes/ordenes.js
│   │   ├── middlewares/internalKey.js
│   │   └── models/Orden.js
│   ├── package.json
│   └── .env
│
├── pagos/                          # Laravel — Puerto 8004
│   ├── app/Http/Controllers/
│   │   └── PagoController.php
│   ├── app/Http/Middleware/
│   │   └── InternalKeyMiddleware.php
│   ├── app/Models/
│   │   └── Pago.php
│   ├── routes/api.php
│   └── .env
│
├── notificaciones/                 # Flask — Puerto 8005
│   ├── app.py
│   ├── routes.py
│   ├── middleware.py
│   ├── database.py
│   └── .env
│
├── tests/
│   ├── performance/load_test.js    # k6: capacidad, carga, estrés
│   └── security/security_test.py  # pruebas básicas de seguridad
│
├── .github/workflows/ci.yml        # Pipeline CI/CD
├── docker-compose.yml
├── .gitignore
└── README.md
```

---

## Instalación y Despliegue

### Prerequisitos

- PHP 8.3 + Composer
- Python 3.11
- Node.js 18
- MySQL (Laragon)
- PostgreSQL 17
- MongoDB (local o Atlas)
- Git

---

### 1. Clonar el repositorio

```bash
git clone https://github.com/TU_USUARIO/e-commerce-microservices.git
cd e-commerce-microservices
```

---

### 2. API Gateway — Laravel (Puerto 8000)

```bash
cd Gateway
composer install
cp .env.example .env
php artisan key:generate
php artisan jwt:secret
php artisan migrate
php artisan serve --port=8000
```

**Variables de entorno `.env`:**
```env
DB_CONNECTION=mysql
DB_HOST=127.0.0.1
DB_PORT=3306
DB_DATABASE=gateway_db
DB_USERNAME=root
DB_PASSWORD=

USUARIOS_URL=http://localhost:8001
PRODUCTOS_URL=http://localhost:8002
ORDENES_URL=http://localhost:8003
PAGOS_URL=http://localhost:8004
NOTIFICACIONES_URL=http://localhost:8005

INTERNAL_KEY=EcommerceSecretKey
JWT_SECRET=<generado_por_artisan>
JWT_TTL=60
```

---

### 3. Usuarios — Django (Puerto 8001)

```bash
cd usuarios
python -m venv venv
source venv/Scripts/activate   # Windows
pip install -r requirements.txt

# Crear base de datos en PostgreSQL
psql -U postgres -c "CREATE DATABASE usuarios_db;"

python manage.py migrate
python manage.py runserver 0.0.0.0:8001
```

**Variables de entorno `.env`:**
```env
DJANGO_SECRET_KEY=tu-clave-secreta
DB_NAME=usuarios_db
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=127.0.0.1
DB_PORT=5432
INTERNAL_KEY=ecommerce_internal_key_2026
```

---

### 4. Productos — Flask (Puerto 8002)

```bash
cd productos
python -m venv venv
source venv/Scripts/activate   # Windows
pip install -r requirements.txt
python app.py
```

**Variables de entorno `.env`:**
```env
PORT=8002
DB_USER=root
DB_PASSWORD=
DB_HOST=127.0.0.1
DB_PORT=3306
DB_NAME=productos_db
INTERNAL_KEY=ecommerce_internal_key_2026
```

---

### 5. Órdenes — Express (Puerto 8003)

```bash
cd ordenes
npm install
npm start
```

**Variables de entorno `.env`:**
```env
PORT=8003
MONGO_URI=mongodb://127.0.0.1:27017/ordenes_db
INTERNAL_KEY=ecommerce_internal_key_2026
```

---

### 6. Pagos — Laravel (Puerto 8004)

```bash
cd pagos
composer install
cp .env.example .env
php artisan key:generate
php artisan migrate
php artisan serve --port=8004
```

**Variables de entorno `.env`:**
```env
DB_CONNECTION=mysql
DB_HOST=127.0.0.1
DB_PORT=3306
DB_DATABASE=pagos_db
DB_USERNAME=root
DB_PASSWORD=
INTERNAL_KEY=ecommerce_internal_key_2026
```

---

### 7. Notificaciones — Flask (Puerto 8005)

```bash
cd notificaciones
python -m venv venv
source venv/Scripts/activate   # Windows
pip install -r requirements.txt
python app.py
```

**Variables de entorno `.env`:**
```env
PORT=8005
MONGO_URI=mongodb://127.0.0.1:27017/
MONGO_DB=notificaciones_db
INTERNAL_KEY=ecommerce_internal_key_2026
```

---

## Endpoints Documentados

> Todas las rutas del Gateway requieren `Authorization: Bearer <token>` excepto `/register`, `/login`, `/forgot-password` y `/reset-password`.
> Todos los microservicios requieren el header `X-Internal-Key: ecommerce_internal_key_2026`.

---

### API Gateway — `localhost:8000`

#### Rutas Públicas

| Método | Endpoint                  | Descripción                     |
|--------|---------------------------|---------------------------------|
| POST   | /api/register             | Registrar nuevo usuario         |
| POST   | /api/login                | Iniciar sesión, obtener JWT     |
| POST   | /api/forgot-password      | Solicitar recuperación          |
| POST   | /api/reset-password       | Resetear contraseña con token   |

**POST /api/register — Body:**
```json
{
  "name": "Ricardo Calderon",
  "email": "ricardo@example.com",
  "password": "password123",
  "password_confirmation": "password123"
}
```

**POST /api/login — Body:**
```json
{
  "email": "ricardo@example.com",
  "password": "password123"
}
```

**Respuesta login (200):**
```json
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "type": "bearer",
  "user": { "id": 1, "name": "Ricardo Calderon", "email": "ricardo@example.com" }
}
```

#### Rutas Protegidas (`Authorization: Bearer <token>`)

| Método | Endpoint                     | Proxy destino      | Descripción              |
|--------|------------------------------|--------------------|--------------------------|
| POST   | /api/logout                  | —                  | Cerrar sesión            |
| GET    | /api/me                      | —                  | Datos del usuario auth   |
| GET    | /api/usuarios                | Django :8001       | Listar usuarios          |
| GET    | /api/usuarios/{id}           | Django :8001       | Obtener usuario          |
| PUT    | /api/usuarios/{id}           | Django :8001       | Actualizar usuario       |
| DELETE | /api/usuarios/{id}           | Django :8001       | Desactivar usuario       |
| GET    | /api/productos               | Flask :8002        | Listar productos         |
| POST   | /api/productos               | Flask :8002        | Crear producto           |
| GET    | /api/productos/{id}          | Flask :8002        | Obtener producto         |
| PUT    | /api/productos/{id}          | Flask :8002        | Actualizar producto      |
| DELETE | /api/productos/{id}          | Flask :8002        | Eliminar producto        |
| GET    | /api/ordenes                 | Express :8003      | Listar órdenes           |
| POST   | /api/ordenes                 | Express :8003      | Crear orden              |
| GET    | /api/ordenes/{id}            | Express :8003      | Obtener orden            |
| PUT    | /api/ordenes/{id}            | Express :8003      | Actualizar orden         |
| DELETE | /api/ordenes/{id}            | Express :8003      | Cancelar orden           |
| GET    | /api/pagos                   | Laravel :8004      | Listar pagos             |
| POST   | /api/pagos                   | Laravel :8004      | Procesar pago            |
| GET    | /api/pagos/{id}              | Laravel :8004      | Obtener pago             |
| GET    | /api/notificaciones          | Flask :8005        | Listar notificaciones    |
| POST   | /api/notificaciones          | Flask :8005        | Crear notificación       |
| PATCH  | /api/notificaciones/{id}/leer| Flask :8005        | Marcar como leída        |
| DELETE | /api/notificaciones/{id}     | Flask :8005        | Eliminar notificación    |

---

### Usuarios — `localhost:8001`

| Método | Endpoint            | Descripción          | Validaciones                     |
|--------|---------------------|----------------------|----------------------------------|
| GET    | /usuarios           | Listar usuarios      | —                                |
| POST   | /usuarios           | Crear usuario        | nombre y email requeridos        |
| GET    | /usuarios/{id}      | Obtener usuario      | 404 si no existe                 |
| PUT    | /usuarios/{id}      | Actualizar usuario   | —                                |
| DELETE | /usuarios/{id}      | Desactivar usuario   | —                                |

**POST /usuarios — Body:**
```json
{
  "nombre": "Ana García",
  "email": "ana@example.com",
  "telefono": "3001234567",
  "direccion": "Calle 10 # 20-30, Manizales"
}
```

**Respuesta (201):**
```json
{
  "id": 1,
  "nombre": "Ana García",
  "email": "ana@example.com",
  "telefono": "3001234567",
  "direccion": "Calle 10 # 20-30, Manizales",
  "activo": true,
  "creado_en": "2026-04-01T20:00:00"
}
```

---

### Productos — `localhost:8002`

| Método | Endpoint            | Descripción          | Validaciones                        |
|--------|---------------------|----------------------|-------------------------------------|
| GET    | /productos          | Listar productos     | —                                   |
| POST   | /productos          | Crear producto       | nombre y precio requeridos, precio ≥ 0 |
| GET    | /productos/{id}     | Obtener producto     | 404 si no existe                    |
| PUT    | /productos/{id}     | Actualizar producto  | —                                   |
| DELETE | /productos/{id}     | Eliminar producto    | Soft delete (activo=False)          |

**POST /productos — Body:**
```json
{
  "nombre": "Laptop Dell XPS",
  "precio": 1200.00,
  "stock": 50,
  "categoria": "Tecnología",
  "descripcion": "Laptop de alto rendimiento"
}
```

**Respuesta (201):**
```json
{
  "id": 1,
  "nombre": "Laptop Dell XPS",
  "precio": 1200.0,
  "stock": 50,
  "categoria": "Tecnología",
  "descripcion": "Laptop de alto rendimiento",
  "activo": true,
  "creado_en": "2026-04-01T20:00:00"
}
```

---

### Órdenes — `localhost:8003`

| Método | Endpoint              | Descripción          | Validaciones                           |
|--------|-----------------------|----------------------|----------------------------------------|
| GET    | /ordenes              | Listar órdenes       | Query param: `?usuario_id=1`           |
| POST   | /ordenes              | Crear orden          | usuario_id y productos[] requeridos    |
| GET    | /ordenes/{id}         | Obtener orden        | 404 si no existe                       |
| PUT    | /ordenes/{id}         | Actualizar estado    | estado debe ser valor válido           |
| DELETE | /ordenes/{id}         | Cancelar orden       | Cambia estado a cancelada              |

**Estados válidos:** `pendiente` → `confirmada` → `enviada` → `entregada` → `cancelada`

**POST /ordenes — Body:**
```json
{
  "usuario_id": 1,
  "productos": [
    {
      "producto_id": "1",
      "nombre": "Laptop Dell XPS",
      "cantidad": 2,
      "precio_unitario": 1200.00
    }
  ],
  "direccion_envio": "Calle 10 # 20-30, Manizales"
}
```

**Respuesta (201):**
```json
{
  "_id": "69cd838222e0b8cdbf1d7998",
  "usuario_id": 1,
  "productos": [...],
  "total": 2400,
  "estado": "pendiente",
  "direccion_envio": "Calle 10 # 20-30, Manizales",
  "creado_en": "2026-04-01T20:00:00.000Z"
}
```

---

### Pagos — `localhost:8004`

| Método | Endpoint        | Descripción       | Validaciones                                        |
|--------|-----------------|-------------------|-----------------------------------------------------|
| GET    | /api/pagos      | Listar pagos      | Query param: `?usuario_id=1`                        |
| POST   | /api/pagos      | Procesar pago     | usuario_id, orden_id, monto > 0, metodo_pago válido |
| GET    | /api/pagos/{id} | Obtener pago      | 404 si no existe                                    |

**Métodos de pago válidos:** `tarjeta_credito`, `tarjeta_debito`, `paypal`, `transferencia`

**POST /api/pagos — Body:**
```json
{
  "usuario_id": 1,
  "orden_id": "69cd838222e0b8cdbf1d7998",
  "monto": 2400.00,
  "metodo_pago": "tarjeta_credito"
}
```

**Respuesta (201):**
```json
{
  "id": 1,
  "usuario_id": 1,
  "orden_id": "69cd838222e0b8cdbf1d7998",
  "monto": "2400.00",
  "metodo_pago": "tarjeta_credito",
  "estado": "completado",
  "referencia": "uuid-generado-automaticamente"
}
```

---

### Notificaciones — `localhost:8005`

| Método | Endpoint                        | Descripción               | Validaciones                         |
|--------|---------------------------------|---------------------------|--------------------------------------|
| GET    | /notificaciones                 | Listar notificaciones     | Query param: `?usuario_id=1`         |
| POST   | /notificaciones                 | Crear notificación        | usuario_id, tipo, mensaje requeridos |
| PATCH  | /notificaciones/{id}/leer       | Marcar como leída         | 404 si no existe                     |
| DELETE | /notificaciones/{id}            | Eliminar notificación     | 404 si no existe                     |

**POST /notificaciones — Body:**
```json
{
  "usuario_id": 1,
  "tipo": "orden_confirmada",
  "mensaje": "Tu orden ha sido confirmada exitosamente"
}
```

**Respuesta (201):**
```json
{
  "_id": "665f3a2b1c4e5d6f7a8b9c0d",
  "usuario_id": "1",
  "tipo": "orden_confirmada",
  "mensaje": "Tu orden ha sido confirmada exitosamente",
  "leida": false,
  "creado_en": "2026-04-01T20:00:00+00:00"
}
```

---

## Flujo Completo de una Compra

```
1. POST /api/login          → Obtener JWT
2. POST /api/productos      → Crear producto (con JWT)
3. POST /api/ordenes        → Crear orden con productos
4. POST /api/pagos          → Procesar pago de la orden
5. POST /api/notificaciones → Enviar notificación al usuario
```

---

## Bases de Datos

| Servicio        | Motor      | Base de datos       | Uso                        |
|-----------------|------------|---------------------|----------------------------|
| Gateway         | MySQL      | gateway_db          | Usuarios auth, tokens JWT  |
| Usuarios        | PostgreSQL | usuarios_db         | Perfiles de clientes       |
| Productos       | MySQL      | productos_db        | Catálogo y stock           |
| Órdenes         | MongoDB    | ordenes_db          | Historial de órdenes       |
| Pagos           | MySQL      | pagos_db            | Transacciones de pago      |
| Notificaciones  | MongoDB    | notificaciones_db   | Alertas y mensajes         |

---

## Pruebas

### Unitarias

```bash
# Gateway (Laravel)
cd Gateway && php artisan test

# Usuarios (Django)
cd usuarios && python -m pytest tests/ -v

# Productos (Flask)
cd productos && python -m pytest tests/ -v

# Órdenes (Express)
cd ordenes && npm test

# Pagos (Laravel)
cd pagos && php artisan test
```

### Rendimiento (k6)

```bash
# Instalar k6: https://k6.io/docs/get-started/installation/
k6 run tests/performance/load_test.js -e BASE_URL=http://localhost:8000
```

Incluye pruebas de **capacidad**, **carga** y **estrés**.

### Seguridad

```bash
pip install requests pytest
pytest tests/security/security_test.py -v
```

---

## Variables de Entorno

| Variable        | Servicio        | Descripción                          |
|-----------------|-----------------|--------------------------------------|
| `JWT_SECRET`    | Gateway         | Clave para firmar tokens JWT         |
| `JWT_TTL`       | Gateway         | Tiempo de vida del token (minutos)   |
| `INTERNAL_KEY`  | Todos           | Clave compartida gateway↔servicios   |
| `USUARIOS_URL`  | Gateway         | URL del microservicio Django         |
| `PRODUCTOS_URL` | Gateway         | URL del microservicio Flask          |
| `ORDENES_URL`   | Gateway         | URL del microservicio Express        |
| `PAGOS_URL`     | Gateway         | URL del microservicio Laravel pagos  |
| `NOTIFICACIONES_URL` | Gateway    | URL del microservicio Flask notif.   |
| `MONGO_URI`     | Órdenes/Notif.  | URI de conexión a MongoDB            |
