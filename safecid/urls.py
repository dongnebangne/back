from django.urls import path
from .views import GetWMSLayer, GetLegend, SidoView, SigunguView, EupmyeondongView, GetCoordinatesFromAddress, GetAddressFromCoordinates
from . import views


urlpatterns = [
    path('get-wms-layer/', GetWMSLayer.as_view(), name='get-wms-layer'),
    path('get-legend/', GetLegend.as_view(), name='get-legend-url'),
    path('sido/', SidoView.as_view(), name='sido-list'),
    path('sigungu/<str:sido>/', SigunguView.as_view(), name='sigungu-list'),
    path('eupmyeondong/<str:sido>/<str:sigungu>/', EupmyeondongView.as_view(), name='eupmyeondong-list'),
    path('coordinates/', GetCoordinatesFromAddress.as_view(), name='get_coordinates'),
    path('address/', GetAddressFromCoordinates.as_view(), name='get_address'),
    #path('process-image/', views.process_image, name='process_image'),
    path('generate-masks/', views.generate_masks, name='generate_masks'),
    path('inpaint-image/', views.inpaint_image, name='inpaint_image'),
]
