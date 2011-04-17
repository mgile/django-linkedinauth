from django.conf import settings
from django.contrib.auth import backends
from django.db import models as db_models
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.contenttypes.models import ContentType
from linkedin_auth.utils import get_credential_cookie, valid_cookie
from linkedin_auth import settings as linkedin_settings
from linkedin_auth.merge import create_merged_user

from linkedin_auth.utils import get_credential_cookie, valid_cookie
from liclient import LinkedInAPI

class LinkedInAuthenticationBackend(backends.ModelBackend):
    
    def authenticate(self, request=None):
        '''
        Lookup a User model based on their LinkedIn member ID. If 
        the profile exists, then they have already successfully
        merged their LinkedIn account and their Django app, so the
        User is considered authenticated and is returned.
        '''
        liapi           = LinkedInAPI(linkedin_settings.LINKEDIN_API_KEY, linkedin_settings.LINKEDIN_SECRET_KEY)
        cred_cookie     = get_credential_cookie(request)
        if not valid_cookie(cred_cookie):
            return None
        
        '''
        This is the actual "login" step, as it verifies the already 
        logged-in LinkedIn user, whose credential cookie was created after
        successfully logging in with the JSAPI.
        '''
        access_token    = liapi.exchange_bearer_token(cred_cookie)
        if not self._verify_access_token(access_token):
            return None       
        
        user            = self._lookup_user_by_token(access_token, cred_cookie['member_id'])
        if not user:
            user        = create_merged_user(access_token)
            
        if settings.DEBUG:
            print 'AUTHENTICATING USER ---> %s' % user
            
        return user
    ## END authenticate
        
        
    def _lookup_user_by_token(self, access_token, member_id):
        user            = None
        profile_module  = getattr(settings, 'AUTH_PROFILE_MODULE', None)
        if profile_module:
            app_label, model_name = settings.AUTH_PROFILE_MODULE.split('.')
            profile_model = db_models.get_model(app_label, model_name)
            if profile_model:
                profile_class = ContentType.objects.get_for_model(profile_model).model_class()
                try:
                    profile = profile_class.objects.get(member_id__iexact=member_id)
                    user    = profile.user
                except ObjectDoesNotExist:
                    pass
                    
        return user
    ## END _lookup_user_by_token
    
    def _verify_access_token(self, access_token):
        if 'oauth_problem' in access_token:
            if settings.DEBUG:
                print 'OAUTH ERROR ---> %s' % access_token['oauth_problem']
            # TODO: log the actual problem message
            return False
        
        required_fields = ['oauth_token_secret', 'oauth_authorization_expires_in', 'oauth_token', 'oauth_expires_in']
    
        if not all([req in access_token for req in required_fields]):
            return False
            
        return True
        
    ## END _verify_access_token
## END LinkedInAuthenticationBackend