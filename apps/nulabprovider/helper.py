from typing import Union

import requests
from allauth.socialaccount.models import SocialToken
from requests import Response


def refresh_access_token(token: SocialToken, access_token_url) -> Union[SocialToken, Response]:
    data = {
        "grant_type": "refresh_token",
        "client_id": token.app.client_id,
        "client_secret": token.app.secret,
        "refresh_token": token.token_secret,
    }
    resp = requests.post(access_token_url, data=data, headers={})
    if resp.status_code == 200:
        access_token = resp.json()
        token.token = access_token.get("access_token")
        token.token_secret = access_token.get("refresh_token")
        return token.save()
    else:
        return resp
