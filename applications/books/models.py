from django.db import models
from slugify import slugify
    

class Book(models.Model):

    title = models.CharField(max_length=50)
    vendor_code = models.CharField(max_length=6, blank=False, unique=True)
    slug = models.SlugField(max_length=6, primary_key=True, blank=True, unique=True)
    author = models.CharField(max_length=60)
    year = models.SmallIntegerField()
    added = models.DateField(auto_now_add=True)
    quantity = models.IntegerField()
    rented = models.IntegerField(default=0)

    out_of_stock = models.BooleanField(default=False)
    
    def __str__(self) -> str:
        return self.vendor_code
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.vendor_code)
        super().save()

    class Meta:
        indexes = [models.Index(fields=['vendor_code']),]
