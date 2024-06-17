from django.conf import settings
from django.http import JsonResponse
from django.views import View
import requests

API_KEY = settings.API_KEY

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
