from rest_framework import generics

from restapi.models import Country
from restapi.serializers import CountrySerializer
from restapi import permissions

class CountryList(generics.ListCreateAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    
class CountryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = (permissions.IsAdminOrReadOnly,)