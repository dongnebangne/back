import csv
from django.core.management.base import BaseCommand
from safecid.models import Address

class Command(BaseCommand):
    help = 'Load addresses from CSV file'

    def handle(self, *args, **kwargs):
        # 절대 경로를 사용하여 CSV 파일 경로 설정
        csv_file_path = 'D:/Programming/safe_cid/back/법정동_데이터.csv'

        # CSV 파일 로드
        with open(csv_file_path, 'r', encoding='cp949') as file:
            reader = csv.reader(file)
            next(reader)  # 헤더 행 건너뛰기
            Address.objects.all().delete()
            for row in reader:
                Address.objects.create(
                    sido=row[0],
                    sigungu=row[1],
                    eupmyeondong=row[2]
                )
        self.stdout.write(self.style.SUCCESS('Successfully loaded addresses'))