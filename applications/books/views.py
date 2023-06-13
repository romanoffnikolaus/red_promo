from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
import django_filters
from rest_framework import filters
from django.db.models import Min
from django.db import transaction, IntegrityError
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from .models import Book
from .serialisers import BookSeriliser
from applications.account.models import Renters
from applications.rent.models import Rent
from applications.rent.serialisers import RentSerialiser



class BookViewset(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSeriliser
    filter_backends = [
        django_filters.rest_framework.DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter]
    filterset_fields = ['author', 'title']
    search_fields = ['title', 'author', 'vendor_code']
    ordering_fields = ['added', 'quantity']

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'tenant_email': openapi.Schema(type=openapi.TYPE_STRING),
                'expiration_date': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE),
            },
            required=['tenant_email', 'expiration_date']))
    @action(detail=True, methods=['post'])
    @transaction.atomic
    def rent(self, request, pk=None):
        book = self.get_object()
        renter_email = request.data.get('tenant_email')
        try:
            tenant = Renters.objects.get(email=renter_email)
        except Renters.DoesNotExist:
            return Response("Арендатор не найден", status=400)
        try:
            expiration_date = request.data.get('expiration_date')
            if not expiration_date:
                raise ValueError("Укажите дату ожидаемого возврата")
        except ValueError as e:
            return Response(str(e), status=400)
        if Rent.objects.filter(book=book, tenant=tenant).exists():
            return Response({"detail": "Книга уже взята в аренду"}, status=400)
        available_quantity = book.quantity - book.rented
        if available_quantity <= 0:
            nearest_date = Rent.objects.aggregate(nearest_date=Min('expiration_date'))['nearest_date']
            return Response({"detail": f"Книга недоступна для аренды. Ближайшая доступная дата: {nearest_date}"}, status=400)
        try:
            rent = Rent.objects.create(book=book, tenant=tenant, expiration_date=expiration_date)
        except IntegrityError:
            return Response("Вы уже взяли данную книгу в аренду", status=400)
        book.rented += 1
        if book.rented >= book.quantity:
            book.out_of_stock = True
        book.save()
        serializer = RentSerialiser(rent)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'tenant_email': openapi.Schema(type=openapi.TYPE_STRING)},
            required=['tenant_email']))
    @action(detail=True, methods=['post'])
    @transaction.atomic
    def rent_back(self, request, pk=None):
        book = self.get_object()
        renter_email = request.data.get('tenant_email')
        try:
            tenant = Renters.objects.get(email=renter_email)
        except Renters.DoesNotExist:
            return Response("Арендатор не найден", status=400)
        
        try:
            rent = Rent.objects.get(book=book, tenant=tenant)
        except Rent.DoesNotExist:
            return Response("Вы не арендовали данную книгу", status=400)
        rent.delete()
        book.rented -= 1
        available_quantity = book.quantity - book.rented
        if book.out_of_stock == True and available_quantity > 0:
            book.out_of_stock = False
        book.save()
        return Response("Книга успешно возвращена")
            