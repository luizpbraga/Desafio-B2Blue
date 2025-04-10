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
        # TODO

class StationHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = StationHistory.objects.all()
    serializer_class = StationHistorySerializer
    
    def get_queryset(self):
        """Permite filtrar o histórico por estação"""
        # TODO
