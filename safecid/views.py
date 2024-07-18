from django.conf import settings
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponse
from django.views import View
import requests
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.core.files.uploadedfile import InMemoryUploadedFile
import base64
import json
import replicate
from PIL import Image
import io
from io import BytesIO
from rest_framework.decorators import api_view
from utils.add_background_to_png import add_background_to_png

API_KEY = settings.API_KEY

#REPLICATE_API_TOKEN = os.getenv('REPLICATE_API_TOKEN')
REPLICATE_API_HOST = "https://api.replicate.com"
REPLICATE_API_TOKEN = settings.REPLICATE_API_TOKEN

class GetWMSLayer(View):
    def get(self, request):
        category = request.GET.get('category', None)
        subcategory = request.GET.get('subcategory', None)

        print(f"Received category: {category}, subcategory: {subcategory}")

        wms_layers = {
            '범죄주의구간': [
                {'name': '전체',
                 'serverUrl': f'https://www.safemap.go.kr/openApiService/wms/getLayerData.do?apikey={API_KEY}',
                 'layername': 'A2SM_CRMNLHSPOT_TOT', 'styles': 'A2SM_CrmnlHspot_Tot_Tot'},
                {'name': '강도',
                 'serverUrl': f'https://www.safemap.go.kr/openApiService/wms/getLayerData.do?apikey={API_KEY}',
                 'layername': 'A2SM_CRMNLHSPOT_TOT', 'styles': 'A2SM_CrmnlHspot_Tot_Brglr'},
                {'name': '성폭력',
                 'serverUrl': f'https://www.safemap.go.kr/openApiService/wms/getLayerData.do?apikey={API_KEY}',
                 'layername': 'A2SM_CRMNLHSPOT_TOT', 'styles': 'A2SM_CrmnlHspot_Tot_Rape'},
                {'name': '절도',
                 'serverUrl': f'https://www.safemap.go.kr/openApiService/wms/getLayerData.do?apikey={API_KEY}',
                 'layername': 'A2SM_CRMNLHSPOT_TOT', 'styles': 'A2SM_CrmnlHspot_Tot_Theft'},
                {'name': '폭력',
                 'serverUrl': f'https://www.safemap.go.kr/openApiService/wms/getLayerData.do?apikey={API_KEY}',
                 'layername': 'A2SM_CRMNLHSPOT_TOT', 'styles': 'A2SM_CrmnlHspot_Tot_Violn'},
            ],
            '노인대상범죄주의구간': [
                {'name': '노인대상범죄주의구간',
                 'serverUrl': f'https://www.safemap.go.kr/openApiService/wms/getLayerData.do?apikey={API_KEY}',
                 'layername': 'A2SM_ODBLRCRMNLHSPOT_ODSN', 'styles': 'A2SM_OdblrCrmnlHspot_Odsn'},
            ],
            '어린이대상범죄주의구간': [
                {'name': '어린이대상범죄주의구간',
                 'serverUrl': f'https://www.safemap.go.kr/openApiService/wms/getLayerData.do?apikey={API_KEY}',
                 'layername': 'A2SM_ODBLRCRMNLHSPOT_KID', 'styles': 'A2SM_OdblrCrmnlHspot_Kid'},
            ],
            '여성밤길치안안전': [
                {'name': '전체',
                 'serverUrl': f'https://www.safemap.go.kr/openApiService/wms/getLayerData.do?apikey={API_KEY}',
                 'layername': 'A2SM_CRMNLHSPOT_F1_TOT', 'styles': 'A2SM_OdblrCrmnlHspot_Tot_20_24'},
                {'name': '성폭력',
                 'serverUrl': f'https://www.safemap.go.kr/openApiService/wms/getLayerData.do?apikey={API_KEY}',
                 'layername': 'A2SM_CRMNLHSPOT_F1_RAPE', 'styles': 'A2SM_OdblrCrmnlHspot_Rape_20_24'},
                {'name': '폭력',
                 'serverUrl': f'https://www.safemap.go.kr/openApiService/wms/getLayerData.do?apikey={API_KEY}',
                 'layername': 'A2SM_CRMNLHSPOT_F1_VIOLN', 'styles': 'A2SM_OdblrCrmnlHspot_Violn_20_24'},
                {'name': '절도',
                 'serverUrl': f'https://www.safemap.go.kr/openApiService/wms/getLayerData.do?apikey={API_KEY}',
                 'layername': 'A2SM_CRMNLHSPOT_F1_THEFT', 'styles': 'A2SM_OdblrCrmnlHspot_Theft_20_24'},
                {'name': '강도',
                 'serverUrl': f'https://www.safemap.go.kr/openApiService/wms/getLayerData.do?apikey={API_KEY}',
                 'layername': 'A2SM_CRMNLHSPOT_F1_BRGLR', 'styles': 'A2SM_OdblrCrmnlHspot_Brglr_20_24'},
            ],
            '치안사고통계': [
                {'name': '전체',
                 'serverUrl': f'https://www.safemap.go.kr/openApiService/wms/getLayerData.do?apikey={API_KEY}',
                 'layername': 'A2SM_CRMNLSTATS', 'styles': 'A2SM_CrmnlStats_Tot'},
                {'name': '마약',
                 'serverUrl': f'https://www.safemap.go.kr/openApiService/wms/getLayerData.do?apikey={API_KEY}',
                 'layername': 'A2SM_CRMNLSTATS', 'styles': 'A2SM_CrmnlStats_Nrctc'},
                {'name': '살인',
                 'serverUrl': f'https://www.safemap.go.kr/openApiService/wms/getLayerData.do?apikey={API_KEY}',
                 'layername': 'A2SM_CRMNLSTATS', 'styles': 'A2SM_CrmnlStats_Murder'},
                {'name': '도박',
                 'serverUrl': f'https://www.safemap.go.kr/openApiService/wms/getLayerData.do?apikey={API_KEY}',
                 'layername': 'A2SM_CRMNLSTATS', 'styles': 'A2SM_CrmnlStats_Gamble'},
                {'name': '강도',
                 'serverUrl': f'https://www.safemap.go.kr/openApiService/wms/getLayerData.do?apikey={API_KEY}',
                 'layername': 'A2SM_CRMNLSTATS', 'styles': 'A2SM_CrmnlStats_Brglr'},
                {'name': '성폭력',
                 'serverUrl': f'https://www.safemap.go.kr/openApiService/wms/getLayerData.do?apikey={API_KEY}',
                 'layername': 'A2SM_CRMNLSTATS', 'styles': 'A2SM_CrmnlStats_Rape'},
                {'name': '절도',
                 'serverUrl': f'https://www.safemap.go.kr/openApiService/wms/getLayerData.do?apikey={API_KEY}',
                 'layername': 'A2SM_CRMNLSTATS', 'styles': 'A2SM_CrmnlStats_Theft'},
                {'name': '약취/유인',
                 'serverUrl': f'https://www.safemap.go.kr/openApiService/wms/getLayerData.do?apikey={API_KEY}',
                 'layername': 'A2SM_CRMNLSTATS', 'styles': 'A2SM_CrmnlStats_Tmpt'},
                {'name': '폭력',
                 'serverUrl': f'https://www.safemap.go.kr/openApiService/wms/getLayerData.do?apikey={API_KEY}',
                 'layername': 'A2SM_CRMNLSTATS', 'styles': 'A2SM_CrmnlStats_Violn'},
                {'name': '방화',
                 'serverUrl': f'https://www.safemap.go.kr/openApiService/wms/getLayerData.do?apikey={API_KEY}',
                 'layername': 'A2SM_CRMNLSTATS', 'styles': 'A2SM_CrmnlStats_Arson'}
            ]
        }

        if category and subcategory:
            filtered_layers = [layer for layer in wms_layers.get(category, []) if layer['name'] == subcategory]
        elif category:
            filtered_layers = wms_layers.get(category, [])
        else:
            filtered_layers = []

        return JsonResponse(filtered_layers, safe=False)

def get_sido(request):
    response = requests.get(f'https://api.vworld.kr/req/data?service=data&request=GetFeature&data=LT_C_ADSIDO_INFO&key={API_KEY}&domain=localhost')
    data = response.json()
    sido_list = [feature['properties']['sido_nm'] for feature in data['response']['result']['featureCollection']['features']]
    return JsonResponse(sido_list, safe=False)

def get_sigungu(request):
    sido = request.GET.get('sido')
    response = requests.get(f'https://api.vworld.kr/req/data?service=data&request=GetFeature&data=LT_C_ADSIGG_INFO&key={API_KEY}&domain=localhost&attrFilter=ctp_kor_nm:like:{sido}')
    data = response.json()
    sigungu_list = [feature['properties']['sig_kor_nm'] for feature in data['response']['result']['featureCollection']['features']]
    return JsonResponse(sigungu_list, safe=False)

def get_emdong(request):
    sigungu = request.GET.get('sigungu')
    response = requests.get(f'https://api.vworld.kr/req/data?service=data&request=GetFeature&data=LT_C_ADEMD_INFO&key={API_KEY}&domain=localhost&attrFilter=signgu_nm:like:{sigungu}')
    data = response.json()
    emdong_list = [feature['properties']['emd_kor_nm'] for feature in data['response']['result']['featureCollection']['features']]
    return JsonResponse(emdong_list, safe=False)

def get_coordinates(request):
    emdong = request.GET.get('emdong')
    response = requests.get(f'https://api.vworld.kr/req/data?service=data&request=GetFeature&data=LT_C_ADEMD_INFO&key={API_KEY}&domain=localhost&attrFilter=emd_kor_nm:like:{emdong}')
    data = response.json()
    feature = data['response']['result']['featureCollection']['features'][0]
    coordinates = feature['geometry']['coordinates']
    return JsonResponse(coordinates, safe=False)


@csrf_exempt
def generate_image(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            prompt = data.get('prompt')
            init_image = data.get('init_image')
            mask = data.get('mask')

            response = requests.post(
                'https://api.replicate.com/v1/predictions',
                headers={
                    'Authorization': f'Token {REPLICATE_API_TOKEN}',
                    'Content-Type': 'application/json',
                },
                json={
                    'version': 'a826166bdfbd1c12981a2e914120aa8c19ab2b5474ff8c70f4e2923e6d6596cc',
                    'input': {
                        'prompt': prompt,
                        'init_image': init_image,
                        'mask': mask,
                    },
                },
            )

            return JsonResponse(response.json())
        except Exception as e:
            print(f"Error: {e}")
            return HttpResponse(status=500, content=f"Error: {e}")

@csrf_exempt
def get_prediction_status(request, prediction_id):
    try:
        response = requests.get(
            f'https://api.replicate.com/v1/predictions/{prediction_id}',
            headers={
                'Authorization': f'Token {REPLICATE_API_TOKEN}',
            },
        )
        return JsonResponse(response.json())
    except Exception as e:
        print(f"Error: {e}")
        return HttpResponse(status=500, content=f"Error: {e}")

