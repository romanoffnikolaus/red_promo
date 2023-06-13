from django.urls import path

from .views import RentListView, RentesrListCreateView

urlpatterns = [
    path('rented_books/', RentListView.as_view(), name = 'rented_books'),
    path('renters/', RentesrListCreateView.as_view(), name='renters'),

]