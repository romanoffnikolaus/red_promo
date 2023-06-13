from rest_framework.routers import DefaultRouter
from django.urls import path, include

from .views import BookViewset


router = DefaultRouter()


router.register('books', BookViewset)

urlpatterns = [
    path('', include(router.urls))
]