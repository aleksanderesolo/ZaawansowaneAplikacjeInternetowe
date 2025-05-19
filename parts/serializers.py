from rest_framework import serializers
from .models import Part
from .models import Ocena
from .models import Samochod, Ocena

class PartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Part
        fields = '__all__'

class OcenaSerializer(serializers.ModelSerializer):
    #part_nazwa = serializers.CharField(source='part.nazwa', read_only=True)

    class Meta:
        model = Ocena
        fields = '__all__'

class SamochodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Samochod
        fields = '__all__'