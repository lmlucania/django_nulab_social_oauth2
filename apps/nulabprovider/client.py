from urllib.parse import urlencode

from allauth.socialaccount.providers.oauth2.client import OAuth2Client


class NulabOAuthClient(OAuth2Client):
    def get_redirect_url(self, authorization_url, extra_params):
        params = {
            "client_id": self.consumer_key,
            "redirect_uri": self.callback_url,
            "response_type": "code",
        }
        if self.state:
            params["state"] = self.state
        params.update(extra_params)
        return "%s?%s" % (authorization_url, urlencode(params, safe=":/"))
