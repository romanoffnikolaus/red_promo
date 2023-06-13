from rest_framework.test import APITestCase, APIRequestFactory
from rest_framework import status

from .models import Book
from applications.rent.models import Rent
from applications.account.models import Renters
from .views import BookViewset


class BookTest(APITestCase):
    
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = Renters.objects.create(
            email = 'pimp@gmail.com',
            adress = 'adress',
            name = 'name',
        )
    
        self.book = Book.objects.create(
            title='Book Title',
            vendor_code='10000',
            author='Book Author',
            year=2022,
            added='2022-01-01',
            quantity=10,
            rented=0,
            out_of_stock=False,
        )
    
    def test_rent_success(self):
        slug = self.book.slug
        tenant_email = self.user.email
        data = {'expiration_date': '2022-06-30', 'tenant_email': f'{tenant_email}'}
        request = self.factory.post(f'books/{slug}/rent/', data, format='json')
        view = BookViewset.as_view({'post': 'rent'})
        response = view(request, pk=slug)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        rent = Rent.objects.get(book=self.book, tenant=self.user)
        self.assertEqual(rent.book, self.book)
        self.assertEqual(rent.tenant, self.user)
        self.assertEqual(str(rent.expiration_date), '2022-06-30')
    
    def test_rend_back(self):
        slug = self.book.slug
        tenant_email = self.user.email
        data = {'expiration_date': '2022-06-30', 'tenant_email': f'{tenant_email}'}
        request = self.factory.post(f'books/{slug}/rent/', data, format='json')
        view = BookViewset.as_view({'post': 'rent'})
        response = view(request, pk=slug)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = {'expiration_date': '2022-06-30', 'tenant_email': f'{tenant_email}'}
        request = self.factory.post(f'books/{slug}/rent_back/', data, format='json')
        view = BookViewset.as_view({'post': 'rent_back'})
        response = view(request, pk=slug)
        self.assertEqual(response.status_code, status.HTTP_200_OK)