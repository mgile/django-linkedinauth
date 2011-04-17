from django.conf import settings
import urllib

try:
    import simplejson as json
except ImportError:
    import json


LINKEDIN_COOKIE_PREFIX  = 'linkedin_oauth_'


def get_credential_cookie(request=None):
    '''
    LinkedInCrendentialCookie implements the JSAPI to REST OAuth2
    token handoff as documented at:
    
        http://developer.linkedin.com/docs/DOC-1252
        
    The purpose of this handoff is to allow an ideal tradeoff
    between usability on the client side with the LinkedIn
    sign-in button, but preserving the ability for the server
    to store the auth token for use in server-side API functions.
    
    The secure cookie may only be retrieved over an SSL connection
    (i.e. HTTPS).
    
    From the LinkedIn developer documentation: 
    
    The cookie is named linkedin_oauth_API_KEY, where API_KEY is your 
    application's LinkedIn API key. (This is also known as a "consumer_key" in OAuth.)
 
    Its value is a JSON object, which looks like this:
    
        {
             "signature_method" :"HMAC-SHA1",
             "signature_order"  : ["access_token", "member_id"],
             "access_token"     :"AD2dpVe1tOclAsNYsCri4nOatfstw7ZnMzWP",
             "signature"        :"73f948524c6d1c07b5c554f6fc62d824eac68fee",
             "member_id"        :"vvUNSej47H"
             "signature_version": 1
        }
    '''
    cookie_name    = '%s%s' % (LINKEDIN_COOKIE_PREFIX, settings.LINKEDIN_API_KEY)
        
    if cookie_name in request.COOKIES:
        cookie         = json.loads(urllib.unquote(request.COOKIES[cookie_name]))
    else:
        cookie          = {}
    
    return cookie
## END get_credential_cookie

def valid_cookie(credential_cookie={}):
    
    credential_keys = [
        'signature_method',
        'signature_order',
        'access_token',
        'signature',
        'member_id',
        'signature_version'
    ]
    
    # TODO: Verify signature on cookie

    return all([key in credential_cookie for key in credential_keys])
## END is_valid_cookie