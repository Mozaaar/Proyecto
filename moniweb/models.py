from django.db import models

class Departamento(models.Model):
    id = models.AutoField(primary_key=True)  # Autoincremental
    nombre = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.nombre


class Ciudad(models.Model):
    id = models.AutoField(primary_key=True)  # Autoincremental
    nombre = models.CharField(max_length=255)
    id_departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre


class Zona(models.Model):
    id = models.AutoField(primary_key=True)  # Autoincremental
    nombre = models.CharField(max_length=255)
    codigo_postal = models.CharField(max_length=20)
    id_ciudad = models.ForeignKey(Ciudad, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre


class TipoCliente(models.Model):
    id_tipo_cliente = models.AutoField(primary_key=True)  # Autoincremental
    tipo = models.CharField(max_length=255)

    def __str__(self):
        return self.tipo


class Cliente(models.Model):
    id = models.AutoField(primary_key=True)  # Autoincremental
    nombre = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20)
    direccion = models.CharField(max_length=255)
    id_zona = models.ForeignKey(Zona, on_delete=models.CASCADE)
    id_tipo_cliente = models.ForeignKey(TipoCliente, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre


class Transporte(models.Model):
    id = models.AutoField(primary_key=True)  # Autoincremental
    tipo = models.CharField(max_length=255)
    capacidad = models.CharField(max_length=255)
    estado = models.CharField(max_length=50)

    def __str__(self):
        return self.tipo


class Transportista(models.Model):
    id_transportista = models.AutoField(primary_key=True)  # Autoincremental
    nombre = models.CharField(max_length=255)
    telefono = models.CharField(max_length=20)
    id_transporte = models.ForeignKey(Transporte, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre


class Servicio(models.Model):
    id_servicio = models.AutoField(primary_key=True)  # Autoincremental
    fecha_solicitud = models.DateField()
    fecha_ejecucion = models.DateField()
    id_cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    id_zona = models.ForeignKey(Zona, on_delete=models.CASCADE)
    costo = models.FloatField()

    def __str__(self):
        return f'Servicio {self.id_servicio}'


class Factura(models.Model):
    id_factura = models.AutoField(primary_key=True)  # Autoincremental
    direccion_despacho = models.CharField(max_length=255)
    id_zona_despacho = models.ForeignKey(Zona, related_name='facturas_despacho', on_delete=models.CASCADE)
    direccion_embarque = models.CharField(max_length=255)
    id_zona_embarque = models.ForeignKey(Zona, related_name='facturas_embarque', on_delete=models.CASCADE)
    numero_guia = models.CharField(max_length=255)
    id_servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)
    monto = models.FloatField()

    def __str__(self):
        return f'Factura {self.id_factura}'


class TipoDePago(models.Model):
    id = models.AutoField(primary_key=True)  # Autoincremental
    tipo = models.CharField(max_length=255)
    def __str__(self):
        return self.tipo


class Pago(models.Model):
    id = models.AutoField(primary_key=True)  # Autoincremental
    monto = models.FloatField()
    fecha = models.DateField()
    detalle = models.TextField(null=True, blank=True) 
    id_tipo_pago = models.ForeignKey(TipoDePago, on_delete=models.CASCADE)
    id_factura = models.ForeignKey(Factura, on_delete=models.CASCADE)
    id_cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return f'Pago {self.id}'


class Envio(models.Model):
    id = models.AutoField(primary_key=True)  # Autoincremental
    fecha_envio = models.DateField()
    fecha_entrega = models.DateField()
    estado_envio = models.CharField(max_length=50)
    numero_guia = models.CharField(max_length=255, default=1)
    id_factura = models.ForeignKey(Factura, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return f'Envio {self.id}'


class Paquete(models.Model):
    id = models.AutoField(primary_key=True)  # Autoincremental
    peso = models.FloatField()
    dimensiones = models.CharField(max_length=255)
    estado = models.CharField(max_length=50)
    id_transportista = models.ForeignKey(Transportista, on_delete=models.CASCADE)
    id_envio = models.ForeignKey(Envio, on_delete=models.CASCADE)

    def __str__(self):
        return f'Paquete {self.id}'


