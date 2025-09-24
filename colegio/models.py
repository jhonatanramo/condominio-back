from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone

# -------------------- País --------------------
class Pais(models.Model):
    nombre = models.CharField(max_length=100)
    codigo = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return self.nombre

# -------------------- Rol --------------------
class Rol(models.Model):
    nombre = models.CharField(max_length=60)

    def __str__(self):
        return self.nombre

# -------------------- Persona --------------------from django.contrib.auth.models import User
from django.contrib.auth.models import User

class Persona(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    ci = models.CharField(max_length=40, blank=True, null=True)
    nombre = models.CharField(max_length=80)
    apellido_paterno = models.CharField(max_length=80, blank=True, null=True)
    apellido_materno = models.CharField(max_length=80, blank=True, null=True)
    fecha_creada = models.DateField(auto_now_add=True)
    pais = models.ForeignKey(Pais, on_delete=models.SET_NULL, null=True)
    telefono = models.CharField(max_length=40, blank=True, null=True)
    clave=models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido_paterno or ''}"

# -------------------- Relación n:m Rol-Persona --------------------
class RolPersona(models.Model):
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE)
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE)
    fecha_asignada = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('persona', 'rol')

# -------------------- Condominio --------------------
class Condominio(models.Model):
    nombre = models.CharField(max_length=120)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    responsable = models.ForeignKey(Persona, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.nombre

# -------------------- Unidad --------------------
class Unidad(models.Model):
    condominio = models.ForeignKey(Condominio, on_delete=models.CASCADE)
    propietario = models.ForeignKey(Persona, on_delete=models.SET_NULL, null=True)
    nro_modulo = models.PositiveSmallIntegerField(blank=True, null=True)
    nro_piso = models.PositiveSmallIntegerField(blank=True, null=True)
    nro_habitacion = models.PositiveSmallIntegerField(blank=True, null=True)
    valor_mensual = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    capacidad = models.PositiveSmallIntegerField(blank=True, null=True)
    nro_contrato = models.CharField(max_length=80, blank=True, null=True)

# -------------------- Área social --------------------
class AreaSocial(models.Model):
    nombre = models.CharField(max_length=120)
    ubicacion = models.CharField(max_length=255, blank=True, null=True)
    hora_inicio_permitido = models.TimeField(blank=True, null=True)
    hora_fin_permitido = models.TimeField(blank=True, null=True)
    capacidad_maxima = models.PositiveSmallIntegerField(blank=True, null=True)

    def __str__(self):
        return self.nombre

# -------------------- Restricción --------------------
class Restriccion(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=500, blank=True, null=True)

# -------------------- Relación n:m Restricción-Área --------------------
class RestriccionArea(models.Model):
    restriccion = models.ForeignKey(Restriccion, on_delete=models.CASCADE)
    area_social = models.ForeignKey(AreaSocial, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('restriccion', 'area_social')

# -------------------- Reserva --------------------
class Reserva(models.Model):
    ESTADOS = [
        ('confirmada', 'Confirmada'),
        ('cancelada', 'Cancelada'),
        ('pendiente', 'Pendiente'),
    ]

    persona = models.ForeignKey(Persona, on_delete=models.CASCADE)
    area_social = models.ForeignKey(AreaSocial, on_delete=models.CASCADE)
    horario_inicio = models.TimeField()
    horario_fin = models.TimeField()
    fecha = models.DateField()
    cantidad_gente = models.PositiveSmallIntegerField(blank=True, null=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')

# -------------------- Incumplimiento --------------------
class Incumplimiento(models.Model):
    ESTADOS = [
        ('cancelado', 'Cancelado'),
        ('pendiente', 'Pendiente'),
    ]

    persona = models.ForeignKey(Persona, on_delete=models.CASCADE)
    restriccion = models.ForeignKey(Restriccion, on_delete=models.CASCADE)
    fecha = models.DateField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    observaciones = models.CharField(max_length=500, blank=True, null=True)

# -------------------- Pagos --------------------
class Pagos(models.Model):
    persona = models.ForeignKey(Persona, on_delete=models.SET_NULL, null=True)
    unidad = models.ForeignKey(Unidad, on_delete=models.SET_NULL, null=True)
    monto = models.DecimalField(max_digits=12, decimal_places=2)
    fecha = models.DateField()
    duracion_meses = models.PositiveSmallIntegerField(blank=True, null=True)
    url_foto = models.CharField(max_length=255, blank=True, null=True)
    metodo_pago = models.CharField(max_length=60, blank=True, null=True)

# -------------------- Visitas --------------------
class Visita(models.Model):
    nombre_visitante = models.CharField(max_length=80)
    apellido_paterno = models.CharField(max_length=80)
    apellido_materno = models.CharField(max_length=80, blank=True, null=True)
    telefono = models.CharField(max_length=40)
    fecha_ingreso = models.DateField()
    hora_ingreso = models.TimeField(blank=True, null=True)
    fecha_salida = models.DateField(blank=True, null=True)
    hora_salida = models.TimeField(blank=True, null=True)
    autorizado = models.ForeignKey(Persona, on_delete=models.SET_NULL, null=True, related_name='visitas_autorizadas')
    area_social = models.ForeignKey(AreaSocial, on_delete=models.SET_NULL, null=True, blank=True)
    unidad = models.ForeignKey(Unidad, on_delete=models.SET_NULL, null=True, blank=True)
    motivo = models.CharField(max_length=255, blank=True, null=True)
