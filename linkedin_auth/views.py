from django.conf import settings
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, redirect
from django.template.context import RequestContext
from django.contrib.auth import authenticate, login, logout

def bearer_exchange_view(request):
    if settings.DEBUG:
        print 'COOKIES ----->'
        print '---> %s' % request.COOKIES
      
    if not request.is_secure():
        # HACK - Inject our test cookie
        request.COOKIES['linkedin_oauth_QW3KdK2JKx-53kUGiq5l_IyPP7sAZ4mEvIvJzZnJqJJOvu0G3qFagdnxmTGYgNyf'] = '%7B%22signature_version%22%3A%221%22%2C%22signature_method%22%3A%22HMAC-SHA1%22%2C%22signature_order%22%3A%5B%22access_token%22%2C%22member_id%22%5D%2C%22access_token%22%3A%227BgOCigNzVSYfQrLb2gnkFJJ_FY7-l0JNcGY%22%2C%22signature%22%3A%22Ke%2Fpm2A1whK5ecFdYzrVhRl5Fu8%3D%22%2C%22member_id%22%3A%22BGM7gC20nu%22%7D'

    
    
    user    = authenticate(request=request)
    context = RequestContext(request)
    if user: 
        login(request, user)
        context['profile_updated']  = False
        return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)
    else:
        context['exchange_error']   = 'Cannot authenticate your LinkedIn account, please try logging in again.  If the error persists, there may be a problem with the LinkedIn service.'
        return render_to_response('registration/login.html', context)
## END bearer_exchange_view


def linkedin_logout_view(request):
    logout(request)
    response = redirect(settings.LOGOUT_REDIRECT_URL)
    return HttpResponseRedirect(settings.LOGOUT_REDIRECT_URL)
## END linkedin_logout_view
