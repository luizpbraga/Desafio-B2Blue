from django.db import models

class Station(models.Model):
    """Modelo para representar uma estação de armazenamento de resíduos"""
    name = models.CharField(max_length=100)
    volume_percentage = models.FloatField(default=0)
    collection_requested = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.volume_percentage}%"

class StationHistory(models.Model):
    """Modelo para armazenar o histórico de operações das estações"""
    station = models.ForeignKey(Station, on_delete=models.CASCADE, related_name='history')
    operation_type = models.CharField(max_length=50)  # 'update', 'collection_request', 'collection_complete'
    volume_percentage = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.station.name} - {self.operation_type} - {self.timestamp}"

    class Meta:
        """Os registros serão ordenados pelo campo timestamp em ordem decrescente"""
        ordering = ['-timestamp']
