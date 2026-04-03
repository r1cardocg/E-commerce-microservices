from django.db import models

class Usuario(models.Model):
    nombre    = models.CharField(max_length=255)
    email     = models.EmailField(unique=True)
    telefono  = models.CharField(max_length=20, blank=True)
    direccion = models.TextField(blank=True)
    activo    = models.BooleanField(default=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'usuarios'

    def to_dict(self):
        return {
            'id':        self.pk,
            'nombre':    self.nombre,
            'email':     self.email,
            'telefono':  self.telefono,
            'direccion': self.direccion,
            'activo':    self.activo,
            'creado_en': self.creado_en.isoformat(),
        }
