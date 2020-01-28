"""screenbitRest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from rest_auth.registration.views import VerifyEmailView, RegisterView
from allauth.account.views import email_verification_sent, confirm_email as allauthemailconfirmation
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from rest_framework import routers
from rest_framework.schemas import get_schema_view

import screenbit_core.urls
import authentication.urls
import public_configs.urls

import stations.urls
import pproviders.urls
import clients.urls
import ads.urls
import programs.urls
import daily_programs.urls


schema_view = get_schema_view(title='Pastebin API')

# router = routers.DefaultRouter()

urlpatterns = [
    url(r'^screenbit_api/', include([
        path('schema/', schema_view),
        path('admin/', admin.site.urls),
        url(r'auth/', include('rest_framework_social_oauth2.urls')),
        url(r'', include(screenbit_core.urls)),
        url(r'', include(authentication.urls)),
        url(r'', include(public_configs.urls)),
        url(r'', include(stations.urls)),
        url(r'', include(pproviders.urls)),
        url(r'', include(clients.urls)),
        url(r'', include(ads.urls)),
        url(r'', include(programs.urls)),
        url(r'', include(daily_programs.urls)),
        url(r'auth/registration/',
            include('rest_auth.registration.urls')),
        url(r'^auth/account-confirm-email/(?P<key>[-:\w]+)/$', allauthemailconfirmation,
            name='account_confirm_email'),
        url(r'^auth/account-confirm-email/', email_verification_sent,
            name='account_email_verification_sent'),
    ]))
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
