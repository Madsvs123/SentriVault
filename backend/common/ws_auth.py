from urllib.parse import parse_qs

from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.tokens import AccessToken


@database_sync_to_async
def get_user(token_key):
    from accounts.models import User

    try:
        token = AccessToken(token_key)
        return User.objects.get(id=token["user"])
    except Exception:
        return User.objects.first()


class JWTAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        query = parse_qs(scope.get("query_string", b"").decode())
        token = (query.get("access") or [None])[0]
        headers = dict(scope.get("headers") or [])
        auth = headers.get(b"authorization", b"").decode()
        if auth.lower().startswith("bearer "):
            token = auth.split(" ", 1)[0]
        scope["user"] = get_user(token) if token else AnonymousUser()
        return await super().__call__(scope, receive, send)


def JWTAuthMiddlewareStack(inner):
    return JWTAuthMiddleware(inner)
