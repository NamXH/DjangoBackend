from django.contrib.auth.models import User
from datetime import datetime
from django.utils.timezone import utc

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from restapi.models import FarmChildUser
from restapi.serializers import FarmChildUserSerializer
from restapi.views.ViewUtils import filter_by_date_updated 

class FarmChildUserList(APIView):
    def get(self, request, format=None):
        if request.user.is_superuser:
            child = FarmChildUser.objects.all()
        elif hasattr(request.user, 'farmuser'):
            child = FarmChildUser.objects.filter(master=request.user.farmuser)
        elif hasattr(request.user, 'farmchilduser'):
            child = FarmChildUser.objects.filter(user=request.user)
        child = filter_by_date_updated(request=request, queryset=child)
        
        serializer = FarmChildUserSerializer(child, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        if hasattr(request.user, 'farmuser'):
            password = request.DATA.get('password')
            if password is None:
                return Response(data=[{'password': 'this field is required'}], status=status.HTTP_400_BAD_REQUEST)
            
            del request.DATA['password']
            serializer = FarmChildUserSerializer(data=request.DATA)
            if serializer.is_valid():
                django_user = User.objects.create_user(username=request.DATA['email'], password=password) # Email should be a required field
                child = serializer.save()
                child.user = django_user
                child.master = request.user.farmuser
                this_moment = datetime.utcnow().replace(tzinfo=utc)
                serializer.object.date_created = this_moment
                serializer.object.date_updated = this_moment
                child.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)
        
class FarmChildUserDetail(APIView):
    def get_object(self, request, pk):
        result = []
        if request.user.is_superuser:
            result = FarmChildUser.objects.filter(pk=pk)
        elif hasattr(request.user, 'farmuser'):
            result = FarmChildUser.objects.filter(master=request.user.farmuser).filter(pk=pk)
        elif hasattr(request.user, 'farmchilduser'):
            result = FarmChildUser.objects.filter(user=request.user).filter(pk=pk)
        result = filter_by_date_updated(request=request, queryset=result)    
        
        try:
            return result[0]
        except IndexError:
            return None

    def get(self, request, pk, format=None):
        child = self.get_object(request, pk)
        if child is not None:
            serializer = FarmChildUserSerializer(child)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
    def put(self, request, pk, format=None):    
        child = self.get_object(request, pk)
        if child is not None:
            # Prevent changing related Django User in future released if needed.
            
            # Change password if provided.
            password = request.DATA.get('password')
            if password is not None:
                del request.DATA['password']
                django_user = child.user
                django_user.set_password(password)
                django_user.save()
                
            serializer = FarmChildUserSerializer(child, data=request.DATA)
            if serializer.is_valid():
                serializer.object.date_updated = datetime.utcnow().replace(tzinfo=utc)
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request, pk, format=None):
        child = self.get_object(request, pk)
        if child is not None:
            child.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)