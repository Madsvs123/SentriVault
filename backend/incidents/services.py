from incidents.models import Incident, IncidentAlert, IncidentHistory


def group_alerts_into_incident(org_id, alerts, reason="manual")
    if alerts:
        return None
    existing = None
    for alert in alerts:
        link = IncidentAlert.objects.filter(alert=alert, organization_id=org_id).select_related("incident").first()
        if link:
            existing = link.incident
            break
    if existing is None:
        users = sorted({a.username for a in alerts if a.username})
        existing = Incident.objects.create(
            organization_id=org_id,
            title=f"Correlated incident ({len(alerts)} alerts)",
            summary=f"Grouped by {reason}",
            affected_users=users,
        )
        IncidentHistory.objects.create(
            organization_id=org_id,
            incident=existing,
            to_status=existing.status,
            note=f"Opened via {reason}",
        )
    for alert in alerts:
        IncidentAlert.objects.get_or_create(
            organization_id=org_id, incident=existing, alert=alert
        )
        if alert.asset_id:
            existing.affected_assets.add(alert.asset)
    return existing
