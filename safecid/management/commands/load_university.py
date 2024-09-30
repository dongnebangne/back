import csv
from django.core.management.base import BaseCommand
from safecid.models import University
import os
from django.conf import settings

class Command(BaseCommand):
    help = 'Load university from CSV file'

    def handle(self, *args, **kwargs):
        csv_file_path = os.path.join(settings.BASE_DIR, '대학교_데이터.csv')

        # CSV 파일 로드
        with open(csv_file_path, 'r', encoding='utf-8-sig') as file:
            reader = csv.reader(file)
            next(reader)  # 헤더 행 건너뛰기
            University.objects.all().delete()
            for row in reader:
                try:
                    lon = float(row[2]) if row[2] else None
                    lat = float(row[3]) if row[3] else None

                    University.objects.create(
                        univ_name=row[0],
                        location=row[1],
                        lon=lon,
                        lat=lat
                    )
                    print(f"저장된 데이터: {row}")
                except ValueError as e:
                    print(f"잘못된 데이터가 있어서 해당 행을 건너뜁니다: {row}, 오류: {e}")

        self.stdout.write(self.style.SUCCESS('Successfully loaded universities'))