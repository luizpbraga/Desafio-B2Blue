from rest_framework import serializers
from .models import Station, StationHistory

class StationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Station
        fields = '__all__'

class StationHistorySerializer(serializers.ModelSerializer):
    # Faz com que o nome da estação seja retornado no JSON gerado, diminuindo 
    # o numero de potencias requisicoes!
    station_name = serializers.CharField(source='station.name', read_only=True)
    
    class Meta:
        model = StationHistory
        fields = '__all__'

