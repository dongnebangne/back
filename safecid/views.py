from django.conf import settings
from django.http import JsonResponse
from django.views import View
from safecid.models import Address
import requests

SAFEMAP_API_KEY = settings.SAFEMAP_API_KEY
VWORLD_API_KEY = settings.VWORLD_API_KEY

class GetWMSLayer(View):
    def get(self, request):
        category = request.GET.get('category', None)
        subcategory = request.GET.get('subcategory', None)

        print(f"Received category: {category}, subcategory: {subcategory}")

        wms_layers = {
            '범죄주의구간': [
                {'name': '전체',
                 'serverUrl': f'https://www.safemap.go.kr/openApiService/wms/getLayerData.do?apikey={SAFEMAP_API_KEY}',
                 'layername': 'A2SM_CRMNLHSPOT_TOT', 'styles': 'A2SM_CrmnlHspot_Tot_Tot'},
                {'name': '강도',
                 'serverUrl': f'https://www.safemap.go.kr/openApiService/wms/getLayerData.do?apikey={SAFEMAP_API_KEY}',
                 'layername': 'A2SM_CRMNLHSPOT_TOT', 'styles': 'A2SM_CrmnlHspot_Tot_Brglr'},
                {'name': '성폭력',
                 'serverUrl': f'https://www.safemap.go.kr/openApiService/wms/getLayerData.do?apikey={SAFEMAP_API_KEY}',
                 'layername': 'A2SM_CRMNLHSPOT_TOT', 'styles': 'A2SM_CrmnlHspot_Tot_Rape'},
                {'name': '절도',
                 'serverUrl': f'https://www.safemap.go.kr/openApiService/wms/getLayerData.do?apikey={SAFEMAP_API_KEY}',
                 'layername': 'A2SM_CRMNLHSPOT_TOT', 'styles': 'A2SM_CrmnlHspot_Tot_Theft'},
                {'name': '폭력',
                 'serverUrl': f'https://www.safemap.go.kr/openApiService/wms/getLayerData.do?apikey={SAFEMAP_API_KEY}',
                 'layername': 'A2SM_CRMNLHSPOT_TOT', 'styles': 'A2SM_CrmnlHspot_Tot_Violn'},
            ],
            '노인대상범죄주의구간': [
                {'name': '노인대상범죄주의구간',
                 'serverUrl': f'https://www.safemap.go.kr/openApiService/wms/getLayerData.do?apikey={SAFEMAP_API_KEY}',
                 'layername': 'A2SM_ODBLRCRMNLHSPOT_ODSN', 'styles': 'A2SM_OdblrCrmnlHspot_Odsn'},
            ],
            '어린이대상범죄주의구간': [
                {'name': '어린이대상범죄주의구간',
                 'serverUrl': f'https://www.safemap.go.kr/openApiService/wms/getLayerData.do?apikey={SAFEMAP_API_KEY}',
                 'layername': 'A2SM_ODBLRCRMNLHSPOT_KID', 'styles': 'A2SM_OdblrCrmnlHspot_Kid'},
            ],
            '여성밤길치안안전': [
                {'name': '전체',
                 'serverUrl': f'https://www.safemap.go.kr/openApiService/wms/getLayerData.do?apikey={SAFEMAP_API_KEY}',
                 'layername': 'A2SM_CRMNLHSPOT_F1_TOT', 'styles': 'A2SM_OdblrCrmnlHspot_Tot_20_24'},
                {'name': '성폭력',
                 'serverUrl': f'https://www.safemap.go.kr/openApiService/wms/getLayerData.do?apikey={SAFEMAP_API_KEY}',
                 'layername': 'A2SM_CRMNLHSPOT_F1_RAPE', 'styles': 'A2SM_OdblrCrmnlHspot_Rape_20_24'},
                {'name': '폭력',
                 'serverUrl': f'https://www.safemap.go.kr/openApiService/wms/getLayerData.do?apikey={SAFEMAP_API_KEY}',
                 'layername': 'A2SM_CRMNLHSPOT_F1_VIOLN', 'styles': 'A2SM_OdblrCrmnlHspot_Violn_20_24'},
                {'name': '절도',
                 'serverUrl': f'https://www.safemap.go.kr/openApiService/wms/getLayerData.do?apikey={SAFEMAP_API_KEY}',
                 'layername': 'A2SM_CRMNLHSPOT_F1_THEFT', 'styles': 'A2SM_OdblrCrmnlHspot_Theft_20_24'},
                {'name': '강도',
                 'serverUrl': f'https://www.safemap.go.kr/openApiService/wms/getLayerData.do?apikey={SAFEMAP_API_KEY}',
                 'layername': 'A2SM_CRMNLHSPOT_F1_BRGLR', 'styles': 'A2SM_OdblrCrmnlHspot_Brglr_20_24'},
            ],
            '치안사고통계': [
                {'name': '전체',
                 'serverUrl': f'https://www.safemap.go.kr/openApiService/wms/getLayerData.do?apikey={SAFEMAP_API_KEY}',
                 'layername': 'A2SM_CRMNLSTATS', 'styles': 'A2SM_CrmnlStats_Tot'},
                {'name': '마약',
                 'serverUrl': f'https://www.safemap.go.kr/openApiService/wms/getLayerData.do?apikey={SAFEMAP_API_KEY}',
                 'layername': 'A2SM_CRMNLSTATS', 'styles': 'A2SM_CrmnlStats_Nrctc'},
                {'name': '살인',
                 'serverUrl': f'https://www.safemap.go.kr/openApiService/wms/getLayerData.do?apikey={SAFEMAP_API_KEY}',
                 'layername': 'A2SM_CRMNLSTATS', 'styles': 'A2SM_CrmnlStats_Murder'},
                {'name': '도박',
                 'serverUrl': f'https://www.safemap.go.kr/openApiService/wms/getLayerData.do?apikey={SAFEMAP_API_KEY}',
                 'layername': 'A2SM_CRMNLSTATS', 'styles': 'A2SM_CrmnlStats_Gamble'},
                {'name': '강도',
                 'serverUrl': f'https://www.safemap.go.kr/openApiService/wms/getLayerData.do?apikey={SAFEMAP_API_KEY}',
                 'layername': 'A2SM_CRMNLSTATS', 'styles': 'A2SM_CrmnlStats_Brglr'},
                {'name': '성폭력',
                 'serverUrl': f'https://www.safemap.go.kr/openApiService/wms/getLayerData.do?apikey={SAFEMAP_API_KEY}',
                 'layername': 'A2SM_CRMNLSTATS', 'styles': 'A2SM_CrmnlStats_Rape'},
                {'name': '절도',
                 'serverUrl': f'https://www.safemap.go.kr/openApiService/wms/getLayerData.do?apikey={SAFEMAP_API_KEY}',
                 'layername': 'A2SM_CRMNLSTATS', 'styles': 'A2SM_CrmnlStats_Theft'},
                {'name': '약취/유인',
                 'serverUrl': f'https://www.safemap.go.kr/openApiService/wms/getLayerData.do?apikey={SAFEMAP_API_KEY}',
                 'layername': 'A2SM_CRMNLSTATS', 'styles': 'A2SM_CrmnlStats_Tmpt'},
                {'name': '폭력',
                 'serverUrl': f'https://www.safemap.go.kr/openApiService/wms/getLayerData.do?apikey={SAFEMAP_API_KEY}',
                 'layername': 'A2SM_CRMNLSTATS', 'styles': 'A2SM_CrmnlStats_Violn'},
                {'name': '방화',
                 'serverUrl': f'https://www.safemap.go.kr/openApiService/wms/getLayerData.do?apikey={SAFEMAP_API_KEY}',
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


class GetLegend(View):
    def get(self, request):
        layer = request.GET.get('layer')
        style = request.GET.get('style')
        if not layer:
            return JsonResponse({'error': 'Missing layer parameter'}, status=400)

        legend_url = f"http://www.safemap.go.kr/legend/legendApiXml.do?apikey={SAFEMAP_API_KEY}&layer={layer}"
        if style:
            legend_url += f"&style={style}"

        return JsonResponse({'legend_url': legend_url})

class SidoView(View):
    def get(self, request):
        sidos = Address.objects.values_list('sido', flat=True).distinct()
        return JsonResponse(list(sidos), safe=False)

class SidoView(View):
    def get(self, request):
        sidos = Address.objects.values('sido').distinct()
        return JsonResponse(list(sidos), safe=False)

class SigunguView(View):
    def get(self, request, sido):
        sigungus = Address.objects.filter(sido=sido).values('sigungu').distinct()
        return JsonResponse(list(sigungus), safe=False)

class EupmyeondongView(View):
    def get(self, request, sido, sigungu):
        try:
            eupmyeondongs = Address.objects.filter(sido=sido, sigungu=sigungu).values('eupmyeondong').distinct()
            if not eupmyeondongs:
                return JsonResponse({"error": "No data found"}, status=404)
            return JsonResponse(list(eupmyeondongs), safe=False)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

class GetCoordinatesFromAddress(View):
    def get(self, request):
        emdong = request.GET.get('emdong')

        api_url = f'https://api.vworld.kr/req/address'
        params = {
            'service': 'address',
            'request': 'GetCoord',
            'type': 'PARCEL',
            'address': f'{emdong}',
            'key': VWORLD_API_KEY,
        }

        response = requests.get(api_url, params=params)

        data = response.json()
        print(data)  # 응답 데이터 출력
        if 'response' in data and 'result' in data['response']:
            coordinates = data['response']['result']['point']
            return JsonResponse(coordinates, safe=False)
        else:
            return JsonResponse({"error": "Invalid response structure or no data found"}, status=500)

class GetAddressFromCoordinates(View):
    def get(self, request):
        lat = request.GET.get('lat')
        lon = request.GET.get('lon')

        api_url = f'https://api.vworld.kr/req/address'
        params = {
            'service': 'address',
            'request': 'GetAddress',
            'type': 'PARCEL',
            'point': f'{lon},{lat}',
            'key': VWORLD_API_KEY,
        }

        response = requests.get(api_url, params=params)

        if response.status_code == 200:
            data = response.json()
            if 'response' in data and 'result' in data['response']:
                result = data['response']['result'][0]
                structure = result.get('structure', {})
                level1 = structure.get('level1', '')
                level2 = structure.get('level2', '')
                level4A = structure.get('level4A', '')
                address = f'{level1} {level2} {level4A}'
                return JsonResponse({'address': address})
            else:
                return JsonResponse({'error': 'No address found'}, status=404)
        else:
            return JsonResponse({'error': 'Failed to fetch data from the API'}, status=500)
