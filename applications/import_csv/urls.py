from rest_framework.urls import path

from .views import CSVReaderView


urlpatterns = [
    path('read_csv/', CSVReaderView.as_view())
]