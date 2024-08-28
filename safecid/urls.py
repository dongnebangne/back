from django.urls import path
from .views import (GetWMSLayer, GetLegend, SidoView, SigunguView, EupmyeondongView,
                    LocationView, UniversityView, UniversityCoordinates, GetCoordinatesFromAddress, GetAddressFromCoordinates)

urlpatterns = [
    path('get-wms-layer/', GetWMSLayer.as_view(), name='get-wms-layer'),
    path('get-legend/', GetLegend.as_view(), name='get-legend-url'),
    path('sido/', SidoView.as_view(), name='sido-list'),
    path('sigungu/<str:sido>/', SigunguView.as_view(), name='sigungu-list'),
    path('eupmyeondong/<str:sido>/<str:sigungu>/', EupmyeondongView.as_view(), name='eupmyeondong-list'),
    path('locations/', LocationView.as_view(), name='location-list'),
    path('universities/<str:location>/', UniversityView.as_view(), name='university-list'),
    path('university/coordinates/<str:name>/', UniversityCoordinates.as_view(), name='university-coordinates'),
    path('coordinates/', GetCoordinatesFromAddress.as_view(), name='get_coordinates'),
    path('address/', GetAddressFromCoordinates.as_view(), name='get_address')
]
