from django.urls import path
from .views import GetWMSLayer, get_sido, get_sigungu, get_emdong, get_coordinates
#from .views import GenerateImage
#from .views import generate_image
#from . import views
from .views import generate_image, get_prediction_status

urlpatterns = [
    path('api/get-wms-layer/', GetWMSLayer.as_view(), name='get-wms-layer'),
    path('api/sido/', get_sido, name='get_sido'),
    path('api/sigungu/', get_sigungu, name='get_sigungu'),
    path('api/emdong/', get_emdong, name='get_emdong'),
    path('api/coordinates/', get_coordinates, name='get_coordinates'),
    #path('api/generate-image/', GenerateImage.as_view(), name='generate_image'),
    #path('api/generate-image/', generate_image, name='generate_image'),
    #path('api/generate-image/', views.generate_image, name='generate_image'),
    #path('api/get-prediction/<str:id>/', views.get_prediction, name='get_prediction'),
    path('api/generate-image/', generate_image, name='generate_image'),
    path('api/predictions/<str:prediction_id>/', get_prediction_status, name='get_prediction_status'),
]
