django-linkedinauth
=====================================

A simple Django project to allow user authentication and profile mapping via the LinkedIn API.

The linkedin_auth module provides the following features:

- Authentication Backend
- Context Processor
- Abstract Django User Profile Model
- View function to exchange bearer tokens
- View function to logout a LinkedIn profile
- A set of convenience Javascript functions (Coming Soon)
    
Included is a sample Django project that creates a simple website that will
allow login via the LinkedIn sign-in button, and execute a redirect to the
bearer token exchange view to execute the Django login and mapping of the
Django user model to a user profile model that is mapped from a server-side
request to the LinkedIn API.


Prerequisites
-------------

django-linkedinauth requires the following Python libraries to function:

    LinkedIn-Client-Library (mgile fork)
[https://github.com/mgile/LinkedIn-Client-Library](https://github.com/mgile/LinkedIn-Client-Library)
    
Note that this module requires a fork of the official LinkedIn-Client-Library
to enable the exchange of JSAPI bearer tokens.  This is a convenience feature
so that websites may bridge from the Javascript login button to a long-lived
OAuth 1.0a access token on the server.
    
For convenience, you may copy and paste the following into your requirements.txt file:

    LinkedIn-Client-Library==1.0
    httplib2==0.6.0
    lxml==2.3
    oauth==1.0.1
    oauth2==1.5.168
    simplejson==2.1.3
    
This includes all of the libraries needed by LinkedIn-Client-Library.


Installation
------------

To install, execute the following from within the django-linkedinauth directory:

    python setup.py install
    
    
settings.py
-----------

Add the following to your TEMPLATE_CONTEXT_PROCESSORS:
    
    'linkedin_auth.context_processors.linkedin',
    
Add the following to INSTALLED_APPS:
    
    'linkedin_auth',
    
Add the following to AUTHENTICATION_BACKENDS:
    
    'linkedin_auth.auth_backends.LinkedInAuthenticationBackend',
    

Ensure the following entries are set:

    LOGOUT_URL= '/linkedin/logout'
    
    LINKEDIN_API_KEY    = <INSERT YOUR LINKEDIN API KEY HERE>
    
    LINKEDIN_SECRET_KEY = <INSERT YOUR LINKEDIN SECRET KEY HERE>

    AUTH_PROFILE_MODULE = '<yourapp.YourProfileModel>'
  
urls.py
-------
  
Add the following to your project urls.py:

    import linkedin_auth.urls
    
    url(r'^linkedin/', include(linkedin_auth.urls)),
    
    
models.py
---------

Below is an example of how to create a user profile in your
Django application that maps to a LinkedIn account. Note that
your model must subclass LinkedInProfileModel, or you must 
include all of the same fields in the LinkedInProfileModel.

    from django.db import models
    from django.contrib.auth.models import User
    from linkedin_auth.models import LinkedInProfileModel

    class ExampleUserProfile(LinkedInProfileModel):
        user        = models.OneToOneField(User)
        
        class Meta:
            unique_together     = ('member_id', 'user')
            verbose_name        = 'Example User Profile'
            verbose_name_plural = 'Example User Profiles'


Ensure to add the following below your profile model:

    from django.db.models.signals import post_save
    from django.dispatch import receiver
    from linkedin_auth.models import random_member_id
    
    @receiver(post_save, sender=User)
    def create_profile(sender, instance, created, **kwargs):
        """Create a matching profile whenever a user object is created."""
        if created:
            rand_id         = random_member_id()
            profile, new    = ExampleUserProfile.objects.get_or_create(user=instance, defaults={ 'member_id': rand_id })
            
    
This code attaches to the signal sent everytime Django creates a new User model.  Upon
creation, the method create_profile will create a new LinkedIn-backed profile model.  When
a user first logs in with their LinkedIn credentials, the linkedin_auth application will
attempt to map the LinkedIn profile for that user to the user profile model.

Templates (Coming Soon)
---------

This project will provide a standalone Javascript class to provide 
several convenience methods to auto-link your website, the linkedin_auth app and 
the LinkedIn JSAPI.

In the interim, you should look in the 'libase.html' template in auth_example
for examples of how to link login/logout events to the linkedin_auth application.
    
    
HTTPS Support
-------------

The LinkedIn bearer token is ONLY available when connecting to the server via SSL (https://).
Because of this, the built-in Django runserver cannot execute a token exchange because
the LinkedIn secure cookie will not be available in the request.COOKIES dictionary.

To enable simple debugging capabilities with Django runserver, you may utilize stunnel.  As a
convenience, the auth_example project provides a file named 'fake_https' that will create a 
tunnel from port 8443 to port 8000 (the default runserver port).  Essentially:

    browser ---> https://localhost:8443 ---> http://localhost:8000 ---> HTTPS=1 python manage.py runserver
    
Without this you will be unable to login via LinkedIn.

To run the Django webserver, you must also fake HTTPS support so that calls to request.is_secure()
return True.  To do this, execute the following from the command line:

    HTTPS=1 python manage.py runserver


Contributors
------------

django-linkedinauth was written by [Michael Gile](http://mgile.com) ([@mgile](http://twitter.com/mgile)).

License
-------
   Copyright &copy; 2011 Michael Gile

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.