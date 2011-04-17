from django.conf.urls.defaults import patterns, url, include

urlpatterns = patterns('linkedin_auth.views',
   url(r'^exchange/$', 'bearer_exchange_view', name='bearer_exchange_view'),
   url(r'^logout/$', 'linkedin_logout_view', name='linkedin_logout_view'),   
)