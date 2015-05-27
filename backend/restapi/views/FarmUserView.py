from django.contrib.auth.models import User
from datetime import datetime
from django.utils.timezone import utc

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from restapi.models import FarmUser
from restapi.serializers import FarmUserSerializer
from restapi.views.ViewUtils import filter_by_date_updated

class FarmUserList(APIView):
    def get(self, request, format=None):
        if request.user.is_superuser:
            farm_users = FarmUser.objects.all()
        else:
            farm_users = FarmUser.objects.filter(user=request.user)
        farm_users = filter_by_date_updated(request=request, queryset=farm_users)
        
        serializer = FarmUserSerializer(farm_users, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        """
        For fast prototyping, we will manually use a user/token when registering new 
        FarmUser. This behavior should be changed in future release.
        """
        password = request.DATA.get('password')
        if password is None:
            return Response(data=[{'password': 'this field is required'}], status=status.HTTP_400_BAD_REQUEST)
        
        del request.DATA['password']
        serializer = FarmUserSerializer(data=request.DATA)
        if serializer.is_valid():
            django_user = User.objects.create_user(username=request.DATA['email'], password=password) # Email should be a required field
            this_moment = datetime.utcnow().replace(tzinfo=utc)
            serializer.object.date_created = this_moment
            serializer.object.date_updated = this_moment
            farm_user = serializer.save()
            farm_user.user = django_user
            farm_user.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
class FarmUserDetail(APIView):
    def get_object(self, request, pk):
        result = []
        if request.user.is_superuser:
            result = FarmUser.objects.filter(pk=pk)
        elif hasattr(request.user, 'farmuser'):
            result = FarmUser.objects.filter(user=request.user).filter(pk=pk)
        result = filter_by_date_updated(request=request, queryset=result)
        
        try:
            return result[0]
        except IndexError:
            return None
    
    def get(self, request, pk, format=None):
        farm_user = self.get_object(request, pk)
        if farm_user is not None:
            serializer = FarmUserSerializer(farm_user)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
    def put(self, request, pk, format=None):    
        farm_user = self.get_object(request, pk)
        if farm_user is not None:
            # Prevent changing related Django User in future released if needed.
            
            # Change password if provided.
            password = request.DATA.get('password')
            if password is not None:
                del request.DATA['password']
                django_user = farm_user.user
                django_user.set_password(password)
                django_user.save()
                
            serializer = FarmUserSerializer(farm_user, data=request.DATA)
            if serializer.is_valid():
                serializer.object.date_updated = datetime.utcnow().replace(tzinfo=utc)
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk, format=None):
        farm_user = self.get_object(request, pk)
        if farm_user is not None:
            farm_user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
