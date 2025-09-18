from rest_framework import serializers
from .models import Persona

class PersonaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Persona
        fields = '__all__'
        #read_only_fields ('',) solo electura, siempre la coma al final
        read_only_feilds=('apellido',)