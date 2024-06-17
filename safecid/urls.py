from django.urls import path
from .views import GetWMSLayer

urlpatterns = [
    path('api/get-wms-layer/', GetWMSLayer.as_view(), name='get-wms-layer')
]
