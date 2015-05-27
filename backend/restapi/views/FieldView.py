from datetime import datetime
from django.utils.timezone import utc

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from restapi.models import Field
from restapi.serializers import FieldSerializer
from restapi.views.ViewUtils import filter_by_date_updated, check_timestamp

class FieldList(APIView):
    def user_has_permission(self, request):
        if hasattr(request.user, 'farmchilduser'):
            return  request.user.farmchilduser.field_permission
        else:
            return True
        
    def get_model_queryset(self, request):
        """
        Get queryset according to user.
        """
        if request.user.is_superuser:
            result = Field.objects.all()
        elif hasattr(request.user, 'farmuser'):
            result = Field.objects.filter(farm_user=request.user.farmuser)
        elif hasattr(request.user, 'farmchilduser'):
            result = Field.objects.filter(farm_user=request.user.farmchilduser.master)
        else:
            return None
        return filter_by_date_updated(request=request, queryset=result)
        
    def get(self, request, format=None):
        if not self.user_has_permission(request):
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        fields = self.get_model_queryset(request)            
        if fields is not None:
            serializer = FieldSerializer(fields, many=True)
            return Response(serializer.data)
        else:
            Response(status=status.HTTP_401_UNAUTHORIZED) # Should not happened since we have an authentication layer before this
    
    def post(self, request, format=None):
        if not self.user_has_permission(request):
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        serializer = FieldSerializer(data=request.DATA)
        if serializer.is_valid():
            if hasattr(request.user, 'farmuser'):
                serializer.object.farm_user = request.user.farmuser
            elif hasattr(request.user, 'farmchilduser'):
                serializer.object.farm_user = request.user.farmchilduser.master
            this_moment = datetime.utcnow().replace(tzinfo=utc)
            serializer.object.date_created = this_moment
            serializer.object.date_updated = this_moment
            serializer.object.timestamp = 0;
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FieldDetail(APIView):
    def user_has_permission(self, request):
        if hasattr(request.user, 'farmchilduser'):
            return  request.user.farmchilduser.field_permission
        else:
            return True
        
    def get_object(self, request, pk):
        result = []
        if request.user.is_superuser:
            result = Field.objects.filter(pk=pk)
        elif hasattr(request.user, 'farmuser'):
            result = Field.objects.filter(farm_user=request.user.farmuser).filter(pk=pk)
        elif hasattr(request.user, 'farmchilduser'):
            result = Field.objects.filter(farm_user=request.user.farmchilduser.master).filter(pk=pk)
        result = filter_by_date_updated(request=request, queryset=result)

        try:
            return result[0]
        except IndexError:
            return None
    
    def get(self, request, pk, format=None):
        if not self.user_has_permission(request):
            return Response(status=status.HTTP_403_FORBIDDEN)
            
        field = self.get_object(request, pk)
        if field is not None:
            serializer = FieldSerializer(field)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
    def put(self, request, pk, format=None):
        if not self.user_has_permission(request):
            return Response(status=status.HTTP_403_FORBIDDEN)
            
        field = self.get_object(request, pk)
        if field is not None:
            timestamp_valid = check_timestamp(request, field.timestamp)
            if timestamp_valid is None:
                return Response(data=[{'timestamp': 'this field is required and should be integer'}], status=status.HTTP_400_BAD_REQUEST)
            elif not timestamp_valid:
                return Response(data='Your current record is outdated. Please issue a GET call to update.', status=status.HTTP_409_CONFLICT)
            
            serializer = FieldSerializer(field, data=request.DATA)
            if serializer.is_valid():
                if hasattr(request.user, 'farmuser'):
                    serializer.object.farm_user = request.user.farmuser
                elif hasattr(request.user, 'farmchilduser'):
                    serializer.object.farm_user = request.user.farmchilduser.master
                serializer.object.date_updated = datetime.utcnow().replace(tzinfo=utc)
                
                try:
                    serializer.object.timestamp = field.timestamp + 1
                except Exception:
                    # Arithmetic overflow
                    serializer.object.timestamp = 0
                    
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
            
    def delete(self, request, pk, format=None):
        if not self.user_has_permission(request):
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        field = self.get_object(request, pk)
        if field is not None:
#             field.delete()
            field.is_deleted = True
            field.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)