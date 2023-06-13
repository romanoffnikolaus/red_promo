from django.db import models

from applications.books.models import Book
from applications.account.models import Renters



class Rent(models.Model):
    tenant = models.ForeignKey(Renters, on_delete=models.CASCADE, related_name='rent_renter')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='rent_book')
    created_at = models.DateField(auto_now_add=True)
    expiration_date = models.DateField()

    def __str__(self) -> str:
        return self.book.title
    
    class Meta:
        indexes = [models.Index(fields=['expiration_date']),]