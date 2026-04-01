from django.urls import path
from usuarios.views import UsuarioListView, UsuarioDetailView

urlpatterns = [
    path('usuarios',          UsuarioListView.as_view()),
    path('usuarios/<int:pk>', UsuarioDetailView.as_view()),
]