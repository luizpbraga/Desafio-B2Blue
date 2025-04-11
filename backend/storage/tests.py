from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Station, StationHistory

class StationModelTests(TestCase):
    """Test cases for Station model"""
    
    def test_create_station(self):
        """Test creating a station"""
        station = Station.objects.create(name="Test Station", volume_percentage=50)
        self.assertEqual(station.name, "Test Station")
        self.assertEqual(station.volume_percentage, 50)
        self.assertFalse(station.collection_requested)
    
    def test_station_str_representation(self):
        """Test string representation of a station"""
        station = Station.objects.create(name="Test Station", volume_percentage=50)
        self.assertEqual(str(station), "Test Station - 50%")


class StationHistoryModelTests(TestCase):
    """Test cases for StationHistory model"""
    
    def setUp(self):
        """Set up test data"""
        self.station = Station.objects.create(name="History Test Station", volume_percentage=50)
    
    def test_create_history_record(self):
        """Test creating a history record"""
        history = StationHistory.objects.create(
            station=self.station,
            operation_type="update",
            volume_percentage=60,
            notes="Test update"
        )
        self.assertEqual(history.station, self.station)
        self.assertEqual(history.operation_type, "update")
        self.assertEqual(history.volume_percentage, 60)
        self.assertEqual(history.notes, "Test update")
    
    def test_history_ordering(self):
        """Test that history records are ordered by timestamp in descending order"""
        StationHistory.objects.create(
            station=self.station,
            operation_type="update",
            volume_percentage=60,
            notes="First update"
        )
        StationHistory.objects.create(
            station=self.station,
            operation_type="update",
            volume_percentage=70,
            notes="Second update"
        )
        
        histories = StationHistory.objects.filter(station=self.station)
        self.assertEqual(histories.count(), 2)
        self.assertEqual(histories[0].notes, "Second update")
        self.assertEqual(histories[1].notes, "First update")


class StationAPITests(APITestCase):
    """Test cases for Station API endpoints"""
    
    def setUp(self):
        """Set up test data"""
        self.station = Station.objects.create(name="API Test Station", volume_percentage=50)
        self.list_url = reverse('station-list')
        self.detail_url = reverse('station-detail', args=[self.station.id])
    
    def test_list_stations(self):
        """Test listing all stations"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_create_station(self):
        """Test creating a new station"""
        data = {'name': 'New Station', 'volume_percentage': 30}
        response = self.client.post(self.list_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Station.objects.count(), 2)
        
        # Check if history record was created
        new_station = Station.objects.get(name='New Station')
        history = StationHistory.objects.filter(station=new_station)
        self.assertEqual(history.count(), 1)
        self.assertEqual(history[0].operation_type, 'create')
    
    def test_retrieve_station(self):
        """Test retrieving a station"""
        response = self.client.get(self.detail_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'API Test Station')
    
    def test_update_volume(self):
        """Test updating a station's volume"""
        data = {'name': self.station.name, 'volume_percentage': 75}
        response = self.client.patch(self.detail_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.station.refresh_from_db()
        self.assertEqual(self.station.volume_percentage, 75)
        self.assertFalse(self.station.collection_requested)
        
        # Check if history record was created
        history = StationHistory.objects.filter(station=self.station, operation_type='update')
        self.assertEqual(history.count(), 1)
    
    def test_update_volume_over_threshold(self):
        """Test updating a station's volume above 80% threshold"""
        data = {'name': self.station.name, 'volume_percentage': 85}
        response = self.client.patch(self.detail_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.station.refresh_from_db()
        self.assertEqual(self.station.volume_percentage, 85)
        self.assertTrue(self.station.collection_requested)
        
        # Check if history records were created (update + collection request)
        history = StationHistory.objects.filter(station=self.station)
        self.assertEqual(history.count(), 2)
        self.assertEqual(
            history.filter(operation_type='collection_request').count(), 
            1
        )
    
    def test_confirm_collection(self):
        """Test confirming collection for a station"""
        # First set collection_requested to True
        self.station.volume_percentage = 85
        self.station.collection_requested = True
        self.station.save()
        
        confirm_url = reverse('station-confirm-collection', args=[self.station.id])
        response = self.client.post(confirm_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.station.refresh_from_db()
        self.assertEqual(self.station.volume_percentage, 0)
        self.assertFalse(self.station.collection_requested)
        
        # Check if history record was created
        history = StationHistory.objects.filter(
            station=self.station, 
            operation_type='collection_complete'
        )
        self.assertEqual(history.count(), 1)
    
    def test_confirm_collection_no_request(self):
        """Test confirming collection when no request exists"""
        confirm_url = reverse('station-confirm-collection', args=[self.station.id])
        response = self.client.post(confirm_url)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)


class StationHistoryAPITests(APITestCase):
    """Test cases for StationHistory API endpoints"""
    
    def setUp(self):
        """Set up test data"""
        self.station = Station.objects.create(name="History API Test Station", volume_percentage=50)
        self.history = StationHistory.objects.create(
            station=self.station,
            operation_type="update",
            volume_percentage=60,
            notes="Test update"
        )
        self.list_url = reverse('stationhistory-list')
        self.detail_url = reverse('stationhistory-detail', args=[self.history.id])
    
    def test_list_history(self):
        """Test listing all history records"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
    
    def test_filter_history_by_station(self):
        """Test filtering history by station"""
        # Create another station and history record
        other_station = Station.objects.create(name="Other Station", volume_percentage=40)
        StationHistory.objects.create(
            station=other_station,
            operation_type="update",
            volume_percentage=45,
            notes="Other update"
        )
        
        # Filter by first station
        response = self.client.get(f"{self.list_url}?station_id={self.station.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['station'], self.station.id)
    
    def test_retrieve_history(self):
        """Test retrieving a specific history record"""
        response = self.client.get(self.detail_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['operation_type'], 'update')
        self.assertEqual(response.data['notes'], 'Test update')

