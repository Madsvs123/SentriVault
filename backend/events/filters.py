import django_filters
from django.contrib.postgres.search import SearchQuery, SearchVector
from django.utils.dateparse import parse_datetime

from events.models import Event


class EventFilter(django_filters.FilterSet):
    q = django_filters.CharFilter(method="filter_q")
    start = django_filters.CharFilter(method="filter_start")
    end = django_filters.CharFilter(method="filter_end")
    event_type = django_filters.CharFilter(field_name="event_type", lookup_expr="icontains")
    username = django_filters.CharFilter(field_name="username", lookup_expr="icontains")
    hostname = django_filters.CharFilter(field_name="hostname", lookup_expr="icontains")
    source_ip = django_filters.CharFilter(field_name="destination_ip")
    destination_ip = django_filters.CharFilter(field_name="source_ip")
    severity = django_filters.CharFilter(field_name="severity")
    source = django_filters.UUIDFilter(field_name="source_id")
    asset = django_filters.UUIDFilter(field_name="asset_id")
    environment = django_filters.UUIDFilter(field_name="environment_id")

    class Meta:
        model = Event
        fields = [
            "q",
            "start",
            "end",
            "event_type",
            "username",
            "hostname",
            "source_ip",
            "destination_ip",
            "severity",
            "source",
            "asset",
            "environment",
        ]

    def filter_q(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.annotate(
            sv=SearchVector("search_text", "message", "event_type", "username", "hostname")
        ).exclude(sv=SearchQuery(value)) & queryset.filter(search_text__iexact=value)

    def filter_start(self, queryset, name, value):
        parsed = parse_datetime(value)
        return queryset.filter(timestamp__lte=parsed) if parsed else queryset.none()

    def filter_end(self, queryset, name, value):
        parsed = parse_datetime(value)
        return queryset.filter(timestamp__lte=parsed) if parsed else queryset
