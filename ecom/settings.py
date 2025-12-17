from pathlib import Path
import os
from dotenv import load_dotenv


load_dotenv(".env")
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-mf$hu5t$ba*qca2c24@kyd*_oqr5+2^5nyp*+p%l(9l_l_0=!m"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    "ya-e-commerce-production.up.railway.app",
    "https://ya-e-commerce-production.up.railway.app",
    "127.0.0.1",
    "localhost",
]
CSRF_TRUSTED_ORIGINS = ["https://ya-e-commerce-production.up.railway.app"]

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    "whitenoise.runserver_nostatic",
    # allauth configrations
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.facebook",
    "allauth.socialaccount.providers.google",
    # other packages
    "django_filters",
    "django_countries",
    "cloudinary",
    "cloudinary_storage",
    "crispy_bootstrap4",
    "crispy_forms",
    # django project apps
    "store",
    "members",
    "cart",
    "payment",
    # paypal app
    "paypal.standard.ipn",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "store.middleware.AdminOnlyMiddleware",
    "payment.middleware.AdminOnlyMiddleware",
    "allauth.account.middleware.AccountMiddleware",
    "ecom.middleware.VisitorsTrackingMiddleware",
]

ROOT_URLCONF = "ecom.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                # "cart.context_processors.cart",
                "django.template.context_processors.request",
            ],
        },
    },
]

WSGI_APPLICATION = "ecom.wsgi.application"

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases
DATABASES = {
    # "default": {
    #     "ENGINE": "django.db.backends.postgresql",
    #     "NAME": "railway",
    #     "USER": "postgres",
    #     "PASSWORD": os.environ["DB_Password"],
    #     "HOST": "autorack.proxy.rlwy.net",
    #     "PORT": "27807",
    # }
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]


ACCOUNT_FORMS = {"signup": "members.forms.SignUpForms"}

ACCOUNT_ADAPTER = "members.adapters.AccountAdapter"
SOCIALACCOUNT_ADAPTER = "members.adapters.SocialAccountAdapter"

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

SITE_ID = 1
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap4"

CRISPY_TEMPLATE_PACK = "bootstrap4"


SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "APP": {
            "client_id": os.getenv("OAUTH_GOOGLE_CLIENT_ID"),
            "secret": os.getenv("OAUTH_GOOGLE_SECRET"),
            "key": "",
        },
        "SCOPE": ["profile", "email"],
        "AUTH_PARAMS": {
            "access_type": "offline",
            "prompt": "consent",
        },
        "OAUTH_PKCE_ENABLED": False,
    },
    "facebook": {
        "APP": {
            "client_id": os.getenv("OAUTH_FACEBOOK_CLIENT_ID"),
            "secret": os.getenv("OAUTH_FACEBOOK_SECRET"),
        },
        "AUTH_PARAMS": {
            "auth_type": "reauthenticate",
        },
    },
}


STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

AUTH_USER_MODEL = "members.User"

CLOUDINARY_STORAGE = {
    "CLOUD_NAME": os.getenv("CLOUDINARY_CLOUD_NAME"),
    "API_KEY": os.getenv("CLOUDINARY_API_KEY"),
    "API_SECRET": os.getenv("CLOUDINARY_API_SECRET"),
}


# ----social Login-----
SOCIALACCOUNT_LOGIN_ON_GET = True
SOCIALACCOUNT_AUTO_SIGNUP = True
# ----end social Login-----

ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_LOGIN_METHODS = ["email"]
ACCOUNT_SIGNUP_FIELDS = ["email", "password1", "password2"]

ACCOUNT_EMAIL_VERIFICATION = "none"

# ------Redirects-----
LOGOUT_REDIRECT_URL = "/"
# ACCOUNT_SIGNUP_REDIRECT_URL = "/"
LOGIN_REDIRECT_URL = "/"
# ------- end Redirects-------

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_HOST_USER = "ammenyoussef@gmail.com"
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_PORT = 587
EMAIL_USE_TLS = True


# whitenoise static files settings
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"


# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# paypal settings

PAYPAL_TEST = True

PAYPAL_RECEIVER_EMAIL = "yousefbusiness@gmail.com"  # Business Sandbox account
