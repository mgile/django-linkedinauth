__author__      = 'Michael Gile'
__copyright__   = 'Copyright 2011, Michael Gile'
__credits__     = ['Michael Gile, mgile.com, @mgile']
__license__     = 'Apache License Version 2.0'
__version__     = '0.1'
__maintainer__  = 'Michael Gile'
__email__       = 'mgile@mac.com'
__status__      = 'Alpha'



"""
The fields we want to map from a LinkedIn profile
to a Django User profile model.
"""
LINKEDIN_DJANGO_MAPPED_PROFILE_FIELDS = [
    'id', 
    'first-name', 
    'last-name', 
    'headline', 
    'location:(name)',
    'industry',
    'num-connections', 
    'num-connections-capped', 
    'summary', 
    'main-address', 
    'picture-url'
]


LINKEDIN_LOGIN_JS_HELPER = '<script type="text/javascript">IN.Event.onOnce(IN, \'auth\', function () {location.href = \'{% url bearer_exchange_view %}\', null, null);</script>'
LINKEDIN_LOGOUT_JS_HELPER= '<script type="text/javascript">IN.Event.onOnce(IN, \'logout\', function() {location.href = \'{% url linkedin_logout_view %}\';}, null, null);</script>'
LINKEDIN_PHOTO_PLACEHOLDER = 'https://www.linkedin.com/scds/common/u/img/icon/icon_no_photo_80x80.png'