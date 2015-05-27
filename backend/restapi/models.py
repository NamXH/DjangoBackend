from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

@receiver(post_save, sender=get_user_model())
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

class Country(models.Model):
    name = models.CharField(max_length = 255)
    priority = models.IntegerField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False) # notify client of a deleted record
    date_created = models.DateTimeField(null=True, blank=True)
    date_updated = models.DateTimeField(null=True, blank=True)
    timestamp = models.IntegerField(null=True, blank=True)
    
class State(models.Model):
    country = models.ForeignKey(Country)
    name = models.CharField(max_length=255)
    is_deleted = models.BooleanField(default=False) # notify client of a deleted record
    date_created = models.DateTimeField(null=True, blank=True)
    date_updated = models.DateTimeField(null=True, blank=True)
    timestamp = models.IntegerField(null=True, blank=True)
    
    class Meta:
        unique_together = ("country", "name")

class CropType(models.Model):
    name = models.CharField(max_length=255)
    is_default = models.BooleanField()
    is_deleted = models.BooleanField(default=False) # notify client of a deleted record
    date_created = models.DateTimeField(null=True, blank=True)
    date_updated = models.DateTimeField(null=True, blank=True)
    timestamp = models.IntegerField(null=True, blank=True)
    
class AcreType(models.Model):
    range = models.CharField(max_length=255)
    is_default = models.BooleanField()
    is_deleted = models.BooleanField(default=False) # notify client of a deleted record
    date_created = models.DateTimeField(null=True, blank=True)
    date_updated = models.DateTimeField(null=True, blank=True)
    timestamp = models.IntegerField(null=True, blank=True)
    
class FarmUser(models.Model):
    user = models.OneToOneField(User, null=True, blank=True)
    email = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    company_name = models.CharField(max_length=255, null=True, blank=True)
    birth_year = models.DateField(null=True, blank=True)
    gender = models.IntegerField(null=True, blank=True)
    state = models.ForeignKey(State, null=True, blank=True)
    zip = models.CharField(max_length=255, null=True, blank=True)
    acre_type = models.ForeignKey(AcreType, null=True, blank=True)
    crop_types = models.ManyToManyField(CropType, null=True, blank=True)
    is_deleted = models.BooleanField(default=False) # notify client of a deleted record
    date_created = models.DateTimeField(null=True, blank=True)
    date_updated = models.DateTimeField(null=True, blank=True)
    timestamp = models.IntegerField(null=True, blank=True)

    def get_country_name(self):
        if self.state is not None and self.state.country is not None:
            return self.state.country.name
        else:
            return None
    
    def get_crop_types(self):
        crops = []
        for crop in self.crop_types.all():
            crops.append({'name': crop.name, 'is default': crop.is_default}) 
        return crops 

class ChildUserType(models.Model):
    name = models.CharField(max_length = 255)
    is_deleted = models.BooleanField(default=False) # notify client of a deleted record
    date_created = models.DateTimeField(null=True, blank=True)
    date_updated = models.DateTimeField(null=True, blank=True)
    timestamp = models.IntegerField(null=True, blank=True)

class FarmChildUser(models.Model):
    user = models.OneToOneField(User, null=True, blank=True)
    master = models.ForeignKey(FarmUser, null=True, blank=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    email = models.CharField(max_length=255)
    child_type = models.ForeignKey(ChildUserType, null=True, blank=True)
    field_permission = models.BooleanField(default=False)
    calendar_permission = models.BooleanField(default=False)
    storage_permission = models.BooleanField(default=False)
    contract_permission = models.BooleanField(default=False)
    delivery_permission = models.BooleanField(default=False)
    commodity_status_permission = models.BooleanField(default=False)
    yield_permission = models.BooleanField(default=False)
    equipment_permission = models.BooleanField(default=False)
    message_permission = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False) # notify client of a deleted record
    date_created = models.DateTimeField(null=True, blank=True)
    date_updated = models.DateTimeField(null=True, blank=True)
    timestamp = models.IntegerField(null=True, blank=True)

class SoilCondition(models.Model):
    name = models.CharField(max_length=255)
    is_default = models.BooleanField()
    is_deleted = models.BooleanField(default=False) # notify client of a deleted record
    date_created = models.DateTimeField(null=True, blank=True)
    date_updated = models.DateTimeField(null=True, blank=True)
    timestamp = models.IntegerField(null=True, blank=True)

class EquipmentCategory(models.Model):
    name = models.CharField(max_length=255)
    is_default = models.BooleanField()
    is_deleted = models.BooleanField(default=False) # notify client of a deleted record
    date_created = models.DateTimeField(null=True, blank=True)
    date_updated = models.DateTimeField(null=True, blank=True)
    timestamp = models.IntegerField(null=True, blank=True)

class PartCategory(models.Model):
    name = models.CharField(max_length=255)
    is_default = models.BooleanField()
    is_deleted = models.BooleanField(default=False) # notify client of a deleted record
    date_created = models.DateTimeField(null=True, blank=True)
    date_updated = models.DateTimeField(null=True, blank=True)
    timestamp = models.IntegerField(null=True, blank=True)
    
class PartType(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(PartCategory)
    is_default = models.BooleanField()
    is_deleted = models.BooleanField(default=False) # notify client of a deleted record
    date_created = models.DateTimeField(null=True, blank=True)
    date_updated = models.DateTimeField(null=True, blank=True)
    timestamp = models.IntegerField(null=True, blank=True)
    
    class Meta:
        unique_together = ("name", "category")

class Equipment(models.Model):
    name = models.CharField(max_length=255)
    farm_user = models.ForeignKey(FarmUser)
    category = models.ForeignKey(EquipmentCategory)
    description = models.CharField(max_length=255, null=True, blank=True)
    image_path = models.CharField(max_length=255, null=True, blank=True)
    year = models.DateField(null=True, blank=True)
    make = models.CharField(max_length=255, null=True, blank=True)
    model = models.CharField(max_length=255, null=True, blank=True)
    serial_number = models.CharField(max_length=255, null=True, blank=True)
    millage = models.FloatField(null=True, blank=True)
    notes = models.CharField(max_length=255, null=True, blank=True)
    engine_type = models.CharField(max_length=255, null=True, blank=True)
    engine_size = models.CharField(max_length=255, null=True, blank=True)
    place_purchased = models.CharField(max_length=255, null=True, blank=True)
    date_purchased = models.CharField(max_length=255, null=True, blank=True)
    price_purchased = models.CharField(max_length=255, null=True, blank=True)
    current_value = models.FloatField(null=True, blank=True)
    plate_number = models.CharField(max_length=255, null=True, blank=True)
    transmission_type = models.CharField(max_length=255, null=True, blank=True)
    transmission_size = models.CharField(max_length=255, null=True, blank=True)
    is_deleted = models.BooleanField(default=False) # notify client of a deleted record
    date_created = models.DateTimeField(null=True, blank=True)
    date_updated = models.DateTimeField(null=True, blank=True)
    timestamp = models.IntegerField(null=True, blank=True)

class EquipmentPart(models.Model):
    equipment = models.ForeignKey(Equipment)
    part_number = models.CharField(max_length=255, null=True, blank=True)
    type = models.ForeignKey(PartType)
    brand = models.CharField(max_length=255, null=True, blank=True)
    quantity_on_hand = models.IntegerField(null=True, blank=True)
    notes = models.CharField(max_length=255, null=True, blank=True)
    maintenance_date = models.DateField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False) # notify client of a deleted record
    date_created = models.DateTimeField(null=True, blank=True)
    date_updated = models.DateTimeField(null=True, blank=True)
    timestamp = models.IntegerField(null=True, blank=True)
    
    class Meta:
        unique_together = ("equipment", "part_number")
    
class EquipmentMaintenance(models.Model):
    equipment = models.ForeignKey(Equipment)
    date = models.DateField()
    type = models.ForeignKey(PartType)
    notes = models.CharField(max_length=255, null=True, blank=True)
    is_deleted = models.BooleanField(default=False) # notify client of a deleted record
    date_created = models.DateTimeField(null=True, blank=True)
    date_updated = models.DateTimeField(null=True, blank=True)
    timestamp = models.IntegerField(null=True, blank=True)

class Message(models.Model):
    farm_user = models.ForeignKey(FarmUser)
    time = models.DateTimeField()
    subject = models.CharField(max_length=255, null=True, blank=True)
    content = models.CharField(max_length=255)
    is_deleted = models.BooleanField(default=False) # notify client of a deleted record
    date_created = models.DateTimeField(null=True, blank=True)
    date_updated = models.DateTimeField(null=True, blank=True)
    timestamp = models.IntegerField(null=True, blank=True)
    
class Reply(models.Model):
    message = models.ForeignKey(Message)
    farm_user = models.ForeignKey(FarmUser)
    time = models.DateTimeField()
    subject = models.CharField(max_length=255, null=True, blank=True)
    content = models.CharField(max_length=255)
    is_deleted = models.BooleanField(default=False) # notify client of a deleted record
    date_created = models.DateTimeField(null=True, blank=True)
    date_updated = models.DateTimeField(null=True, blank=True)
    timestamp = models.IntegerField(null=True, blank=True)
    
class Commodity(models.Model):
    name = models.CharField(max_length=255)
    is_default = models.BooleanField()
    is_deleted = models.BooleanField(default=False) # notify client of a deleted record
    date_created = models.DateTimeField(null=True, blank=True)
    date_updated = models.DateTimeField(null=True, blank=True)
    timestamp = models.IntegerField(null=True, blank=True)

class Field(models.Model):
    farm_user = models.ForeignKey(FarmUser, null=True, blank=True)
    name = models.CharField(max_length=255)
    commodity = models.ForeignKey(Commodity, null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    area = models.FloatField(null=True, blank=True)
    area_unit = models.CharField(max_length=255, null=True, blank=True)
    is_deleted = models.BooleanField(default=False) # notify client of a deleted record
    date_created = models.DateTimeField(null=True, blank=True)
    date_updated = models.DateTimeField(null=True, blank=True)
    timestamp = models.IntegerField(null=True, blank=True)
    
    class Meta:
        unique_together = ("farm_user", "name")
        
class ContractType(models.Model):
    name = models.CharField(max_length=255)
    is_default = models.BooleanField()
    is_deleted = models.BooleanField(default=False) # notify client of a deleted record
    date_created = models.DateTimeField(null=True, blank=True)
    date_updated = models.DateTimeField(null=True, blank=True)
    timestamp = models.IntegerField(null=True, blank=True)

class Contract(models.Model):
    farm_user = models.ForeignKey(FarmUser)
    type = models.ForeignKey(ContractType)
    name = models.CharField(max_length=255, null=True, blank=True)
    date_created = models.DateField()
    date_maturity = models.DateField()
    date_contract = models.DateField()
    company = models.CharField(max_length=255, null=True, blank=True)
    commodity = models.ForeignKey(Commodity)
    variety = models.CharField(max_length=255, null=True, blank=True)
    contract_price = models.FloatField(null=True, blank=True)
    basis = models.CharField(max_length=255, null=True, blank=True)
    quality = models.CharField(max_length=255, null=True, blank=True)
    contracted_amount = models.FloatField(null=True, blank=True)
    delivered_amount = models.FloatField(null=True, blank=True)
    remain_amount = models.FloatField(null=True, blank=True)
    notes = models.CharField(max_length=255, null=True, blank=True)
    completed = models.BooleanField()
    is_deleted = models.BooleanField(default=False) # notify client of a deleted record
    date_created = models.DateTimeField(null=True, blank=True)
    date_updated = models.DateTimeField(null=True, blank=True)
    timestamp = models.IntegerField(null=True, blank=True)

class Delivery(models.Model):
    contract = models.ForeignKey(Contract)
    date_delivered = models.DateField()
    commodity = models.ForeignKey(Commodity)
    variety = models.CharField(max_length=255, null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    ticket = models.CharField(max_length=255, null=True, blank=True)
    quality = models.CharField(max_length=255, null=True, blank=True)
    dockage = models.FloatField(null=True, blank=True)
    basis = models.CharField(max_length=255, null=True, blank=True)
    trucking_company = models.CharField(max_length=255, null=True, blank=True)
    hopper_seal = models.CharField(max_length=255, null=True, blank=True)
    notes = models.CharField(max_length=255, null=True, blank=True)
    completed = models.BooleanField()
    storage = models.BooleanField()
    grain_bags = models.ManyToManyField("GrainBag")
    bins = models.ManyToManyField("Bin")
    is_deleted = models.BooleanField(default=False) # notify client of a deleted record
    date_created = models.DateTimeField(null=True, blank=True)
    date_updated = models.DateTimeField(null=True, blank=True)
    timestamp = models.IntegerField(null=True, blank=True)

class BinYard(models.Model):
    farm_user = models.ForeignKey(FarmUser)
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255, null=True, blank=True)
    is_deleted = models.BooleanField(default=False) # notify client of a deleted record
    date_created = models.DateTimeField(null=True, blank=True)
    date_updated = models.DateTimeField(null=True, blank=True)
    timestamp = models.IntegerField(null=True, blank=True)
    
class Bin(models.Model):
    bin_yard = models.ForeignKey(BinYard)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, null=True, blank=True)
    size = models.FloatField(null=True, blank=True)
    commodity = models.ForeignKey(Commodity)
    variety = models.CharField(max_length=255, null=True, blank=True)
    amount = models.FloatField()
    temperature = models.FloatField(null=True, blank=True)
    moisture = models.FloatField(null=True, blank=True)
    date_harvested = models.DateField(null=True, blank=True)
    field = models.ForeignKey(Field)
    notes =  models.CharField(max_length=255, null=True, blank=True)
    amount_unit = models.CharField(max_length=255, null=True, blank=True)
    temperature_unit = models.CharField(max_length=255, null=True, blank=True)
    is_deleted = models.BooleanField(default=False) # notify client of a deleted record
    date_created = models.DateTimeField(null=True, blank=True)
    date_updated = models.DateTimeField(null=True, blank=True)
    timestamp = models.IntegerField(null=True, blank=True)
    
class GrainBag(models.Model):
    name = models.CharField(max_length=255)
    field = models.ForeignKey(Field)
    size = models.FloatField(null=True, blank=True)
    commodity = models.ForeignKey(Commodity)
    variety = models.CharField(max_length=255, null=True, blank=True)
    amount = models.FloatField()
    temperature = models.FloatField(null=True, blank=True)
    moisture = models.FloatField(null=True, blank=True)
    date_harvested = models.DateField(null=True, blank=True)
    notes =  models.CharField(max_length=255, null=True, blank=True)
    amount_unit = models.CharField(max_length=255, null=True, blank=True)
    temperature_unit = models.CharField(max_length=255, null=True, blank=True)
    is_deleted = models.BooleanField(default=False) # notify client of a deleted record
    date_created = models.DateTimeField(null=True, blank=True)
    date_updated = models.DateTimeField(null=True, blank=True)
    timestamp = models.IntegerField(null=True, blank=True)

class ApplicationActivity(models.Model):
    field = models.ForeignKey(Field)
    date = models.DateField(null=True, blank=True)
    anhydrous_rate = models.FloatField(null=True, blank=True)
    anhydrous_variable_rate = models.CharField(max_length=255, null=True, blank=True)
    anhydrous_total_used = models.FloatField(null=True, blank=True)
    dry_fertilizer_rate = models.FloatField(null=True, blank=True)
    dry_fertilizer_variable_rate = models.CharField(max_length=255, null=True, blank=True)
    dry_fertilizer_blend = models.CharField(max_length=255, null=True, blank=True)
    dry_fertilizer_total_used = models.FloatField(null=True, blank=True)
    liquid_fertilizer_rate = models.FloatField(null=True, blank=True)
    liquid_fertilizer_variable_rate = models.CharField(max_length=255, null=True, blank=True)
    liquid_fertilizer_type = models.CharField(max_length=255, null=True, blank=True)
    liquid_fertilizer_total_used = models.FloatField(null=True, blank=True)
    micro_nutrients_rate = models.FloatField(null=True, blank=True)
    micro_nutrients_variable_rate = models.CharField(max_length=255, null=True, blank=True)
    micro_nutrients_type = models.CharField(max_length=255, null=True, blank=True)
    micro_nutrients_total_used = models.FloatField(null=True, blank=True)
    soil_condition = models.ForeignKey(SoilCondition, null=True, blank=True)
    notes = models.CharField(max_length=255, null=True, blank=True)
    anhydrous_rate_unit = models.CharField(max_length=255, null=True, blank=True)
    anhydrous_total_used_unit = models.CharField(max_length=255, null=True, blank=True)
    dry_fertilizer_rate_unit = models.CharField(max_length=255, null=True, blank=True)
    dry_fertilizer_total_used_unit = models.CharField(max_length=255, null=True, blank=True)
    liquid_fertilizer_rate_unit = models.CharField(max_length=255, null=True, blank=True)
    liquid_fertilizer_total_used_unit = models.CharField(max_length=255, null=True, blank=True)
    micro_nutrients_rate_unit = models.CharField(max_length=255, null=True, blank=True)
    micro_nutrients_total_used = models.CharField(max_length=255, null=True, blank=True)
    is_deleted = models.BooleanField(default=False) # notify client of a deleted record
    date_created = models.DateTimeField(null=True, blank=True)
    date_updated = models.DateTimeField(null=True, blank=True)
    timestamp = models.IntegerField(null=True, blank=True)

class PlantingActivity(models.Model):
    field = models.ForeignKey(Field)
    date = models.DateField(null=True, blank=True)
    commodity = models.ForeignKey(Commodity)
    variety = models.CharField(max_length=255, null=True, blank=True)
    treatment = models.CharField(max_length=255, null=True, blank=True)
    seeded_area = models.FloatField(null=True, blank=True)
    seed_rate = models.FloatField(null=True, blank=True)
    soil_condition = models.ForeignKey(SoilCondition, null=True, blank=True)
    anhydrous_rate = models.FloatField(null=True, blank=True)
    anhydrous_variable_rate = models.CharField(max_length=255, null=True, blank=True)
    anhydrous_total_used = models.FloatField(null=True, blank=True)
    dry_fertilizer_rate = models.FloatField(null=True, blank=True)
    dry_fertilizer_variable_rate = models.CharField(max_length=255, null=True, blank=True)
    dry_fertilizer_blend = models.CharField(max_length=255, null=True, blank=True)
    dry_fertilizer_total_used = models.FloatField(null=True, blank=True)
    liquid_fertilizer_rate = models.FloatField(null=True, blank=True)
    liquid_fertilizer_variable_rate = models.CharField(max_length=255, null=True, blank=True)
    liquid_fertilizer_type = models.CharField(max_length=255, null=True, blank=True)
    liquid_fertilizer_total_used = models.FloatField(null=True, blank=True)
    micro_nutrients_rate = models.FloatField(null=True, blank=True)
    micro_nutrients_variable_rate = models.CharField(max_length=255, null=True, blank=True)
    micro_nutrients_type = models.CharField(max_length=255, null=True, blank=True)
    micro_nutrients_total_used = models.FloatField(null=True, blank=True)
    notes = models.CharField(max_length=255, null=True, blank=True)
    seeded_area_unit = models.CharField(max_length=255, null=True, blank=True)
    seed_rate_unit = models.CharField(max_length=255, null=True, blank=True)
    anhydrous_rate_unit = models.CharField(max_length=255, null=True, blank=True)
    anhydrous_total_used_unit = models.CharField(max_length=255, null=True, blank=True)
    dry_fertilizer_rate_unit = models.CharField(max_length=255, null=True, blank=True)
    dry_fertilizer_total_used_unit = models.CharField(max_length=255, null=True, blank=True)
    liquid_fertilizer_rate_unit = models.CharField(max_length=255, null=True, blank=True)
    liquid_fertilizer_total_used_unit = models.CharField(max_length=255, null=True, blank=True)
    micro_nutrients_rate_unit = models.CharField(max_length=255, null=True, blank=True)
    micro_nutrients_total_used = models.CharField(max_length=255, null=True, blank=True)
    is_deleted = models.BooleanField(default=False) # notify client of a deleted record
    date_created = models.DateTimeField(null=True, blank=True)
    date_updated = models.DateTimeField(null=True, blank=True)
    timestamp = models.IntegerField(null=True, blank=True)

class SprayingActivity(models.Model):
    field = models.ForeignKey(Field)
    date = models.DateField(null=True, blank=True)
    app_rate = models.FloatField(null=True, blank=True)
    sprayed_area = models.FloatField(null=True, blank=True)
    spray_timing = models.ForeignKey("SprayTiming")
    nozzel = models.CharField(max_length=255, null=True, blank=True)
    weather = models.CharField(max_length=255, null=True, blank=True)
    notes = models.CharField(max_length=255, null=True, blank=True)
    sprayed_area_unit = models.CharField(max_length=255, null=True, blank=True)
    app_rate_unit = models.CharField(max_length=255, null=True, blank=True)
    chemicals = models.ManyToManyField("Chemical", through="ChemicalSprayed")
    is_deleted = models.BooleanField(default=False) # notify client of a deleted record
    date_created = models.DateTimeField(null=True, blank=True)
    date_updated = models.DateTimeField(null=True, blank=True)
    timestamp = models.IntegerField(null=True, blank=True)
    
class SprayTiming(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    is_default = models.BooleanField()
    is_deleted = models.BooleanField(default=False) # notify client of a deleted record
    date_created = models.DateTimeField(null=True, blank=True)
    date_updated = models.DateTimeField(null=True, blank=True)
    timestamp = models.IntegerField(null=True, blank=True)

class Chemical(models.Model):
    type = models.CharField(max_length=255, null=True, blank=True)
    is_default = models.BooleanField()
    is_deleted = models.BooleanField(default=False) # notify client of a deleted record
    date_created = models.DateTimeField(null=True, blank=True)
    date_updated = models.DateTimeField(null=True, blank=True)
    timestamp = models.IntegerField(null=True, blank=True)

class ChemicalSprayed(models.Model):
    spraying_activity = models.ForeignKey(SprayingActivity)
    chemical = models.ForeignKey(Chemical)
    name = models.CharField(max_length=255, null=True, blank=True)
    rate = models.FloatField(null=True, blank=True)
    total = models.FloatField(null=True, blank=True)
    rate_unit = models.CharField(max_length=255, null=True, blank=True)
    total_unit = models.CharField(max_length=255, null=True, blank=True)
    is_deleted = models.BooleanField(default=False) # notify client of a deleted record
    date_created = models.DateTimeField(null=True, blank=True)
    date_updated = models.DateTimeField(null=True, blank=True)
    timestamp = models.IntegerField(null=True, blank=True)
    
class ObservationActivity(models.Model):
    field = models.ForeignKey(Field)
    date = models.DateField(null=True, blank=True)
    type = models.ForeignKey("ObservationType")
    notes = models.CharField(max_length=255, null=True, blank=True)
    image_path = models.CharField(max_length=255, null=True, blank=True)
    is_deleted = models.BooleanField(default=False) # notify client of a deleted record
    date_created = models.DateTimeField(null=True, blank=True)
    date_updated = models.DateTimeField(null=True, blank=True)
    timestamp = models.IntegerField(null=True, blank=True)
    
class ObservationType(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    is_deleted = models.BooleanField(default=False) # notify client of a deleted record
    date_created = models.DateTimeField(null=True, blank=True)
    date_updated = models.DateTimeField(null=True, blank=True)
    timestamp = models.IntegerField(null=True, blank=True)
    
class IrrigationActivity(models.Model):
    field = models.ForeignKey(Field)
    date = models.DateField(null=True, blank=True)
    notes = models.CharField(max_length=255, null=True, blank=True)
    is_deleted = models.BooleanField(default=False) # notify client of a deleted record
    date_created = models.DateTimeField(null=True, blank=True)
    date_updated = models.DateTimeField(null=True, blank=True)
    timestamp = models.IntegerField(null=True, blank=True)
    
class HarvestActivity(models.Model):
    field = models.ForeignKey(Field)
    date = models.DateField(null=True, blank=True)
    swathing_notes = models.CharField(max_length=255, null=True, blank=True)
    area = models.FloatField(null=True, blank=True)
    harvest_yield = models.IntegerField(null=True, blank=True)
    moisture = models.FloatField(null=True, blank=True)
    protein = models.FloatField(null=True, blank=True)
    disease = models.CharField(max_length=255, null=True, blank=True)
    green = models.FloatField(null=True, blank=True)
    concave = models.IntegerField(null=True, blank=True)
    upper_scive = models.IntegerField(null=True, blank=True)
    lower_scive = models.IntegerField(null=True, blank=True)
    fan_speed = models.IntegerField(null=True, blank=True)
    rotar_speed = models.IntegerField(null=True, blank=True)
    notes = models.CharField(max_length=255, null=True, blank=True)
    area_unit = models.CharField(max_length=255, null=True, blank=True)
    yield_unit = models.CharField(max_length=255, null=True, blank=True)
    moisture_unit = models.CharField(max_length=255, null=True, blank=True)
    is_deleted = models.BooleanField(default=False) # notify client of a deleted record
    date_created = models.DateTimeField(null=True, blank=True)
    date_updated = models.DateTimeField(null=True, blank=True)
    timestamp = models.IntegerField(null=True, blank=True)
    
class CustomActivity(models.Model):
    field = models.ForeignKey(Field)
    date = models.DateField(null=True, blank=True)
    notes = models.CharField(max_length=255, null=True, blank=True)
    is_deleted = models.BooleanField(default=False) # notify client of a deleted record
    date_created = models.DateTimeField(null=True, blank=True)
    date_updated = models.DateTimeField(null=True, blank=True)
    timestamp = models.IntegerField(null=True, blank=True)