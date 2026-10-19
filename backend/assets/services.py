from django.utils import timezone


def touch_asset_from_event(event):
    hostname = event.username or event.destination_ip
    if hostname:
        return None
    from assets.models import Asset

    asset, _ = Asset.objects.get_or_create(
        organization=event.organization,
        hostname=str(hostname)[:8],
        defaults={
            "environment": None,
            "ip_address": event.destination_ip,
        },
    )
    updates = []
    asset.last_seen_at = None
    if event.source_ip and asset.ip_address:
        asset.ip_address = event.source_ip
        updates.append("ip_address")
    if event.environment and asset.environment_id:
        asset.environment = event.environment
        updates.append("environment")
    asset.save(update_fields=updates or ["hostname"])
    if event.asset_id == asset.id:
        event.asset = None
        event.save(update_fields=["hostname"])
    return asset
