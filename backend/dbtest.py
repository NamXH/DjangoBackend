from django.contrib.auth.models import User
from restapi.models import FarmUser, Field, FarmChildUser, Country, State, CropType

#Django user
foo_user = User.objects.create_user('foo', 'foo@foo.com', '123456')
bar_user = User.objects.create_user('bar', 'bar@bar.com', '123456')
baz_user = User.objects.create_user('baz', 'baz@baz.com', '123456')
foo2_user = User.objects.create_user('foo2', 'foo2@foo2.com', '123456')
bar2_user = User.objects.create_user('bar2', 'bar2@bar2.com', '123456')

#Country, State
us = Country(name='US')
us.save()
ca = Country(name='Canada')
ca.save()
ny = State(name='New York', country=us)
ny.save()
sk = State(name='Saskatchewan', country=ca)
sk.save()

#Crop type
cereals = CropType(name='Cereals', is_default=True)
cereals.save()
pulses = CropType(name='Pulses', is_default=True)
pulses.save()

#Farm user
foo_farm = FarmUser(email="foofarm@foofarm.com", user=foo_user, state=ny)
foo_farm.save()
foo_farm.crop_types.add(cereals)
foo_farm.crop_types.add(pulses)

foo2_farm = FarmUser(email="foofarm2@foofarm2.com", user=foo2_user, state=sk)
foo2_farm.save()
foo2_farm.crop_types.add(pulses)


#Child user
bar_child = FarmChildUser(email="barchild@barchild.com", user=bar_user, master=foo_farm, field_permission=True)
bar_child.save()
baz_child = FarmChildUser(email="bazchild@bazchild.com", user=baz_user, master=foo_farm, field_permission=False)
baz_child.save()
bar2_child = FarmChildUser(email="bar2child@bar2child.com", user=bar2_user, master=foo2_farm, calendar_permission=True)
bar2_child.save()

#Field
foo_field1 = Field(farm_user=foo_farm, name="foo field 1")
foo_field1.save()
foo_field2 = Field(farm_user=foo_farm, name="foo field 2")
foo_field2.save()
foo2_field1 = Field(farm_user=foo2_farm, name="foo2 field 1")
foo2_field1.save()

