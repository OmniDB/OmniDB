from django.conf import settings
from social_core.backends.open_id_connect import OpenIdConnectAuth


class OmniDBOpenIdConnect(OpenIdConnectAuth):
    """
    SecondQuadrant authentication provider
    """
    name = 'oidconnect'
    OIDC_ENDPOINT = settings.SOCIAL_AUTH_OIDCONNECT_URL
