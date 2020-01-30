"""
URLconf for registration and activation, using django-registration's
default backend.

If the default behavior of these views is acceptable to you, simply
use a line like this in your root URLconf to set up the default URLs
for registration::

    (r'^accounts/', include('registration.backends.default.urls')),

This will also automatically set up the views in
``django.contrib.auth`` at sensible default locations.

If you'd like to customize registration behavior, feel free to set up
your own URL patterns for these views instead.

"""


from django.conf.urls import patterns
from django.conf.urls import include
from django.conf.urls import url
from django.http import request
from django.views.generic.base import TemplateView
from django.contrib.sites.models import Site

from erp.registration.backends.default.views import ActivationView
from erp.registration.backends.default.views import RegistrationView


urlpatterns = patterns('',
                       url(r'^activate/complete/$',
                           TemplateView.as_view(template_name='registration/activation_complete.html'),
                           {'site':Site.objects.get_current()},
                           name='registration_activation_complete'),
                       # Activation keys get matched by \w+ instead of the more specific
                       # [a-fA-F0-9]{40} because a bad activation key should still get to the view;
                       # that way it can return a sensible "invalid key" message instead of a
                       # confusing 404.
                       url(r'^activate/(?P<activation_key>\w+)/$',
                           ActivationView.as_view(),
                           name='erp.registration_activate'),
                       url(r'^avator/change/$',
                           'erp.avator_management.views.change'),
                       url(r'^register/$',
                           RegistrationView.as_view(),
                           name='erp.registration_register'),
                       url(r'^register/complete/$',
                           TemplateView.as_view(template_name='registration/registration_complete.html'),
                           name='registration_complete'),
                       url(r'^register/closed/$',
                           TemplateView.as_view(template_name='registration/registration_closed.html'),
                           name='erp.registration_disallowed'),
                       url(r'^profile/(?P<u_id>\d+)/$',
                           'erp.user_management.views.profile'),
                       url(r'^profile/$',
                           'erp.user_management.views.profile'),
                       (r'', include('erp.registration.auth_urls')),
                       )
