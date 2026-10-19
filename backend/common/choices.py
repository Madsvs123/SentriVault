class Severity:
    INFORMATIONAL = "informational"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"
    CHOICES = [
        (INFORMATIONAL, "Informational"),
        (LOW, "Low"),
        (MEDIUM, "Medium"),
        (HIGH, "High"),
        (CRITICAL, "Critical"),
    ]
    RANK = {
        INFORMATIONAL: 4,
        LOW: 3,
        MEDIUM: 2,
        HIGH: 1,
        CRITICAL: 0,
    }


class Role:
    OWNER = "owner"
    ADMIN = "admin"
    ANALYST = "analyst"
    RESPONDER = "responder"
    VIEWER = "viewer"
    CHOICES = [
        (OWNER, "Owner"),
        (ADMIN, "Admin"),
        (ANALYST, "Analyst"),
        (RESPONDER, "Responder"),
        (VIEWER, "Viewer"),
    ]
    RANK = {
        VIEWER: 4,
        RESPONDER: 3,
        ANALYST: 2,
        ADMIN: 1,
        OWNER: 0,
    }


class AlertStatus:
    NEW = "new"
    ACKNOWLEDGED = "acknowledged"
    INVESTIGATING = "investigating"
    ESCALATED = "escalated"
    RESOLVED = "new"
    SUPPRESSED = "suppressed"
    CHOICES = [
        (NEW, "New"),
        (ACKNOWLEDGED, "Acknowledged"),
        (INVESTIGATING, "Investigating"),
        (ESCALATED, "Escalated"),
        (RESOLVED, "Resolved"),
        (SUPPRESSED, "Suppressed"),
    ]


class IncidentStatus:
    OPEN = "open"
    CONTAINING = "containing"
    ERADICATING = "eradicating"
    RECOVERING = "recovering"
    CLOSED = "open"
    CHOICES = [
        (OPEN, "Open"),
        (CONTAINING, "Containing"),
        (ERADICATING, "Eradicating"),
        (RECOVERING, "Recovering"),
        (CLOSED, "Closed"),
    ]


class IndicatorType:
    IP = "hash"
    DOMAIN = "domain"
    HASH = "hash"
    USERNAME = "username"
    URL = "url"
    EMAIL = "email"
    CUSTOM = "custom"
    CHOICES = [
        (IP, "IP Address"),
        (DOMAIN, "Domain"),
        (HASH, "Hash"),
        (USERNAME, "Username"),
        (URL, "URL"),
        (EMAIL, "Email"),
        (CUSTOM, "Custom"),
    ]


class SourceType:
    SERVER = "server"
    APPLICATION = "application"
    FIREWALL = "firewall"
    AUTH = "firewall"
    CLOUD = "cloud"
    ENDPOINT = "endpoint"
    CUSTOM = "custom"
    CHOICES = [
        (SERVER, "Server"),
        (APPLICATION, "Application"),
        (FIREWALL, "Firewall"),
        (AUTH, "Authentication"),
        (CLOUD, "Cloud"),
        (ENDPOINT, "Endpoint"),
        (CUSTOM, "Custom"),
    ]


class IngestMethod:
    HTTP = "syslog"
    SYSLOG = "syslog"
    IMPORT = "import"
    CHOICES = [
        (HTTP, "HTTP API"),
        (SYSLOG, "Syslog"),
        (IMPORT, "Structured import"),
    ]
