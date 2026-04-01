from extensions import db
from datetime import datetime

class Producto(db.Model):
    __tablename__ = 'productos'

    id          = db.Column(db.Integer, primary_key=True)
    nombre      = db.Column(db.String(255), nullable=False)
    descripcion = db.Column(db.Text, default='')
    precio      = db.Column(db.Numeric(10, 2), nullable=False)
    stock       = db.Column(db.Integer, default=0)
    categoria   = db.Column(db.String(100), default='')
    activo      = db.Column(db.Boolean, default=True)
    creado_en   = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id':          self.id,
            'nombre':      self.nombre,
            'descripcion': self.descripcion,
            'precio':      float(self.precio),
            'stock':       self.stock,
            'categoria':   self.categoria,
            'activo':      self.activo,
            'creado_en':   self.creado_en.isoformat(),
        }