from rest_framework import generics

from restapi.models import CropType
from restapi.serializers import CropTypeSerializer
from restapi import permissions

class CropTypeList(generics.ListCreateAPIView):
    queryset = CropType.objects.all()
    serializer_class = CropTypeSerializer
    
class CropTypeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = CropType.objects.all()
    serializer_class = CropTypeSerializer
    permission_classes = (permissions.IsAdminOrReadOnly,)