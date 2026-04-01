import json
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import Usuario
from .middleware import internal_key_required

@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(internal_key_required, name='dispatch')
class UsuarioListView(View):
    def get(self, request):
        usuarios = [u.to_dict() for u in Usuario.objects.filter(activo=True)]
        return JsonResponse({'usuarios': usuarios}, status=200)

    def post(self, request):
        try:
            data = json.loads(request.body)
        except:
            return JsonResponse({'error': 'JSON inválido'}, status=400)

        errors = {}
        if not data.get('nombre'):
            errors['nombre'] = 'El nombre es requerido'
        if not data.get('email'):
            errors['email'] = 'El email es requerido'
        if errors:
            return JsonResponse({'errors': errors}, status=422)

        if Usuario.objects.filter(email=data['email']).exists():
            return JsonResponse({'error': 'El email ya existe'}, status=422)

        usuario = Usuario.objects.create(
            nombre=data['nombre'],
            email=data['email'],
            telefono=data.get('telefono', ''),
            direccion=data.get('direccion', ''),
        )
        return JsonResponse(usuario.to_dict(), status=201)


@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(internal_key_required, name='dispatch')
class UsuarioDetailView(View):
    def get(self, request, pk):
        try:
            usuario = Usuario.objects.get(pk=pk)
        except Usuario.DoesNotExist:
            return JsonResponse({'error': 'Usuario no encontrado'}, status=404)
        return JsonResponse(usuario.to_dict())

    def put(self, request, pk):
        try:
            usuario = Usuario.objects.get(pk=pk)
        except Usuario.DoesNotExist:
            return JsonResponse({'error': 'Usuario no encontrado'}, status=404)
        data = json.loads(request.body)
        for field in ['nombre', 'telefono', 'direccion']:
            if field in data:
                setattr(usuario, field, data[field])
        usuario.save()
        return JsonResponse(usuario.to_dict())

    def delete(self, request, pk):
        try:
            usuario = Usuario.objects.get(pk=pk)
        except Usuario.DoesNotExist:
            return JsonResponse({'error': 'Usuario no encontrado'}, status=404)
        usuario.activo = False
        usuario.save()
        return JsonResponse({'message': 'Usuario desactivado'})