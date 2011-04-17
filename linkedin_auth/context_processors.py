import linkedin_auth
from linkedin_auth import settings as lisettings
    
def linkedin(request):
    contextdict = {
        'LINKEDIN_API_KEY'          : lisettings.LINKEDIN_API_KEY,
        'LINKEDIN_LOGIN_JS_HELPER'  : linkedin_auth.LINKEDIN_LOGIN_JS_HELPER,
        'LINKEDIN_LOGOUT_JS_HELPER' : linkedin_auth.LINKEDIN_LOGOUT_JS_HELPER,
        'LINKEDIN_PHOTO_PLACEHOLDER': linkedin_auth.LINKEDIN_PHOTO_PLACEHOLDER
    }

    return contextdict
## END linkedin