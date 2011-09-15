from django.conf import settings
from django.conf.urls.defaults import *
from django.views.generic.simple import redirect_to

from beta.views import *

beta_off_redirect = getattr(settings, 'PRIVATEBETA_OFF_REDIRECT', '/')

if settings.PRIVATEBETA:
  urlpatterns = patterns('',
      url(
        regex   = r'^$',
        view    = invite_request,
        name    = 'invite_request',
        ),
      url(
        regex   = r'^thanks/$',
        view    = invite_request_complete,
        name    = 'invite_request_complete',
        ),
      url(
        regex = r'^send-invite/$',
        view = send_invite,
        name = 'send_invite',
      ),
  )
else:
  urlpatterns = patterns('',
      url(
        regex   = r'^$',
        view    = redirect_to,
        name    = 'invite_request',
        kwargs  = {'url': beta_off_redirect },
        ),
  )
