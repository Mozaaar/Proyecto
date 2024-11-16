from django.urls import path
from .views import (
    NuevoEnvioView,
    ListarEnviosView,
    ActualizarEnvioView,
    EliminarEnvioView,
    menu_vista,
    RedirectToMenuView,
    SeleccionarActualizarEnvioView,
    SeleccionarEliminarEnvioView,
)
urlpatterns = [
    path('', RedirectToMenuView.as_view(), name='redirect_to_menu'),  # Redirige a menú
    path('menu/', menu_vista, name='menu'),
    path('nuevo/', NuevoEnvioView.as_view(), name='nuevo_envio'),
    path('envios/', ListarEnviosView.as_view(), name='listar_envios'),
    path('actualizar/', SeleccionarActualizarEnvioView.as_view(), name='seleccionar_actualizar_envio'),
    path('<int:pk>/actualizar/', ActualizarEnvioView.as_view(), name='actualizar_envio'),
    path('eliminar/', SeleccionarEliminarEnvioView.as_view(), name='seleccionar_eliminar_envio'),
    path('<int:pk>/eliminar/', EliminarEnvioView.as_view(), name='eliminar_envio'),
]

