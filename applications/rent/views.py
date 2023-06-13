from rest_framework.generics import ListAPIView, ListCreateAPIView

from .models import Rent
from .serialisers import RentSerialiser
from applications.account.models import Renters
from applications.account.serializers import RentersSerialiser


class RentListView(ListAPIView):
    queryset = Rent.objects.all()
    serializer_class = RentSerialiser


class RentesrListCreateView(ListCreateAPIView):
    queryset = Renters.objects.all()
    serializer_class = RentersSerialiser