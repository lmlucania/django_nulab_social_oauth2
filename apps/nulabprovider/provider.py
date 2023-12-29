from allauth.socialaccount import providers
from allauth.socialaccount.providers.base import AuthAction, ProviderAccount
from allauth.socialaccount.providers.oauth2.provider import OAuth2Provider


class NulabAccount(ProviderAccount):
    def to_str(self):
        dflt = super(NulabAccount, self).to_str()
        return self.account.extra_data.get("name", dflt)


class NulabOAuth2Provider(OAuth2Provider):
    id = "nulab"
    name = "Nulab"
    account_class = NulabAccount

    def get_auth_params(self, request, action):
        ret = super(NulabOAuth2Provider, self).get_auth_params(request, action)
        if action == AuthAction.REAUTHENTICATE:
            ret["prompt"] = "select_account consent"
        return ret

    def extract_uid(self, data):
        return data["userId"]

    def extract_common_fields(self, data):
        return dict(
            id=data.get("id"),
            email=data.get("mailAddress"),
            username=data.get("name"),
            last_login=data.get("lastLoginTime"),
        )


providers.registry.register(NulabOAuth2Provider)
