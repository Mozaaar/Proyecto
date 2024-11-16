from django.contrib import admin

# Register your models here.
from .models import Departamento
from .models import Ciudad
from .models import Zona
from .models import TipoCliente
from .models import Cliente
from .models import TipoDePago
from .models import Transportista
from .models import Transporte
from .models import Servicio
from .models import Factura
from .models import Pago
from .models import Paquete
from .models import Envio

# Register your models here.


admin.site.register(Departamento)
admin.site.register(Ciudad)
admin.site.register(Zona)
admin.site.register(TipoCliente)
admin.site.register(Cliente)
admin.site.register(TipoDePago)
admin.site.register(Transportista)
admin.site.register(Transporte)
admin.site.register(Servicio)
admin.site.register(Factura)
admin.site.register(Pago)
admin.site.register(Paquete)
admin.site.register(Envio)
