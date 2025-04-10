from django.core.management.base import BaseCommand
from storage.models import Station

class Command(BaseCommand):
    help = 'Cria as estações iniciais de armazenamento'

    def handle(self, *args, **kwargs):
        # Verificar se já existem estações
        if Station.objects.exists():
            self.stdout.write(self.style.WARNING('Estações já existem no banco de dados.'))
            return
        
        # Criar as três estações iniciais
        stations = [
            Station(name='Estação A', volume_percentage=0),
            Station(name='Estação B', volume_percentage=0),
            Station(name='Estação C', volume_percentage=0),
        ]
        
        Station.objects.bulk_create(stations)
        
        self.stdout.write(self.style.SUCCESS('Estações iniciais criadas com sucesso!'))
