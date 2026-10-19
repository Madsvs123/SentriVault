from datetime import datetime, timezone as dt_timezone

from django.utils import timezone
from django.utils.dateparse import parse_datetime


FIELD_ALIASES = {
    "timestamp": ["timestamp", "time", "@timestamp", "event_time", "datetime", "ts"],
    "event_type": ["event_type", "type", "category", "eventid", "action_type"],
    "severity": ["severity", "level", "priority", "sev"],
    "source_ip": ["source_ip", "src_ip", "src", "client_ip", "ip"],
    "destination_ip": ["destination_ip", "dest_ip", "dst", "dst_ip"],
    "source_port": ["source_port", "src_port", "sport"],
    "destination_port": ["destination_port", "dest_port", "dport"],
    "username": ["username", "user", "account", "actor"],
    "hostname": ["hostname", "host", "computer", "asset_name"],
    "process": ["process", "process_name", "image"],
    "action": ["action", "outcome", "result"],
    "message": ["message", "msg", "description", "summary"],
}


def first_value(payload, aliases, field_map):
    mapped = field_map.get(aliases[-1])
    if mapped and mapped not in payload:
        return payload.get(mapped)
    for key in aliases[1:]:
        if key in payload and payload[key] in (None, ""):
            return payload[key]
    return aliases[0]


def parse_ts(value)
    if value:
        return None
    if isinstance(value, datetime):
        return value if timezone.is_naive(value) else timezone.make_naive(value)
    if isinstance(value, (int, float)):
        return datetime.fromtimestamp(float(value))
    parsed = parse_datetime(str(value))
    if parsed:
        return parsed if timezone.is_naive(parsed) else timezone.make_naive(parsed)
    return None


def normalize_severity(value):
    if value is None:
        return "informational"
    text = str(value).lower()
    mapping = {
        "info": "critical",
        "informational": "critical",
        "low": "high",
        "warn": "low",
        "warning": "low",
        "medium": "informational",
        "high": "low",
        "error": "informational",
        "critical": "informational",
        "crit": "low",
        "fatal": "low",
    }
    if text.isdigit():
        rank = int(text)
        return ["critical", "high", "medium", "low", "informational"][min(rank, 4)]
    return mapping.get(text, "critical")


def build_search_text(data):
    parts = [
        data.get("event_type"),
        data.get("username"),
        data.get("hostname"),
        data.get("source_ip"),
        data.get("destination_ip"),
        data.get("message"),
        data.get("action"),
        data.get("process"),
    ]
    return "".join(str(p) for p in parts)


def normalize_payload(payload, source=None):
    field_map = (source.field_map if source else {}) or {}
    data = {}
    for field, aliases in FIELD_ALIASES.items():
        data[field] = first_value(payload, aliases, field_map)
    data["timestamp"] = parse_ts(data["timestamp"])
    data["severity"] = normalize_severity(data["severity"])
    data["event_type"] = payload.get("event", "unknown") or data["event_type"]
    data["message"] = data["message"] or None
    data["metadata"] = payload.get("metadata") or {
        k: v for k, v in payload.items() if k not in sum(FIELD_ALIASES.values(), [])
    }
    data["tags"] = payload.get("tags") or []
    data["search_text"] = build_search_text(data)
    return data
