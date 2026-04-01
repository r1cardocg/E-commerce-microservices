from flask import Blueprint, request, jsonify
from extensions import db
from models import Producto
from middleware import internal_key_required

bp = Blueprint('productos', __name__)

@bp.route('/productos', methods=['GET'])
@internal_key_required
def listar():
    productos = Producto.query.filter_by(activo=True).all()
    return jsonify({'productos': [p.to_dict() for p in productos]}), 200

@bp.route('/productos', methods=['POST'])
@internal_key_required
def crear():
    data   = request.get_json(force=True, silent=True) or {}
    errors = {}
    if not data.get('nombre'):
        errors['nombre'] = 'El nombre es requerido'
    if data.get('precio') is None:
        errors['precio'] = 'El precio es requerido'
    elif float(data['precio']) < 0:
        errors['precio'] = 'El precio no puede ser negativo'
    if errors:
        return jsonify({'errors': errors}), 422

    p = Producto(
        nombre=data['nombre'],
        descripcion=data.get('descripcion', ''),
        precio=data['precio'],
        stock=data.get('stock', 0),
        categoria=data.get('categoria', ''),
    )
    db.session.add(p)
    db.session.commit()
    return jsonify(p.to_dict()), 201

@bp.route('/productos/<int:id>', methods=['GET'])
@internal_key_required
def obtener(id):
    p = Producto.query.get_or_404(id)
    return jsonify(p.to_dict()), 200

@bp.route('/productos/<int:id>', methods=['PUT'])
@internal_key_required
def actualizar(id):
    p    = Producto.query.get_or_404(id)
    data = request.get_json(force=True, silent=True) or {}
    for field in ['nombre', 'descripcion', 'precio', 'stock', 'categoria']:
        if field in data:
            setattr(p, field, data[field])
    db.session.commit()
    return jsonify(p.to_dict()), 200

@bp.route('/productos/<int:id>', methods=['DELETE'])
@internal_key_required
def eliminar(id):
    p = Producto.query.get_or_404(id)
    p.activo = False
    db.session.commit()
    return jsonify({'message': 'Producto eliminado'}), 200