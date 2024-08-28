import os
from django.conf import settings
from django.http import JsonResponse
from django.views import View
from safecid.models import Address
import requests
import xmltodict


from django.views.decorators.csrf import csrf_exempt
from .models import UploadedImage
#from .ai_processing import process_image_with_sam_and_lama_or_sd
from .ai_processing import generate_masks_with_sam, inpaint_image_with_selected_mask
from .utils import load_img_to_array, save_array_to_img
from pathlib import Path
from .sam_segment import predict_masks_with_sam

BASE_DIR = Path(__file__).resolve().parent.parent
PRETRAINED_MODELS_DIR = BASE_DIR / 'safecid' / 'pretrained_models'

SAFEMAP_API_KEY = settings.SAFEMAP_API_KEY
VWORLD_API_KEY = settings.VWORLD_API_KEY


@csrf_exempt
def generate_masks(request):
    if request.method == 'POST':
        image_file = request.FILES['image']
        point_coords = [float(coord) for coord in request.POST.get('point_coords').split(',')]
        point_labels = [int(label) for label in request.POST.get('point_labels').split(',')]
        dilate_kernel_size = int(request.POST.get('dilate_kernel_size', 15))

        sam_model_type = request.POST.get('sam_model_type', 'vit_h')
        sam_ckpt = PRETRAINED_MODELS_DIR / 'sam_vit_h_4b8939.pth'

        uploaded_image = UploadedImage.objects.create(image=image_file)
        image_path = uploaded_image.image.path

        img = load_img_to_array(image_path)
        mask_file_paths = generate_masks_with_sam(
            img, point_coords, point_labels, dilate_kernel_size, sam_model_type, sam_ckpt
        )

        # Return the full URL for the masks
        return JsonResponse({
            'masks': [
                {
                    'mask_url': f'{settings.MEDIA_URL}results/{Path(mask_path).name}',
                    'masked_image_url': f'{settings.MEDIA_URL}results/{Path(masked_img_path).name}'
                }
                for mask_path, masked_img_path in mask_file_paths
            ]
        })


@csrf_exempt
def inpaint_image(request):
    if request.method == 'POST':
        selected_mask_idx = int(request.POST.get('selected_mask_idx'))
        text_prompt = request.POST.get('text_prompt', '')

        lama_config = PRETRAINED_MODELS_DIR / 'big-lama' / 'config.yaml'
        lama_ckpt = PRETRAINED_MODELS_DIR / 'big-lama' / 'models' / 'lama_model.pth'

        uploaded_image = UploadedImage.objects.latest('id')
        image_path = uploaded_image.image.path
        img = load_img_to_array(image_path)

        inpainted_image_path = inpaint_image_with_selected_mask(
            img, selected_mask_idx, text_prompt, lama_config, lama_ckpt
        )

        return JsonResponse({
            'inpainted_image_url': f'{settings.MEDIA_URL}results/{Path(inpainted_image_path).name}'
        })



# 범죄 유형별 wms 레이어
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


# 범죄 유형별 범례
class GetLegend(View):
    def get(self, request):
        layer = request.GET.get('layer')
        style = request.GET.get('style')

        if not layer or not style:
            return JsonResponse({'error': 'Layer and style parameters are required'}, status=400)

        url = f'http://www.safemap.go.kr/legend/legendApiXml.do?apikey={SAFEMAP_API_KEY}&layer={layer}&style={style}'
        response = requests.get(url)
        if response.status_code == 200:
            data = xmltodict.parse(response.content)
            return JsonResponse(data)
        else:
            return JsonResponse({'error': 'Failed to fetch data'}, status=500)

# 시도 목록
class SidoView(View):
    def get(self, request):
        sidos = Address.objects.values_list('sido', flat=True).distinct()
        return JsonResponse(list(sidos), safe=False)

# 시군구 목록
class SigunguView(View):
    def get(self, request, sido):
        sigungus = Address.objects.filter(sido=sido).values('sigungu').distinct()
        return JsonResponse(list(sigungus), safe=False)


# 읍면동 목록
class EupmyeondongView(View):
    def get(self, request, sido, sigungu):
        try:
            eupmyeondongs = Address.objects.filter(sido=sido, sigungu=sigungu).values('eupmyeondong').distinct()
            if not eupmyeondongs:
                return JsonResponse({"error": "No data found"}, status=404)
            return JsonResponse(list(eupmyeondongs), safe=False)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

# 주소로부터 좌표 변환
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

# 좌표로부터 주소 변환
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
