from restapi.models import FarmUser, FarmChildUser, Field, State, Country, CropType
from rest_framework import serializers

class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = ('id', 'name', 'country')
        
class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ('id', 'name', 'priority')
        
class CropTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CropType
        fields = ('id', 'name', 'is_default')
        
class FieldSerializer(serializers.ModelSerializer):
    commodity = serializers.Field(source='commodity.name')
    
    class Meta:
        model = Field
        fields = ('id', 'farm_user', 'name', 'commodity', 'location', 'area', 'area_unit',
                  'date_created', 'date_updated', 'timestamp', 'is_deleted')

class FarmUserSerializer(serializers.ModelSerializer):
    country = serializers.Field(source='get_country_name')
    state = serializers.Field(source='state.name')
    crops = serializers.Field(source='get_crop_types')
    user = serializers.Field(source='user.id')
    
    class Meta:
        model = FarmUser
        fields = ('user', 'id', 'email', 'first_name', 'last_name', 'company_name',
                  'birth_year', 'gender', 'date_created', 'date_updated', 'state', 'country',
                  'zip', 'acre_type', 'crops')
        
class FarmChildUserSerializer(serializers.ModelSerializer):
    child_type = serializers.Field(source='child_type.name')
    
    class Meta:
        model = FarmChildUser
        fields = ('id', 'master', 'first_name', 'last_name', 'email', 'child_type', 'field_permission',
                  'calendar_permission', 'storage_permission', 'contract_permission',
                  'delivery_permission', 'commodity_status_permission', 'yield_permission',
                  'equipment_permission', 'message_permission')


        

        