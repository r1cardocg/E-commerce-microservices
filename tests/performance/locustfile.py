from locust import HttpUser, task, between, LoadTestShape
import random
import string


def random_email():
    suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
    return f"user_{suffix}@loadtest.com"


class EcommerceUser(HttpUser):
    host      = "http://127.0.0.1:8000"
    wait_time = between(1, 3)

    def on_start(self):
        # token como atributo de instancia, NO de clase
        self.token = ""
        email    = random_email()
        password = "Password123!"

        # Registrar
        self.client.post("/api/register", json={
            "name":                  f"LoadUser",
            "email":                 email,
            "password":              password,
            "password_confirmation": password,
        }, headers={"Accept": "application/json", "Content-Type": "application/json"})

        # Login
        r = self.client.post("/api/login", json={
            "email":    email,
            "password": password,
        }, headers={"Accept": "application/json", "Content-Type": "application/json"})

        if r.status_code == 200:
            body = r.json()
            # Soporta {"token": ...} y {"access_token": ...}
            self.token = body.get("access_token") or body.get("token", "")

    def h(self):
        return {
            "Authorization": f"Bearer {self.token}",
            "Accept":        "application/json",
            "Content-Type":  "application/json",
        }

    # ── Productos ─────────────────────────────────────────────
    @task(3)
    def listar_productos(self):
        self.client.get("/api/productos", headers=self.h())

    @task(2)
    def crear_producto(self):
        self.client.post("/api/productos", json={
            "nombre":    f"Producto {random.randint(1, 9999)}",
            "precio":    round(random.uniform(10, 1000), 2),
            "stock":     random.randint(1, 100),
            "categoria": random.choice(["Tecnología", "Ropa", "Hogar", "Deportes"]),
        }, headers=self.h())

    # ── Órdenes ───────────────────────────────────────────────
    @task(3)
    def listar_ordenes(self):
        self.client.get("/api/ordenes", headers=self.h())

    @task(1)
    def crear_orden(self):
        self.client.post("/api/ordenes", json={
            "usuario_id": random.randint(1, 100),
            "productos": [{
                "producto_id":     str(random.randint(1, 50)),
                "nombre":          "Producto Test",
                "cantidad":        random.randint(1, 5),
                "precio_unitario": round(random.uniform(10, 500), 2),
            }],
            "direccion_envio": f"Calle {random.randint(1, 100)} # {random.randint(1, 50)}",
        }, headers=self.h())

    # ── Pagos ─────────────────────────────────────────────────
    @task(2)
    def listar_pagos(self):
        self.client.get("/api/pagos", headers=self.h())

    @task(1)
    def crear_pago(self):
        self.client.post("/api/pagos", json={
            "usuario_id":  random.randint(1, 100),
            "orden_id":    f"orden-{random.randint(1000, 9999)}",
            "monto":       round(random.uniform(50, 2000), 2),
            "metodo_pago": random.choice([
                "tarjeta_credito", "tarjeta_debito", "paypal", "transferencia"
            ]),
        }, headers=self.h())

    # ── Usuarios ──────────────────────────────────────────────
    @task(2)
    def listar_usuarios(self):
        self.client.get("/api/usuarios", headers=self.h())

    # ── Notificaciones ────────────────────────────────────────
    @task(1)
    def listar_notificaciones(self):
        self.client.get("/api/notificaciones", headers=self.h())

    @task(1)
    def crear_notificacion(self):
        self.client.post("/api/notificaciones", json={
            "usuario_id": random.randint(1, 100),
            "tipo":       random.choice([
                "orden_confirmada", "pago_completado",
                "envio_realizado", "entrega_completada"
            ]),
            "mensaje": f"Notificación de prueba {random.randint(1, 9999)}",
        }, headers=self.h())


class CapacidadShape(LoadTestShape):
    """
    Los 3 escenarios en uno:
      0-90s   → Capacidad  (rampa progresiva 0→100 usuarios)
      90-210s → Carga      (20 usuarios sostenidos)
      210-330s→ Estrés     (200 usuarios, carga extrema)
      330-360s→ Bajada
    """
    stages = [
        # Capacidad — rampa progresiva
        {"duration": 30,  "users": 10,  "spawn_rate": 2},
        {"duration": 60,  "users": 50,  "spawn_rate": 5},
        {"duration": 90,  "users": 100, "spawn_rate": 10},
        # Carga — sostenida normal
        {"duration": 150, "users": 20,  "spawn_rate": 5},
        {"duration": 210, "users": 20,  "spawn_rate": 5},
        # Estrés — carga extrema
        {"duration": 270, "users": 200, "spawn_rate": 20},
        {"duration": 330, "users": 200, "spawn_rate": 20},
        # Bajada
        {"duration": 360, "users": 0,   "spawn_rate": 20},
    ]

    def tick(self):
        run_time = self.get_run_time()
        for stage in self.stages:
            if run_time < stage["duration"]:
                return stage["users"], stage["spawn_rate"]
        return None
