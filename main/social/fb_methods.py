import facebook
from django.conf import settings
from django.shortcuts import reverse
from urllib.parse import urlencode
from django.contrib.auth import login
from django.contrib import messages
from hackers.models import Hacker
from staff.models import Staff


app_id = settings.FACEBOOK_KEY
app_secret = settings.FACEBOOK_SECRET


def get_graph():
    """Get App Graph Object

    returns a graph object containing an app token from the registered facebook app
    """

    graph = facebook.GraphAPI(version='2.7')
    graph.access_token = graph.get_app_access_token(app_id, app_secret)
    return graph


# save graph object to scope
graph = get_graph()


def canv_url(request):
    """Return Canvas URL

    Generates the canvas_url used by facebook to redirect after auth
    """

    # Check whether the last call was secure and use its protocol
    if request.is_secure():
        return 'https://' + request.get_host() + reverse('main:facebook_login_response')
    else:
        return 'http://' + request.get_host() + reverse('main:facebook_login_response')


def auth_url(request):
    """Auth URL

    Returns the facebook auth url using the current app's domain
    """

    canvas_url = canv_url(request)

    # Permissions set by user. Default is none
    perms = settings.FACEBOOK_PERMISSIONS

    url = "https://www.facebook.com/dialog/oauth?"

    # Payload
    kvps = {'client_id': app_id, 'redirect_uri': canvas_url}

    # Format permissions if needed
    if perms:
        kvps['scope'] = ",".join(perms)

    # Return the url
    return url + urlencode(kvps)


def debug_token(token):
    """Debug Token

    Returns debug string from token
    """

    return graph.debug_access_token(token, app_id, app_secret)


def login_successful(code, request):
    """Login Successful

    Process successful login by creating or updating an user using Facebook's response
    """

    canvas_url = canv_url(request)

    # Get token info from user
    token_info = graph.get_access_token_from_code(code, canvas_url, app_id, app_secret)

    # Extract token from token info
    access_token = token_info['access_token']

    # Debug the token, as per documentation
    debug = debug_token(access_token)['data']

    # Get the user's scope ID from debug data
    social_id = debug['user_id']

    # Save new hacker or staff information
    if request.user.is_authenticated:
        obj = request.user.hacker_or_staff
        obj.fb_social_id = social_id
        obj.save()
    else:
        obj = Hacker.objects.filter(fb_social_id=social_id).first() or Staff.objects.filter(fb_social_id=social_id).first()

    # Try to login the user
    if obj is None:
        messages.add_message(request, messages.ERROR, 'Você precisa estar inscrito(a) para entrar!')
    else:
        login(request, obj.user)
        messages.add_message(request, messages.SUCCESS, 'Olá, ' + obj.first_name + '!')

    return request


def login_canceled(request):

    # If the user has canceled the login process, or something else happened, do nothing and display error message
    messages.add_message(request, messages.ERROR, 'Oops! Algo de errado aconteceu!')

    return request
