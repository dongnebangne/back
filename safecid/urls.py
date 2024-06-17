from django.urls import path
from .views import GetWMSLayer, get_sido, get_sigungu, get_emdong, get_coordinates

urlpatterns = [
    path('api/get-wms-layer/', GetWMSLayer.as_view(), name='get-wms-layer'),
    path('api/sido/', get_sido, name='get_sido'),
    path('api/sigungu/', get_sigungu, name='get_sigungu'),
    path('api/emdong/', get_emdong, name='get_emdong'),
    path('api/coordinates/', get_coordinates, name='get_coordinates'),
]
