from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Station, StationHistory
from .serializers import StationSerializer, StationHistorySerializer

class StationViewSet(viewsets.ModelViewSet):
    queryset = Station.objects.all()
    serializer_class = StationSerializer

    def perform_create(self, serializer):
        """Criar uma nova estação e registrar no histórico"""
        station = serializer.save()
        StationHistory.objects.create(
            station=station,
            operation_type='create',
            volume_percentage=station.volume_percentage,
            notes='Estação criada'
        )

    def perform_update(self, serializer):
        """Atualizar o volume da estação e verificar se precisa solicitar coleta"""
        old_percentage = self.get_object().volume_percentage
        station = serializer.save()
        new_percentage = station.volume_percentage
        
        # Registrar a atualização no histórico
        StationHistory.objects.create(
            station=station,
            operation_type='update',
            volume_percentage=new_percentage,
            notes=f'Volume atualizado de {old_percentage}% para {new_percentage}%'
        )

       # Verificar se precisa solicitar coleta (80% ou mais)
        if new_percentage >= 80 and not station.collection_requested:
            station.collection_requested = True
            station.save()
            
            StationHistory.objects.create(
                station=station,
                operation_type='collection_request',
                volume_percentage=new_percentage,
                notes='Pedido de coleta gerado automaticamente'
            )

class StationHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = StationHistory.objects.all()
    serializer_class = StationHistorySerializer
    
    def get_queryset(self):
        """Permite filtrar o histórico por estação"""
        queryset = StationHistory.objects.all()
        station_id = self.request.query_params.get('station_id', None)
        
        if station_id is not None:
            queryset = queryset.filter(station_id=station_id)
            
        return queryset
