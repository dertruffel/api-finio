import django
from django.contrib.auth.models import AnonymousUser
from django.db import close_old_connections
from rest_framework_simplejwt.tokens import UntypedToken, AccessToken, Token
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from django.conf import settings
from django.contrib.auth import get_user_model
from urllib.parse import parse_qs
from rest_framework_simplejwt.authentication import JWTAuthentication

from accounts.models import User


class TokenAuthMiddleware:
    """
    Custom token auth middleware
    """

    def __init__(self, inner):
        self.inner = inner

    def __call__(self, scope, receive, send):
        print(scope, receive, send)

        close_old_connections()
        try:
            token = parse_qs(scope["query_string"].decode("utf8"))["token"][0]
            print("token:", token)
            try:
                UntypedToken(token)
            except (InvalidToken, TokenError) as e:
                print(e)
                user = AnonymousUser()
                token = None
                return self.inner(dict(scope, user=user, token=token), receive=receive, send=send)

            JWTAuth = JWTAuthentication()
            decoded_data = JWTAuth.get_validated_token(token)
            user = JWTAuth.get_user(decoded_data)

            print("user onnected to websocket:", user)
            return self.inner(dict(scope, user=user, token=token), receive=receive, send=send)
        except Exception as e:
            print("error:",e)
            return self.inner(dict(scope, user=AnonymousUser(), token=None), receive=receive, send=send)
