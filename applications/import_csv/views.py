import csv

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from .tasks import process_csv_file


class CSVReaderView(APIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'file': openapi.Schema(type=openapi.TYPE_FILE),
            },
            required=['file']))
    def post(self, request):
        email = request.user.email
        try:
            csv_file = request.FILES['file']
        except KeyError:
            return Response({"detail": "Файл CSV не найден. Прикрепите csv файл с ключем file"}, status=400)
        decoded_file = csv_file.read().decode('utf-8')
        csv_data = list(csv.DictReader(decoded_file.split()))
        process_csv_file.apply_async(args=(csv_data, email))
        return Response({"detail": "CSV-файл успешно обработан. Идет заполнение БД"})