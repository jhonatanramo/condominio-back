# colegio/serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    Pais, Rol, Persona, RolPersona, Condominio, Unidad, AreaSocial,
    Restriccion, RestriccionArea, Reserva, Incumplimiento, Pagos, Visita
)

# -------------------- User --------------------
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

# -------------------- País --------------------
class PaisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pais
        fields = '__all__'

# -------------------- Rol --------------------
class RolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rol
        fields = '__all__'

# -------------------- Persona --------------------
class PersonaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Persona
        fields = '__all__'

# -------------------- RolPersona --------------------
class RolPersonaSerializer(serializers.ModelSerializer):
    class Meta:
        model = RolPersona
        fields = '__all__'

# -------------------- Condominio --------------------
class CondominioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Condominio
        fields = '__all__'

# -------------------- Unidad --------------------
class UnidadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unidad
        fields = '__all__'

# -------------------- Área Social --------------------
class AreaSocialSerializer(serializers.ModelSerializer):
    class Meta:
        model = AreaSocial
        fields = '__all__'

# -------------------- Restricción --------------------
class RestriccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restriccion
        fields = '__all__'

# -------------------- Restriccion-Área --------------------
class RestriccionAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestriccionArea
        fields = '__all__'

# -------------------- Reserva --------------------
class ReservaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reserva
        fields = '__all__'

# -------------------- Incumplimiento --------------------
class IncumplimientoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Incumplimiento
        fields = '__all__'

# -------------------- Pagos --------------------
class PagosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pagos
        fields = '__all__'

# -------------------- Visitas --------------------
class VisitaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visita
        fields = '__all__'
