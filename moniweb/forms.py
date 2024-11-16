from django import forms
from .models import Cliente, Servicio, Factura, Pago, Envio, Paquete, Zona, Transportista
from django.utils import timezone
import random

class ZonaForm(forms.ModelForm):
    class Meta:
        model = Zona
        fields = ['nombre', 'codigo_postal', 'id_ciudad']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'codigo_postal': forms.TextInput(attrs={'class': 'form-control'}),
            'id_ciudad': forms.Select(attrs={'class': 'form-control'}),
        }

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'email', 'telefono', 'direccion', 'id_zona', 'id_tipo_cliente']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'id_zona': forms.Select(attrs={'class': 'form-control'}),
            'id_tipo_cliente': forms.Select(attrs={'class': 'form-control'}),
        }

class ServicioForm(forms.ModelForm):
    class Meta:
        model = Servicio
        fields = ['id_cliente', 'id_zona', 'costo']
        widgets = {
            
            'id_cliente': forms.Select(attrs={'class': 'form-control'}),
            'id_zona': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(ServicioForm, self).__init__(*args, **kwargs)
        if not self.instance.pk:  # Solo para nuevos registros
            self.initial['fecha_solicitud'] = timezone.now().date()
            self.initial['fecha_ejecucion'] = timezone.now().date() + timezone.timedelta(days=15)

    def save(self, commit=True):
        instance = super(ServicioForm, self).save(commit=False)
        if not instance.pk:  # Para nuevos registros
            instance.fecha_solicitud = timezone.now().date()
            instance.fecha_ejecucion = timezone.now().date() + timezone.timedelta(days=15)
         
        if commit:
            instance.save()
        return instance

class FacturaForm(forms.ModelForm):
    class Meta:
        model = Factura
        fields = ['direccion_despacho', 'id_zona_despacho', 'direccion_embarque', 'id_zona_embarque', 'numero_guia', 'id_servicio']
        widgets = {
            'direccion_despacho': forms.TextInput(attrs={'class': 'form-control'}),
            'id_zona_despacho': forms.Select(attrs={'class': 'form-control'}),
            'direccion_embarque': forms.TextInput(attrs={'class': 'form-control'}),
            'id_zona_embarque': forms.Select(attrs={'class': 'form-control'}),
            'numero_guia': forms.TextInput(attrs={'class': 'form-control'}),
            'id_servicio': forms.Select(attrs={'class': 'form-control'}),
        }

    def save(self, commit=True):
        instance = super(FacturaForm, self).save(commit=False)
        if not instance.pk:  # Para nuevos registros
            cliente = instance.id_servicio.id_cliente
            instance.direccion_despacho = cliente.direccion
            instance.id_zona_despacho = cliente.id_zona
            instance.numero_guia = f'NG-{random.randint(1000, 9999)}'  # Genera un número de guía
            instance.monto = instance.id_servicio.costo
        if commit:
            instance.save()
        return instance

class PagoForm(forms.ModelForm):
    class Meta:
        model = Pago
        fields = ['id_factura', 'fecha', 'id_tipo_pago', 'detalle' ]
        widgets = {
            'id_factura': forms.Select(attrs={'class': 'form-control'}),
            'fecha': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'id_tipo_pago': forms.Select(attrs={'class': 'form-control'}),
            'detalle': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(PagoForm, self).__init__(*args, **kwargs)
        if not self.instance.pk:  # Solo para nuevos registros
            self.initial['fecha'] = timezone.now().date()

    def save(self, commit=True):
        instance = super(PagoForm, self).save(commit=False)
        if not instance.pk:  # Para nuevos registros
            instance.fecha = timezone.now().date()
            # Suponiendo que tienes un id_factura e id_cliente actuales disponibles
            instance.id_factura = Factura.objects.latest('id_factura')
            instance.id_cliente = instance.id_factura.id_servicio.id_cliente
            instance.monto = instance.id_factura.monto

        if commit:
            instance.save()
        return instance

class EnvioForm(forms.ModelForm):
    class Meta:
        model = Envio
        fields = ['estado_envio', 'id_factura']
        widgets = {
            'estado_envio': forms.TextInput(attrs={'class': 'form-control'}),
            'id_factura': forms.Select(attrs={'class': 'form-control'}),

        }

    def save(self, commit=True):
        instance = super(EnvioForm, self).save(commit=False)
        if not instance.pk:  # Para nuevos registros
            servicio = instance.id_factura.id_servicio
            instance.fecha_envio = servicio.fecha_ejecucion
            instance.fecha_entrega = servicio.fecha_ejecucion + timezone.timedelta(days=15)
            instance.numero_guia = instance.id_factura.numero_guia
        if commit:
            instance.save()
        return instance

class PaqueteForm(forms.ModelForm):
    class Meta:
        model = Paquete
        fields = ['peso', 'dimensiones', 'estado', 'id_transportista', 'id_envio']
        widgets = {
            'peso': forms.NumberInput(attrs={'class': 'form-control'}),
            'dimensiones': forms.TextInput(attrs={'class': 'form-control'}),
            'estado': forms.TextInput(attrs={'class': 'form-control'}),
            'id_transportista': forms.Select(attrs={'class': 'form-control'}),
            'id_envio': forms.Select(attrs={'class': 'form-control'}),
        }

    def save(self, commit=True):
        instance = super(PaqueteForm, self).save(commit=False)
        if not instance.pk:  # Para nuevos registros
            # Suponiendo que tienes un id_transportista e id_envio actuales disponibles
            instance.id_transportista = Transportista.objects.latest('id_transportista')
            instance.id_envio = Envio.objects.latest('id')
        if commit:
            instance.save()
        return instance
