import os
from functools import wraps
from flask import request, jsonify

def internal_key_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        key = request.headers.get('X-Internal-Key', '')
        if key != os.getenv('INTERNAL_KEY', ''):
            return jsonify({'error': 'Acceso no autorizado'}), 403
        return f(*args, **kwargs)
    return decorated