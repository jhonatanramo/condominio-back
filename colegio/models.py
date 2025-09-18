from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone

class Pais(models.Model):
    nombre = models.CharField(max_length=100)
    codigo = models.CharField(max_length=10, blank=True, null=True)
    
    def __str__(self):
        return self.nombre

class Rol(models.Model):
    nombre = models.CharField(max_length=60)
    
    def __str__(self):
        return self.nombre

class Persona(models.Model):
    ci = models.CharField(max_length=40, blank=True, null=True)
    nombre = models.CharField(max_length=80)
    apellido_paterno = models.CharField(max_length=80, blank=True, null=True)
    apellido_materno = models.CharField(max_length=80, blank=True, null=True)
    fecha_creada = models.DateField(default=timezone.now)
    pais = models.ForeignKey(Pais, on_delete=models.SET_NULL, null=True, blank=True)
    telefono = models.CharField(max_length=40, blank=True, null=True)
    email = models.EmailField(max_length=100, blank=True, null=True)
    roles = models.ManyToManyField(Rol, through='RolPersona')
    
    def __str__(self):
        return f"{self.nombre} {self.apellido_paterno or ''}"

class RolPersona(models.Model):
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE)
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE)
    fecha_asignada = models.DateField(default=timezone.now)
    
    class Meta:
        unique_together = ['persona', 'rol']
    
    def __str__(self):
        return f"{self.persona} - {self.rol}"

class Condominio(models.Model):
    nombre = models.CharField(max_length=120)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    administrador = models.ForeignKey(Persona, on_delete=models.SET_NULL, null=True, blank=True, related_name='condominios_administrados')
    
    def __str__(self):
        return self.nombre

class Unidad(models.Model):
    condominio = models.ForeignKey(Condominio, on_delete=models.CASCADE)
    propietario = models.ForeignKey(Persona, on_delete=models.SET_NULL, null=True, blank=True, related_name='unidades_propiedad')
    nro_modulo = models.PositiveSmallIntegerField()
    nro_piso = models.PositiveSmallIntegerField()
    nro_habitacion = models.PositiveSmallIntegerField()
    valor_mensual = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    capacidad = models.PositiveSmallIntegerField()
    nro_contrato = models.CharField(max_length=80, blank=True, null=True)
    
    def __str__(self):
        return f"{self.condominio} - M{self.nro_modulo}P{self.nro_piso}H{self.nro_habitacion}"
    
    class Meta:
        indexes = [
            models.Index(fields=['nro_modulo', 'nro_piso', 'nro_habitacion'])
        ]

class AreaSocial(models.Model):
    nombre = models.CharField(max_length=120)
    ubicacion = models.CharField(max_length=255, blank=True, null=True)
    hora_inicio_permitido = models.TimeField()
    hora_fin_permitido = models.TimeField()
    capacidad_maxima = models.PositiveSmallIntegerField()
    restricciones = models.ManyToManyField('Restriccion', through='RestriccionArea')
    
    def __str__(self):
        return self.nombre

class Restriccion(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(max_length=500, blank=True, null=True)
    
    def __str__(self):
        return self.nombre

class RestriccionArea(models.Model):
    restriccion = models.ForeignKey(Restriccion, on_delete=models.CASCADE)
    area_social = models.ForeignKey(AreaSocial, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ['restriccion', 'area_social']
    
    def __str__(self):
        return f"{self.restriccion} - {self.area_social}"

class Reserva(models.Model):
    ESTADO_CHOICES = [
        ('confirmada', 'Confirmada'),
        ('cancelada', 'Cancelada'),
        ('pendiente', 'Pendiente'),
    ]
    
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE)
    area_social = models.ForeignKey(AreaSocial, on_delete=models.CASCADE)
    horario_inicio = models.TimeField()
    horario_fin = models.TimeField()
    fecha = models.DateField()
    cantidad_gente = models.PositiveSmallIntegerField()
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='pendiente')
    
    def __str__(self):
        return f"{self.persona} - {self.area_social} - {self.fecha}"
    
    class Meta:
        indexes = [
            models.Index(fields=['fecha'])
        ]
    
    def clean(self):
        # Validaciones similares al procedimiento almacenado
        if self.horario_inicio < self.area_social.hora_inicio_permitido or self.horario_fin > self.area_social.hora_fin_permitido:
            raise ValidationError('Horario fuera del rango permitido')
        
        if self.cantidad_gente > self.area_social.capacidad_maxima:
            raise ValidationError('La cantidad de personas excede la capacidad del área')
        
        # Verificar solapamiento de reservas
        reservas_solapadas = Reserva.objects.filter(
            area_social=self.area_social,
            fecha=self.fecha,
            estado='confirmada'
        ).exclude(pk=self.pk).filter(
            models.Q(horario_inicio__range=(self.horario_inicio, self.horario_fin)) |
            models.Q(horario_fin__range=(self.horario_inicio, self.horario_fin)) |
            models.Q(horario_inicio__lte=self.horario_inicio, horario_fin__gte=self.horario_fin)
        )
        
        if reservas_solapadas.exists():
            raise ValidationError('Ya existe una reserva en el horario seleccionado')

class Incumplimiento(models.Model):
    ESTADO_CHOICES = [
        ('cancelado', 'Cancelado'),
        ('pendiente', 'Pendiente'),
    ]
    
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE)
    restriccion = models.ForeignKey(Restriccion, on_delete=models.CASCADE)
    fecha = models.DateField(default=timezone.now)
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='pendiente')
    observaciones = models.TextField(max_length=500, blank=True, null=True)
    
    def __str__(self):
        return f"{self.persona} - {self.restriccion} - {self.fecha}"
    
    class Meta:
        indexes = [
            models.Index(fields=['persona'])
        ]

class Pago(models.Model):
    persona = models.ForeignKey(Persona, on_delete=models.SET_NULL, null=True, blank=True)
    unidad = models.ForeignKey(Unidad, on_delete=models.SET_NULL, null=True, blank=True)
    monto = models.DecimalField(max_digits=12, decimal_places=2)
    fecha = models.DateField()
    duracion_meses = models.PositiveSmallIntegerField()
    url_foto = models.URLField(max_length=255, blank=True, null=True)
    metodo_pago = models.CharField(max_length=60, blank=True, null=True)
    
    def __str__(self):
        return f"{self.persona} - {self.monto} - {self.fecha}"
    
    class Meta:
        indexes = [
            models.Index(fields=['fecha'])
        ]

class Visita(models.Model):
    nombre_visitante = models.CharField(max_length=80)
    apellido_paterno = models.CharField(max_length=80)
    apellido_materno = models.CharField(max_length=80, blank=True, null=True)
    telefono = models.CharField(max_length=40)
    fecha_ingreso = models.DateField()
    hora_ingreso = models.TimeField(blank=True, null=True)
    fecha_salida = models.DateField(blank=True, null=True)
    hora_salida = models.TimeField(blank=True, null=True)
    autorizado_por = models.ForeignKey(Persona, on_delete=models.SET_NULL, null=True, blank=True, related_name='visitas_autorizadas')
    area_social = models.ForeignKey(AreaSocial, on_delete=models.SET_NULL, null=True, blank=True)
    unidad = models.ForeignKey(Unidad, on_delete=models.SET_NULL, null=True, blank=True)
    motivo = models.CharField(max_length=255, blank=True, null=True)
    
    def __str__(self):
        return f"{self.nombre_visitante} {self.apellido_paterno} - {self.fecha_ingreso}"
    
    class Meta:
        indexes = [
            models.Index(fields=['fecha_ingreso'])
        ]