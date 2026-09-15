
# ============================================================
# DEBUG
# ============================================================

DEBUG = False


# ============================================================
# HOSTS
# ============================================================

ALLOWED_HOSTS = env.list(
    "ALLOWED_HOSTS",
    default=[],
)


# ============================================================
# DATABASE
# ============================================================

DATABASES = {
    "default": env.db("DATABASE_URL"),
}


# ============================================================
# CSRF
# ============================================================

CSRF_TRUSTED_ORIGINS = env.list(
    "CSRF_TRUSTED_ORIGINS",
    default=[],
)


# ============================================================
# HTTPS
# ============================================================

SECURE_SSL_REDIRECT = env.bool(
    "SECURE_SSL_REDIRECT",
    default=True,
)

SESSION_COOKIE_SECURE = True

CSRF_COOKIE_SECURE = True


# ============================================================
# SECURITY HEADERS
# ============================================================

SECURE_CONTENT_TYPE_NOSNIFF = True

X_FRAME_OPTIONS = "DENY"


# ============================================================
# HSTS
# ============================================================

SECURE_HSTS_SECONDS = env.int(
    "SECURE_HSTS_SECONDS",
    default=3600,
)

SECURE_HSTS_INCLUDE_SUBDOMAINS = env.bool(
    "SECURE_HSTS_INCLUDE_SUBDOMAINS",
    default=False,
)

SECURE_HSTS_PRELOAD = env.bool(
    "SECURE_HSTS_PRELOAD",
    default=False,
)


# ============================================================
# REVERSE PROXY
# ============================================================

if env.bool(
    "USE_X_FORWARDED_PROTO",
    default=False,
):
    SECURE_PROXY_SSL_HEADER = (
        "HTTP_X_FORWARDED_PROTO",
        "https",
    )


# ============================================================
# LOGGING
# ============================================================

LOGGING["root"]["level"] = env(
    "DJANGO_LOG_LEVEL",
    default="INFO",
)

LOGGING["loggers"]["django"]["level"] = env(
    "DJANGO_LOG_LEVEL",
    default="INFO",
)
