from django.contrib import admin
from .models import Station, StationHistory

@admin.register(Station)
class StationAdmin(admin.ModelAdmin):
    list_display = ('name', 'volume_percentage', 'collection_requested', 'updated_at')
    list_filter = ('collection_requested',)
    search_fields = ('name',)

@admin.register(StationHistory)
class StationHistoryAdmin(admin.ModelAdmin):
    list_display = ('station', 'operation_type', 'volume_percentage', 'timestamp')
    list_filter = ('operation_type', 'station')
    search_fields = ('station__name', 'operation_type')
