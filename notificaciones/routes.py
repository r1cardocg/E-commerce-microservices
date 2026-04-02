from flask import Blueprint, request, jsonify
from database import db
from middleware import internal_key_required
from datetime import datetime, timezone
from bson import ObjectId

bp = Blueprint('notificaciones', __name__)

def parse(doc):
    doc['_id'] = str(doc['_id'])
    return doc

@bp.route('/notificaciones', methods=['GET'])
@internal_key_required
def listar():
    """GET /notificaciones — Lista notificaciones, filtra por usuario_id si se pasa."""
    usuario_id = request.args.get('usuario_id')
    filtro = {'usuario_id': usuario_id} if usuario_id else {}
    docs = list(db.notificaciones.find(filtro).sort('creado_en', -1).limit(50))
    return jsonify({'notificaciones': [parse(d) for d in docs]}), 200

@bp.route('/notificaciones', methods=['POST'])
@internal_key_required
def crear():
    """POST /notificaciones — Crea una nueva notificación."""
    data   = request.get_json(force=True, silent=True) or {}
    errors = {}
    if not data.get('usuario_id'):
        errors['usuario_id'] = 'El usuario_id es requerido'
    if not data.get('tipo'):
        errors['tipo'] = 'El tipo es requerido'
    if not data.get('mensaje'):
        errors['mensaje'] = 'El mensaje es requerido'
    if errors:
        return jsonify({'errors': errors}), 422

    doc = {
        'usuario_id': str(data['usuario_id']),
        'tipo':       data['tipo'],
        'mensaje':    data['mensaje'],
        'leida':      False,
        'creado_en':  datetime.now(timezone.utc).isoformat(),
    }
    result = db.notificaciones.insert_one(doc)
    doc['_id'] = str(result.inserted_id)
    return jsonify(doc), 201

@bp.route('/notificaciones/<string:nid>/leer', methods=['PATCH'])
@internal_key_required
def marcar_leida(nid):
    """PATCH /notificaciones/{id}/leer — Marca una notificación como leída."""
    result = db.notificaciones.update_one(
        {'_id': ObjectId(nid)},
        {'$set': {'leida': True}}
    )
    if result.matched_count == 0:
        return jsonify({'error': 'Notificación no encontrada'}), 404
    return jsonify({'message': 'Notificación marcada como leída'}), 200

@bp.route('/notificaciones/<string:nid>', methods=['DELETE'])
@internal_key_required
def eliminar(nid):
    """DELETE /notificaciones/{id} — Elimina una notificación."""
    result = db.notificaciones.delete_one({'_id': ObjectId(nid)})
    if result.deleted_count == 0:
        return jsonify({'error': 'Notificación no encontrada'}), 404
    return jsonify({'message': 'Notificación eliminada'}), 200
