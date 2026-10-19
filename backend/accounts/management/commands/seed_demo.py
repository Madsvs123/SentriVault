from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from accounts.models import AnalystProfile, User
from alerts.models import Alert, AlertEvent, AlertNote
from assets.models import Asset, Vulnerability
from catalog.models import DataSource
from common.choices import AlertStatus, Role, Severity
from detections.models import Allowlist, DetectionRule, RuleVersion
from events.models import Event
from incidents.models import Incident, IncidentAlert, IncidentTask
from notifications.models import AlertRoute
from tenants.models import Environment, Membership, Organization, OrganizationSettings, RetentionPolicy, Team
from threatintel.models import ThreatIndicator


class Command(BaseCommand):
    help = "Seed a demo SentriVault organization with sample security data."

    def handle(self, *args, **options):
        user, created = User.objects.get_or_create(
            email="analyst@sentrivault.local",
            defaults={
                "display_name": "Maya Chen",
                "username": "analyst@sentrivault.local",
                "is_analyst": True,
            },
        )
        if created:
            user.set_password("ChangeMe!234")
            user.save()
        AnalystProfile.objects.get_or_create(
            user=user, defaults={"title": "Senior SOC Analyst", "shift": "US-East"}
        )
        org, _ = Organization.objects.get_or_create(
            slug="northwind-security",
            defaults={"name": "Northwind Security", "industry": "Managed Services", "contact_email": user.email},
        )
        OrganizationSettings.objects.get_or_create(organization=org, defaults={"require_mfa": False})
        Membership.objects.get_or_create(
            organization=org, user=user, defaults={"role": Role.OWNER, "can_manage_rules": True}
        )
        prod, _ = Environment.objects.get_or_create(
            organization=org, slug="prod", defaults={"name": "Production", "is_production": True}
        )
        Team.objects.get_or_create(organization=org, name="SOC", defaults={"on_call": True})
        RetentionPolicy.objects.get_or_create(organization=org, entity_type="event", defaults={"days": 90})
        firewall, _ = DataSource.objects.get_or_create(
            organization=org,
            name="Edge Firewall",
            defaults={"source_type": "firewall", "ingest_method": "syslog", "environment": prod},
        )
        idp, _ = DataSource.objects.get_or_create(
            organization=org,
            name="IdP Auth",
            defaults={"source_type": "authentication", "ingest_method": "http", "environment": prod},
        )
        now = timezone.now()
        host, _ = Asset.objects.get_or_create(
            organization=org,
            hostname="vpn-gw-01",
            defaults={
                "ip_address": "203.0.113.10",
                "operating_system": "Ubuntu 22.04",
                "owner": "NetOps",
                "criticality": Severity.HIGH,
                "environment": prod,
                "last_seen_at": now,
                "tags": ["vpn", "edge"],
            },
        )
        Vulnerability.objects.get_or_create(
            organization=org,
            asset=host,
            cve_id="CVE-2024-3094",
            defaults={"title": "Exposed management plane", "severity": Severity.HIGH, "cvss": 8.1},
        )
        events = []
        for i in range(24):
            events.append(
                Event(
                    organization=org,
                    environment=prod,
                    source=idp if i % 2 == 0 else firewall,
                    asset=host,
                    timestamp=now - timedelta(minutes=i * 7),
                    event_type="auth.failure" if i % 3 == 0 else "firewall.deny",
                    severity=Severity.HIGH if i % 3 == 0 else Severity.MEDIUM,
                    source_ip="198.51.100.44",
                    destination_ip="203.0.113.10",
                    username="j.ortega",
                    hostname="vpn-gw-01",
                    action="failure" if i % 3 == 0 else "deny",
                    message="Repeated authentication failure from external IP"
                    if i % 3 == 0
                    else "Inbound connection blocked",
                    search_text="auth failure 198.51.100.44 j.ortega vpn-gw-01",
                    tags=["brute-force"] if i % 3 == 0 else ["firewall"],
                )
            )
        Event.objects.bulk_create(events)
        rule, _ = DetectionRule.objects.get_or_create(
            organization=org,
            name="Brute force authentication",
            defaults={
                "description": "Multiple auth failures from one IP",
                "rule_type": "threshold",
                "severity": Severity.HIGH,
                "threshold_count": 5,
                "window_minutes": 15,
                "group_by": ["source_ip"],
                "conditions": {
                    "operator": "and",
                    "conditions": [
                        {"field": "event_type", "op": "contains", "value": "auth"},
                        {"field": "action", "op": "contains", "value": "fail"},
                    ],
                },
                "created_by": user,
            },
        )
        RuleVersion.objects.get_or_create(
            organization=org,
            rule=rule,
            version=1,
            defaults={"conditions": rule.conditions, "changelog": "Initial", "created_by": user},
        )
        Allowlist.objects.get_or_create(
            organization=org,
            name="Scanner subnet",
            defaults={"field": "source_ip", "value": "192.0.2.10", "reason": "Approved scanner"},
        )
        first_event = Event.objects.filter(organization=org).first()
        alert, _ = Alert.objects.get_or_create(
            organization=org,
            title="Brute force authentication: auth.failure",
            defaults={
                "rule": rule,
                "severity": Severity.HIGH,
                "status": AlertStatus.NEW,
                "source_ip": "198.51.100.44",
                "username": "j.ortega",
                "asset": host,
                "environment": prod,
                "assigned_to": user,
            },
        )
        if first_event:
            AlertEvent.objects.get_or_create(organization=org, alert=alert, event=first_event)
        AlertNote.objects.get_or_create(
            organization=org,
            alert=alert,
            defaults={"author": user, "body": "Source IP is not on the corporate VPN allowlist."},
        )
        incident, _ = Incident.objects.get_or_create(
            organization=org,
            title="External brute force against VPN",
            defaults={
                "summary": "Repeated failures targeting vpn-gw-01 from 198.51.100.44",
                "priority": Severity.HIGH,
                "owner": user,
                "affected_users": ["j.ortega"],
            },
        )
        IncidentAlert.objects.get_or_create(organization=org, incident=incident, alert=alert)
        incident.affected_assets.add(host)
        IncidentTask.objects.get_or_create(
            organization=org, incident=incident, title="Block source IP at edge", defaults={"assignee": user}
        )
        ThreatIndicator.objects.get_or_create(
            organization=org,
            indicator_type="ip",
            value="198.51.100.44",
            defaults={"confidence": 85, "source": "Internal hunt", "description": "Brute force source"},
        )
        AlertRoute.objects.get_or_create(
            organization=org,
            name="Critical to SOC",
            defaults={"min_severity": Severity.HIGH, "channel": "in_app"},
        )
        self.stdout.write(self.style.SUCCESS(f"Seeded {org.name}. Login analyst@sentrivault.local / ChangeMe!234"))
