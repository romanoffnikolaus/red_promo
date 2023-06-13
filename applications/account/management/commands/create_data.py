from django.core.management.base import BaseCommand
from django.utils.text import slugify

from applications.books.models import Book
from applications.account.models import Renters
from applications.rent.models import Rent


class Command(BaseCommand):

    help = 'Creates test data'

    def handle(self, *args, **kwargs):
        '''Создание 6 читателей'''
        test_data = [
            {'name': 'Jonny', 'email': 'Jonny@example.com', 'adress': 'random city'},
            {'name': 'Ammy', 'email': 'Ammy@example.com', 'adress': 'random city'},
            {'name': 'Tom', 'email': 'Tom@example.com', 'adress': 'random city'},
            {'name': 'Dong', 'email': 'Dong@example.com', 'adress': 'random city'},
            {'name': 'David', 'email': 'david@example.com', 'adress': 'random city'},
        ]

        for data in test_data:
            renter = Renters.objects.create(
                name=data['name'],
                email=data['email'],
                adress=data['adress']
            )
        
        '''Создание книг'''
        test_books = [
            {'title': 'Book 1', 'vendor_code': '123123', 'author': 'Author', 'year': 2022, 'quantity': 5},
            {'title': 'Book 2', 'vendor_code': '123456', 'author': 'Author', 'year': 2023, 'quantity': 3},
            {'title': 'Book 3', 'vendor_code': '123789', 'author': 'Author', 'year': 2021, 'quantity': 2},
            {'title': 'Book 4', 'vendor_code': '123823', 'author': 'Author', 'year': 2022, 'quantity': 5},
            {'title': 'Book 5', 'vendor_code': '123956', 'author': 'Author', 'year': 2023, 'quantity': 3},
            {'title': 'Book 6', 'vendor_code': '123089', 'author': 'Author', 'year': 2021, 'quantity': 2},
        ]

        for data in test_books:
            book = Book(
                title=data['title'],
                vendor_code=data['vendor_code'],
                author=data['author'],
                year=data['year'],
                quantity=data['quantity']
            )
            book.slug = slugify(book.vendor_code)
            book.save()

        '''Создание аренд книг'''
        test_rents = [
            {'tenant': test_data[0]['email'], 'book': test_books[0]['vendor_code'], 'expiration_date': '2023-10-30'},
            {'tenant': test_data[1]['email'], 'book': test_books[1]['vendor_code'], 'expiration_date': '2023-01-30'},
            {'tenant': test_data[2]['email'], 'book': test_books[2]['vendor_code'], 'expiration_date': '2023-05-30'}]
        for data in test_rents:
            rent = Rent(
                tenant=Renters.objects.get(email=data['tenant']),
                book=Book.objects.get(vendor_code=data['book']),
                expiration_date=data['expiration_date']
            )
            rent.save()
        self.stdout.write(self.style.SUCCESS('Successfully created test Renters data'))
