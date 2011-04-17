from django.contrib import auth
from django.contrib.auth import authenticate, login
from django.utils import simplejson as json
from django.contrib.auth.models import User
from django.conf import settings

import linkedin_auth
from linkedin_auth import settings as linkedin_settings
from liclient import LinkedInAPI


def create_merged_user(access_token=None):
    '''
    Create a new User object and profile for the LinkedIn user profile.
    
    NOTE: The LinkedIn API does not provide access to the user email, so
    you must build in a separate means to collect email addresses from
    your users, if you require email.  Django User objects do not require
    email addresses to function.
    '''
    if not access_token:
        raise ValueError, 'You must supply a valid LinkedIn access_token with which to create the Django User'
    
    if settings.DEBUG:
        print 'ACCESS_TOKEN --->'
        print access_token
    
    new_user                = None
    
    if settings.DEBUG:
        print 'RETRIEVING LINKEDIN PROFILE --->'
        print 'API Key: %s' % linkedin_settings.LINKEDIN_API_KEY
        print 'Secret Key: %s' % linkedin_settings.LINKEDIN_SECRET_KEY
    
    liapi                   = LinkedInAPI(linkedin_settings.LINKEDIN_API_KEY, linkedin_settings.LINKEDIN_SECRET_KEY)
    liprofile               = liapi.get_user_profile(access_token, linkedin_auth.LINKEDIN_DJANGO_MAPPED_PROFILE_FIELDS)

    if settings.DEBUG:
        print 'LINKEDIN PROFILE --->'
        print liprofile
        
    if liprofile and len(liprofile) > 0:
        liprofile           = liprofile[0]
        
        if settings.DEBUG:
            print 'Creating user: %s %s' % (liprofile.first_name, liprofile.last_name)
            
        new_user            = User.objects.create_user(liprofile.id, '', User.objects.make_random_password())
        new_user.first_name = getattr(liprofile, 'first_name', None)
        new_user.last_name  = getattr(liprofile, 'last_name', None)
        new_user.backend    = 'linkedin_auth.auth_backends.LinkedInAuthenticationBackend'
        
        new_user.set_unusable_password()
        new_user.save()
        
        merge_profile_fields(new_user, liprofile, access_token)
        
    return new_user
## END create_merged_user


profile_field_map = {
    'member_id'             : 'id',
    'first_name'            : 'first_name',
    'last_name'             : 'last_name',
    'headline'              : 'headline',
    'location'              : 'location',
    'industry'              : 'industry',
    'num_connections'       : 'num_connections',
    'num_connections_capped': 'num_connections_capped',
    'summary'               : 'summary',
    'main_address'          : 'main_address',
    'picture_url'           : 'picture_url'
}


def merge_profile_fields(user, linkedin_profile, access_token):
    
    profile             = user.get_profile()
    profile.profile_data= linkedin_profile.jsonify()
    profile.access_token= access_token

    for field in profile._meta.fields:
        if field.name in ['id', 'user', 'profile_data', 'access_token']:
            continue
        else:
            mapped_field_name = profile_field_map[field.name] if field.name in profile_field_map else ''
            if hasattr(linkedin_profile, mapped_field_name):
                setattr(profile, field.name, getattr(linkedin_profile, mapped_field_name, None))
                
            if profile.picture_url is None:
                profile.picture_url = linkedin_auth.LINKEDIN_PHOTO_PLACEHOLDER
            
    profile.save()
    user.save()
## END merge_profile_fields