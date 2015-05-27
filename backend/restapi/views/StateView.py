from rest_framework import generics

from restapi.models import State
from restapi.serializers import StateSerializer
from restapi import permissions

class StateList(generics.ListCreateAPIView):
    queryset = State.objects.all()
    serializer_class = StateSerializer
    
class StateDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = State.objects.all()
    serializer_class = StateSerializer
    permission_classes = (permissions.IsAdminOrReadOnly,)