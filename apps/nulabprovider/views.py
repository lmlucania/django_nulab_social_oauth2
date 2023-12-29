import requests
from allauth.socialaccount.providers.oauth2.client import OAuth2Error
from allauth.socialaccount.providers.oauth2.views import (OAuth2Adapter,
                                                          OAuth2CallbackView,
                                                          OAuth2LoginView)
from django.conf import settings

from .client import NulabOAuthClient
from .helper import refresh_access_token
from .provider import NulabOAuth2Provider


class NulabOAuth2Adapter(OAuth2Adapter):
    client_class = NulabOAuthClient
    provider_id = NulabOAuth2Provider.id
    access_token_url = settings.SERVER_URL_PREFIX + "/api/v2/oauth2/token"
    authorize_url = settings.SERVER_URL_PREFIX + "/OAuth2AccessRequest.action"
    myself_url = settings.SERVER_URL_PREFIX + "/api/v2/users/myself"

    def complete_login(self, request, app, token, response, allow_refresh_token=True, **kwargs):
        headers = {"Authorization": "Bearer {0}".format(token.token)}
        resp = requests.get(self.myself_url, headers=headers)
        if resp.status_code == 200:
            return self.get_provider().sociallogin_from_response(request, resp.json())

        # アクセストークンの有効期限切れの場合
        elif (
            allow_refresh_token
            and resp.status_code == 401
            and resp.json().get("error_description") == "The access token expired."
        ):
            refresh_access_token(token, self.access_token_url)
            # 再帰呼び出し（アクセストークンの再取得はしない）
            self.complete_login(request, app, token, response, False, **kwargs)
        else:
            raise OAuth2Error(resp)


oauth2_login = OAuth2LoginView.adapter_view(NulabOAuth2Adapter)
oauth2_callback = OAuth2CallbackView.adapter_view(NulabOAuth2Adapter)
