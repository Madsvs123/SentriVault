from django.contrib import admin

from detections.models import Allowlist, DetectionRule, RuleVersion, Suppression

admin.site.register(DetectionRule)
admin.site.register(RuleVersion)
admin.site.register(Allowlist)
admin.site.register(Suppression)
