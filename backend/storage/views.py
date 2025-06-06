from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Station, StationHistory
from .serializers import StationSerializer, StationHistorySerializer
from .pagination import StandardResultsSetPagination

class StationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing storage stations.

    Provides standard CRUD operations for Station objects
    with additional collection management functionality.
    """

    queryset = Station.objects.all()
    serializer_class = StationSerializer

    def perform_create(self, serializer):
        """Create a new station and record creation in history"""

        station = serializer.save()
        StationHistory.objects.create(
            station=station,
            operation_type='create',
            volume_percentage=station.volume_percentage,
            notes='Estação criada'
        )

    def perform_update(self, serializer):
        """
        Update station volume and automatically manage collection requests
        when threshold is exceeded.
        """

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

    @action(detail=True, methods=['post'])
    def confirm_collection(self, request, pk=None):
        """
        Confirm waste collection for a station.
        
        Resets the station's volume to zero and marks collection as complete.
        Returns 400 if no collection was previously requested.
        """

        station = self.get_object()
        
        if not station.collection_requested:
            return Response(
                {'error': 'Não há pedido de coleta para esta estação.'},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        old_percentage = station.volume_percentage
        station.volume_percentage = 0
        station.collection_requested = False
        station.save()
        
        # Registrar a coleta no histórico
        StationHistory.objects.create(
            station=station,
            operation_type='collection_complete',
            volume_percentage=0,
            notes=f'Coleta confirmada. Volume anterior: {old_percentage}%'
        )
        
        return Response({
            'success': True,
            'message': 'Coleta confirmada com sucesso.',
            'station': StationSerializer(station).data
        })

class StationHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing station history records.
    
    Provides read-only access to history with filtering capabilities.
    """

    queryset = StationHistory.objects.all()
    serializer_class = StationHistorySerializer
    # pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        """
        Return filtered history records based on query parameters.
        
        Supports filtering by station_id.
        """

        queryset = StationHistory.objects.all()
        station_id = self.request.query_params.get('station_id', None)
        
        if station_id is not None:
            queryset = queryset.filter(station_id=station_id)
            
        return queryset
