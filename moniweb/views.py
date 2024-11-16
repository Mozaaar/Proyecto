from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, View
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.contrib import messages
import random
from .models import Factura, Envio
from .forms import ZonaForm, ClienteForm, ServicioForm, FacturaForm, PagoForm, EnvioForm, PaqueteForm

class RedirectToMenuView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(reverse('menu'))

def menu_vista(request):
    return render(request, 'menu.html')

class NuevoEnvioView(View):
    def get(self, request, *args, **kwargs):
        zona_form = ZonaForm()
        cliente_form = ClienteForm()
        servicio_form = ServicioForm()
        factura_form = FacturaForm()
        pago_form = PagoForm()
        envio_form = EnvioForm()
        paquete_form = PaqueteForm()

        return render(request, 'nuevo_envio.html', {
            'zona_form': zona_form,
            'cliente_form': cliente_form,
            'servicio_form': servicio_form,
            'factura_form': factura_form,
            'pago_form': pago_form,
            'envio_form': envio_form,
            'paquete_form': paquete_form,
        })

    def post(self, request, *args, **kwargs):
        zona_form = ZonaForm(request.POST)
        cliente_form = ClienteForm(request.POST)
        servicio_form = ServicioForm(request.POST)
        factura_form = FacturaForm(request.POST)
        pago_form = PagoForm(request.POST)
        envio_form = EnvioForm(request.POST)
        paquete_form = PaqueteForm(request.POST)

        # Guardar Zona
        if 'save_zona' in request.POST:
            if zona_form.is_valid():
                zona_form.save()
                messages.success(request, "Zona guardada con éxito.")
                return redirect('nuevo_envio')

        # Guardar Cliente
        if 'save_cliente' in request.POST:
            if cliente_form.is_valid():
                cliente_form.save()
                messages.success(request, "Cliente guardado con éxito.")
                return redirect('nuevo_envio')

        # Guardar Servicio
        if 'save_servicio' in request.POST:
            if servicio_form.is_valid():
                servicio = servicio_form.save(commit=False)
                # Aquí puedes establecer relaciones si es necesario, por ejemplo:
                # servicio.id_cliente = cliente_form.instance  # Si el cliente ya fue guardado
                servicio.save()
                messages.success(request, "Servicio guardado con éxito.")
                return redirect('nuevo_envio')

        # Guardar Factura
        if 'save_factura' in request.POST:
            if factura_form.is_valid():
                factura = factura_form.save(commit=False)
                # factura.id_servicio = servicio_form.instance  # Si el servicio ya fue guardado
                factura.save()
                messages.success(request, "Factura guardada con éxito.")
                return redirect('nuevo_envio')

        # Guardar Pago
        if 'save_pago' in request.POST:
            if pago_form.is_valid():
                pago = pago_form.save(commit=False)
                # pago.id_factura = factura_form.instance  # Si la factura ya fue guardada
                # pago.id_cliente = cliente_form.instance  # Si el cliente ya fue guardado
                pago.save()
                messages.success(request, "Pago guardado con éxito.")
                return redirect('nuevo_envio')

        # Guardar Envío
        if 'save_envio' in request.POST:
            if envio_form.is_valid():
                envio = envio_form.save(commit=False)
                # envio.id_servicio = servicio_form.instance  # Si el servicio ya fue guardado
                envio.save()
                messages.success(request, "Envío guardado con éxito.")
                return redirect('nuevo_envio')

        # Guardar Paquete
        if 'save_paquete' in request.POST:
            if paquete_form.is_valid():
                paquete = paquete_form.save(commit=False)
                # paquete.id_envio = envio_form.instance  # Si el envío ya fue guardado
                paquete.save()
                messages.success(request, "Paquete guardado con éxito.")
                return redirect('nuevo_envio')

        # Si no se guarda nada, renderiza de nuevo con los formularios
        return render(request, 'nuevo_envio.html', {
            'zona_form': zona_form,
            'cliente_form': cliente_form,
            'servicio_form': servicio_form,
            'factura_form': factura_form,
            'pago_form': pago_form,
            'envio_form': envio_form,
            'paquete_form': paquete_form,
        })

class ListarEnviosView(ListView):
    model = Envio
    template_name = 'listar_envios.html'  # Nombre de tu plantilla
    context_object_name = 'envios'

class SeleccionarActualizarEnvioView(View):
    def get(self, request):
        envios = Envio.objects.all()  # Obtener todos los envíos
        return render(request, 'seleccionar_actualizar_envio.html', {'envios': envios})

    def post(self, request):
        envio_id = request.POST.get('envio_id')
        return redirect('actualizar_envio', pk=envio_id)
class ActualizarEnvioView(SuccessMessageMixin, UpdateView):
    model = Envio
    form_class = EnvioForm
    template_name = 'actualizar_envio.html'
    success_url = reverse_lazy('listar_envios')
    success_message = "¡Envío actualizado exitosamente!"
    context_object_name = 'envio'
class SeleccionarEliminarEnvioView(View):
     def get(self, request):
        envios = Envio.objects.all()  # Obtener todos los envíos
        return render(request, 'seleccionar_eliminar_envio.html', {'envios': envios})

     def post(self, request):
        envio_id = request.POST.get('envio_id')
        return redirect('eliminar_envio', pk=envio_id)

class EliminarEnvioView(DeleteView):
    model = Envio
    template_name = 'eliminar_envio.html'  # Aquí se especifica la plantilla de confirmación
    success_url = reverse_lazy('listar_envios')  # Redirige a la lista de envíos después de eliminar

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        messages.success(self.request, "¡Envío eliminado exitosamente!")
        return super().delete(request, *args, **kwargs)

