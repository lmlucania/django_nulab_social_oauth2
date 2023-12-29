from allauth.socialaccount.providers.oauth2.urls import default_urlpatterns

from .provider import NulabOAuth2Provider

app_name = "apps.nulabprovider"

urlpatterns = default_urlpatterns(NulabOAuth2Provider)
