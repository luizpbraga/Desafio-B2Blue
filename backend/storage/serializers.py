from rest_framework import serializers
from .models import Station, StationHistory

class StationSerializer(serializers.ModelSerializer):
    """Serializer for the Station model with custom validation"""
    
    def validate_volume_percentage(self, value):
        """Validate that volume percentage is between 0 and 100"""
        if value < 0 or value > 100:
            raise serializers.ValidationError("Volume percentage must be between 0 and 100")
        return value
    
    class Meta:
        model = Station
        fields = '__all__'

class StationHistorySerializer(serializers.ModelSerializer):
    """Serializer for the StationHistory model with additional fields"""
    # Returns the station name in the generated JSON, reducing the number of potential requests
    station_name = serializers.CharField(source='station.name', read_only=True)
    
    class Meta:
        model = StationHistory
        fields = '__all__'
