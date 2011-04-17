from django.conf.urls.defaults import patterns, include, url
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required

import linkedin_auth.urls

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'auth_example.views.home', name='home'),
    # url(r'^auth_example/', include('auth_example.foo.urls')),

    (r'^accounts/login/$', 'django.contrib.auth.views.login'),
    (r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
    (r'^accounts/profile/$', TemplateView.as_view(template_name="liprofile.html")),
    (r'^accounts/profile/connections/$', TemplateView.as_view(template_name='liconnections.html')),
    
    # django-linkedinauth
    url(r'^linkedin/', include(linkedin_auth.urls), name='linkedin_auth'),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    
    url(r'^$', TemplateView.as_view(template_name="home.html"), name='homepage_view'),
)
