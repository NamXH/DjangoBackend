from django.conf.urls import patterns, include, url
from restapi import views

urlpatterns = patterns('',
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api-token-auth/', 'rest_framework.authtoken.views.obtain_auth_token'),
)

urlpatterns += patterns('',
    url(r'^time/$', views.TimeList.as_view(), name='time-list'),
                        
    url(r'^states/$', views.StateList.as_view(), name='state-list'),
    url(r'^states/(?P<pk>[0-9]+)/$', views.StateDetail.as_view(), name='state-detail'),
   
    url(r'^countries/$', views.CountryList.as_view(), name='country-list'),
    url(r'^countries/(?P<pk>[0-9]+)/$', views.CountryDetail.as_view(), name='country-detail'),
    
    url(r'^croptypes/$', views.CropTypeList.as_view(), name='croptype-list'),
    url(r'^croptypes/(?P<pk>[0-9]+)/$', views.CropTypeDetail.as_view(), name='croptype-detail'),
    
    url(r'^fields/$', views.FieldList.as_view(), name='field-list'),
    url(r'^fields/(?P<pk>[0-9]+)/$', views.FieldDetail.as_view(), name='field-detail'),
    
    url(r'^farmusers/$', views.FarmUserList.as_view(), name='farmuser-list'),
    url(r'^farmusers/(?P<pk>[0-9]+)/$', views.FarmUserDetail.as_view(), name='farmuser-detail'),
    
    url(r'^farmchildusers/$', views.FarmChildUserList.as_view(), name='farmchilduser-list'),
    url(r'^farmchildusers/(?P<pk>[0-9]+)/$', views.FarmChildUserDetail.as_view(), name='farmchilduser-detail'),
)