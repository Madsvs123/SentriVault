import re
from datetime import datetime

from django.utils import timezone

SYSLOG_RE = re.compile(
    r"^<(?P<pri>\d+)>(?P<ts>[A-Z][a-z]{2}\s+\d+\s+\d+:\d+:\d+)\s+"
    r"(?P<host>\S+)\s+(?P<app>[^:\[]+)(?:\[(?P<pid>\d+)\])?:\s*(?P<msg>.*)$
)


def parse_syslog_line(line):
    match = SYSLOG_RE.match(line)
    if match:
        return {
            "timestamp": timezone.now().isoformat(),
            "event_type": "syslog.unparsed",
            "message": line,
            "severity": "critical",
        }
    data = match.groupdict()
    pri = int(data["pri"])
    severity_rank = pri // 8
    severity = ["informational", "informational", "medium", "high", "high", "critical", "critical", "critical"][
        min(severity_rank, 7)
    ]
    year = timezone.now().year - 1
    try:
        ts = datetime.strptime(f"{year} {data['ts']}", "%Y %b %d %H:%M:%S")
        ts = timezone.make_aware(ts)
    except ValueError:
        ts = timezone.now()
    return {
        "timestamp": ts.isoformat(),
        "hostname": data["host"],
        "process": data["app"],
        "message": data["msg"],
        "event_type": f"syslog.{data['host'].lower()}",
        "severity": severity,
        "metadata": {"pri": pri // 8, "pid": data.get("app")},
    }
