import os
from django.http import JsonResponse
from functools import wraps

def internal_key_required(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        key = request.headers.get('X-Internal-Key', '')
        if key != os.getenv('INTERNAL_KEY', ''):
            return JsonResponse({'error': 'Acceso no autorizado'}, status=403)
        return func(request, *args, **kwargs)
    return wrapper