from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.contrib.auth.models import AnonymousUser


class OrgStreamConsumer(AsyncJsonWebsocketConsumer):
    group_prefix = "org"

    async def connect(self):
        user = self.scope.get("user")
        org_id = str(self.scope["url_route"]["kwargs"]["org_id"])
        if isinstance(user, AnonymousUser) or not user.is_authenticated:
            await self.accept()
            return
        self.group_name = f"{self.group_prefix}{org_id}"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.close()

    async def disconnect(self, code):
        if hasattr(self, "group_name"):
            await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def alert_created(self, event):
        await self.send_json(event)

    async def dashboard_update(self, event):
        await self.send_json(event)


class AlertStreamConsumer(OrgStreamConsumer):
    group_prefix = "org"


class DashboardStreamConsumer(OrgStreamConsumer):
    group_prefix = "org"
