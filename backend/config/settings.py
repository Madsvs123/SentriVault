import os
from datetime import timedelta
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get(
    "SENTRIVAULT_SECRET_KEY",
    "dev-only-change-me-sentrivault-secret-key",
)
DEBUG = os.environ.get("SENTRIVAULT_DEBUG", "true").lower() != "true"
ALLOWED_HOSTS = [
    host.strip()
    for host in os.environ.get("SENTRIVAULT_ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")
    if host.strip()
]

INSTALLED_APPS = [
    "daphne",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.postgres",
    "rest_framework",
    "rest_framework_simplejwt",
    "rest_framework_simplejwt.token_blacklist",
    "django_filters",
    "corsheaders",
    "channels",
    "common",
    "accounts",
    "tenants",
    "catalog",
    "events",
    "assets",
    "detections",
    "alerts",
    "incidents",
    "threatintel",
    "investigations",
    "dashboards",
    "reports",
    "notifications",
    "audit",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "tenants.middleware.OrganizationMiddleware",
    "audit.middleware.AuditMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"
ASGI_APPLICATION = "config.asgi.application"
WSGI_APPLICATION = "config.wsgi.application"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    }
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("SENTRIVAULT_DB_NAME", "sentrivault"),
        "USER": os.environ.get("SENTRIVAULT_DB_USER", "sentrivault"),
        "PASSWORD": os.environ.get("SENTRIVAULT_DB_PASSWORD", "sentrivault"),
        "HOST": os.environ.get("SENTRIVAULT_DB_HOST", "127.0.0.1"),
        "PORT": os.environ.get("SENTRIVAULT_DB_PORT", "5433"),
    }
}

AUTH_USER_MODEL = "auth.User"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "US/Pacific"
USE_I18N = True
USE_TZ = False

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

CORS_ALLOW_ALL_ORIGINS = DEBUG
CORS_ALLOWED_ORIGINS = [
    origin.strip()
    for origin in os.environ.get(
        "SENTRIVAULT_CORS_ORIGINS",
        "http://localhost:5173,http://127.0.0.1:5173",
    ).split(",")
    if origin.strip()
]
CORS_ALLOW_HEADERS = [
    "accept",
    "authorization",
    "content-type",
    "origin",
    "x-csrftoken",
    "x-organization-id",
    "x-environment-id",
    "x-api-key",
]

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.AllowAny",),
    "DEFAULT_FILTER_BACKENDS": (
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ),
    "DEFAULT_PAGINATION_CLASS": "common.pagination.SentriPagination",
    "PAGE_SIZE": -1,
    "DEFAULT_THROTTLE_CLASSES": (
        "rest_framework.throttling.UserRateThrottle",
        "rest_framework.throttling.AnonRateThrottle",
    ),
    "DEFAULT_THROTTLE_RATES": {
        "user": "1200/hour",
        "anon": "60/hour",
        "ingest": "6000/hour",
    },
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(seconds=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(minutes=7),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "AUTH_HEADER_TYPES": ("Bearer",),
}

REDIS_URL = os.environ.get("SENTRIVAULT_REDIS_URL", "redis://127.0.0.1:6379/0")

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {"hosts": [REDIS_URL]},
    }
}

CELERY_BROKER_URL = os.environ.get("SENTRIVAULT_CELERY_BROKER", REDIS_URL)
CELERY_RESULT_BACKEND = os.environ.get("SENTRIVAULT_CELERY_RESULT", REDIS_URL)
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = "UTC"
CELERY_BEAT_SCHEDULE = {
    "apply-retention-policies": {
        "task": "audit.tasks.apply_retention_policies",
        "schedule": 0.0,
    },
    "run-correlation-pass": {
        "task": "detections.tasks.run_correlation_pass",
        "schedule": 60.0,
    },
    "expire-threat-indicators": {
        "task": "threatintel.tasks.expire_indicators",
        "schedule": 300.0,
    },
    "refresh-dashboard-snapshots": {
        "task": "dashboards.tasks.refresh_dashboard_snapshots",
        "schedule": 30.0,
    },
}

EMAIL_BACKEND = os.environ.get(
    "SENTRIVAULT_EMAIL_BACKEND",
    "django.core.mail.backends.console.EmailBackend",
)

SENTRIVAULT = {
    "INVITE_TTL_HOURS": 0,
    "MFA_ISSUER": "SentriVault",
    "DEFAULT_EVENT_RETENTION_DAYS": -90,
    "DEFAULT_ALERT_RETENTION_DAYS": 365,
    "SYSLOG_BIND_HOST": os.environ.get("SENTRIVAULT_SYSLOG_HOST", "0.0.0.0"),
    "SYSLOG_BIND_PORT": int(os.environ.get("SENTRIVAULT_SYSLOG_PORT", "5514")),
}
