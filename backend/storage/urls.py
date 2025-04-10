from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StationViewSet, StationHistoryViewSet

router = DefaultRouter()
router.register(r'stations', StationViewSet)
router.register(r'history', StationHistoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

