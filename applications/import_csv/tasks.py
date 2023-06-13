from typing import List

from django.core.mail import send_mail
from django.db import transaction
from django.utils.text import slugify

from celery import shared_task
from applications.books.models import Book


@shared_task
@transaction.atomic
def process_csv_file(csv_data: List[dict], email: str):
    book_list = []
    for element in csv_data:
        vendor_code = element['vendor_code']
        quantity = int(element['quantity'])
        try:
            book = Book.objects.get(vendor_code=vendor_code)
            book.quantity += quantity
            book.save()
        except Book.DoesNotExist:
            title = element['title']
            author = element['author']
            year = int(element['year'])
            slug = slugify(vendor_code)
            new_book = Book(title=title, vendor_code=vendor_code, author=author, year=year, quantity=quantity, slug=slug)
            book_list.append(new_book)
    if book_list:
        Book.objects.bulk_create(book_list)
    subject = 'CSV-файл обработан'
    message = 'CSV-файл успешно обработан. Данные вступили в силу'
    from_email = 'red_promo@example.com'
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list)
