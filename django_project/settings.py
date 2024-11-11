"""
Django settings for django_project project.

Generated by 'django-admin startproject' using Django 5.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path

from cbs import BaseSettings
import environ

from django.utils.translation import gettext_lazy as _

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

envi = environ.Env()
envi.read_env(BASE_DIR / ".env")


ROOT_URLCONF = "django_project.urls"


WSGI_APPLICATION = "django_project.wsgi.application"


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = "en"
LANGUAGES = (
    ("fa", _("Persian")),
    ("en", _("English")),
)
LANGUAGES_BIDI = ["fa"]

LOCALE_PATHS = [BASE_DIR / "locale"]

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [str(BASE_DIR / "static")]

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# taggit
TAGGIT_CASE_INSENSITIVE = True

# session
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"

# tailwind
TAILWIND_APP_NAME = "theme"

# tinymce
TINYMCE_DEFAULT_CONFIG = {
    "height": "420px",
    "width": "960px",
    "menubar": "file edit view insert format tools table help",
    "plugins": "advlist autolink lists link image charmap print preview anchor searchreplace visualblocks code "
    "fullscreen insertdatetime media table paste code help wordcount spellchecker",
    "toolbar": "undo redo | bold italic underline strikethrough | fontselect fontsizeselect formatselect | alignleft "
    "aligncenter alignright alignjustify | outdent indent |  numlist bullist checklist | forecolor "
    "backcolor casechange permanentpen formatpainter removeformat | pagebreak | charmap emoticons | "
    "fullscreen  preview save print | insertfile image media pageembed template link anchor codesample | "
    "a11ycheck ltr rtl | showcomments addcomment code",
    "custom_undo_redo_levels": 10,
}


class Settings(BaseSettings):
    SECRET_KEY = "django-insecure-1xq=$6u(0oy7x3*li2glj6l3$tz#*6jq+je1&cs*uo!89%gba9"
    ALLOWED_HOSTS = ("localhost", "127.0.0.1")
    ADMIN_URL = "admin/"
    INTERNAL_IPS = ("127.0.0.1",)
    PASSWORD_HASHERS = ("django.contrib.auth.hashers.Argon2PasswordHasher",)
    SITE_ID = 1

    DEBUG = envi.bool("DEBUG", True)
    STORAGES = {
        "default": {
            "BACKEND": "django.core.files.storage.FileSystemStorage",
        },
        "staticfiles": {
            "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
        },
    }
    TEMPLATES = [
        {
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            "DIRS": [BASE_DIR / "templates"],
            "APP_DIRS": True,
            "OPTIONS": {
                "context_processors": [
                    "django.template.context_processors.debug",
                    "django.template.context_processors.request",
                    "django.contrib.auth.context_processors.auth",
                    "django.contrib.messages.context_processors.messages",
                    "django.template.context_processors.i18n",
                ],
            },
        },
    ]
    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "verbose": {
                "format": "%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s",
            },
        },
        "handlers": {
            "console": {
                "level": "DEBUG",
                "class": "logging.StreamHandler",
                "formatter": "verbose",
            }
        },
        "root": {"level": "INFO", "handlers": ["console"]},
    }

    CACHES = {
        "default": {
            "BACKEND": "django_valkey.cache.ValkeyCache",
            "LOCATION": "valkey://127.0.0.1:6379?protocol=3",
            "OPTIONS": {
                "COMPRESSOR": "django_valkey.compressors.brotli.BrotliCompressor",
            },
        }
    }
    CACHE_MIDDLEWARE_ALIAS = "default"
    CACHE_MIDDLEWARE_SECONDS = 10
    CACHE_MIDDLEWARE_KEY_PREFIX = ""

    def MIDDLEWARE(self):
        return list(
            filter(
                None,
                [
                    "django.middleware.security.SecurityMiddleware",
                    (
                        "whitenoise.middleware.WhiteNoiseMiddleware"
                        if self.DEBUG
                        else None
                    ),
                    "django.contrib.sessions.middleware.SessionMiddleware",
                    "django.middleware.cache.UpdateCacheMiddleware",
                    "django.middleware.locale.LocaleMiddleware",
                    "django.middleware.common.CommonMiddleware",
                    "django.middleware.cache.FetchFromCacheMiddleware",
                    "django.middleware.csrf.CsrfViewMiddleware",
                    "django.contrib.auth.middleware.AuthenticationMiddleware",
                    "django.contrib.messages.middleware.MessageMiddleware",
                    "django.middleware.clickjacking.XFrameOptionsMiddleware",
                    (
                        "debug_toolbar.middleware.DebugToolbarMiddleware"
                        if self.DEBUG
                        else None
                    ),
                    (
                        "django_browser_reload.middleware.BrowserReloadMiddleware"
                        if self.DEBUG
                        else None
                    ),
                ],
            )
        )

    def DATABASES(self):
        return {
            "default": {
                "ENGINE": "django.db.backends.postgresql",
                "NAME": envi.str("POSTGRES_NAME", default="postgres"),
                "USER": envi.str("POSTGRES_USER", default="postgres"),
                "PASSWORD": envi.str("POSTGRES_PASSWORD", default="postgres"),
                "HOST": envi.str("POSTGRES_HOST", default="localhost"),
                "PORT": 5432,
                # "ATOMIC_REQUESTS": True,
            }
        }

    def INSTALLED_APPS(self):
        return list(
            filter(
                None,
                [
                    "django.contrib.admin",
                    "django.contrib.auth",
                    "django.contrib.contenttypes",
                    "django.contrib.sessions",
                    "django.contrib.messages",
                    "whitenoise.runserver_nostatic" if self.DEBUG else None,
                    "django.contrib.staticfiles",
                    "django.contrib.sites",
                    "django.contrib.sitemaps",
                    # debug toolbar
                    "debug_toolbar" if self.DEBUG else None,
                    # rest
                    "rest_framework",
                    # taggit
                    "taggit",
                    # tailwind
                    "django_tailwind_cli",
                    "django_browser_reload" if self.DEBUG else None,
                    # extensions
                    "django_extensions" if self.DEBUG else None,
                    # tiny
                    "tinymce",
                    # local
                    "posts",
                ],
            )
        )


class ProdSettings(Settings):
    DEBUG = envi.bool("DEBUG", False)
    ALLOWED_HOSTS = envi.list(
        "ALLOWED_HOSTS",
    )
    ADMIN_URL = envi.str("ADMIN_URL", default="admin/")
    STORAGES = {
        "default": {
            "BACKEND": "django.core.files.storage.FileSystemStorage",
        },
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
        },
    }

    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "filters": {
            "require_debug_false": {"()": "django.utils.log.RequireDebugFalse"}
        },
        "formatters": {
            "verbose": {
                "format": "%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s",
            },
        },
        "handlers": {
            "mail_admins": {
                "level": "ERROR",
                "filters": ["require_debug_false"],
                "class": "django.utils.log.AdminEmailHandler",
            },
            "console": {
                "level": "DEBUG",
                "class": "logging.StreamHandler",
                "formatter": "verbose",
            },
        },
        "root": {"level": "INFO", "handlers": ["console"]},
        "loggers": {
            "django.request": {
                "handlers": ["mail_admins"],
                "level": "ERROR",
                "propagate": True,
            },
            "django.security.DisallowedHost": {
                "level": "ERROR",
                "handlers": ["console", "mail_admins"],
                "propagate": True,
            },
        },
    }

    def DATABASES(self):
        database = super().DATABASES()
        database["default"]["CONN_MAX_AGE"] = envi.int(
            "django_conn_max_age", default=60
        )


class TestSettings(Settings):
    SECRET_KEY = "testsecret"
    PASSWORD_HASHERS = ("django.contrib.auth.hashers.MD5PasswordHasher",)

    def MIDDLEWARE(self):
        return [
            m
            for m in super().MIDDLEWARE()
            if m != "django.middleware.cache.UpdateCacheMiddleware"
            and m != "django.middleware.cache.FetchFromCacheMiddleware"
            and m != "debug_toolbar.middleware.DebugToolbarMiddleware"
        ]


__getattr__, __dir__ = Settings.use()
