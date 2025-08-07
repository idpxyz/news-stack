import os
from pathlib import Path
from dotenv import load_dotenv
from urllib.parse import urlparse
load_dotenv()
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "dev-secret-key")
DEBUG = os.getenv("DJANGO_DEBUG", "1") == "1"
ALLOWED_HOSTS = [
    "localhost","127.0.0.1",
    "media1.local",
    "media2.local",
    "portal.local"
    ]
INSTALLED_APPS = [
    "django.contrib.admin","django.contrib.auth","django.contrib.contenttypes",
    "django.contrib.sessions","django.contrib.messages","django.contrib.staticfiles",
    "wagtail.contrib.forms","wagtail.contrib.redirects","wagtail.embeds","wagtail.sites",
    "wagtail.users","wagtail.snippets","wagtail.documents","wagtail.images",
    "wagtail.search","wagtail.admin","wagtail","modelcluster","taggit",
    "wagtail.contrib.settings",
    "core","news","authapp","portal",
]
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "wagtail.contrib.redirects.middleware.RedirectMiddleware",
]
ROOT_URLCONF = "news_platform.urls"
TEMPLATES = [{
    "BACKEND":"django.template.backends.django.DjangoTemplates",
    "DIRS":[BASE_DIR/"templates"],"APP_DIRS":True,
    "OPTIONS":{"context_processors":[
        "django.template.context_processors.debug","django.template.context_processors.request",
        "django.contrib.auth.context_processors.auth","django.contrib.messages.context_processors.messages",
    ]},
}]
WSGI_APPLICATION = "news_platform.wsgi.application"
DATABASES = {"default":{"ENGINE":"django.db.backends.sqlite3","NAME":BASE_DIR/"db.sqlite3"}}
db_url=os.getenv("DATABASE_URL")
if db_url:
    o=urlparse(db_url)
    if o.scheme.startswith("postgres"):
        DATABASES["default"]={"ENGINE":"django.db.backends.postgresql","NAME":o.path.lstrip("/"),
                               "USER":o.username,"PASSWORD":o.password,"HOST":o.hostname,"PORT":o.port or 5432}
STATIC_URL="/static/"
STATICFILES_DIRS=[BASE_DIR/"static"]
MEDIA_URL="/media/"
MEDIA_ROOT=BASE_DIR/"media"
WAGTAIL_SITE_NAME="News Platform"
WAGTAILADMIN_BASE_URL="http://localhost:9000"
REDIS_URL=os.getenv("REDIS_URL")
if REDIS_URL:
    CACHES={"default":{"BACKEND":"django_redis.cache.RedisCache","LOCATION":REDIS_URL,
                       "OPTIONS":{"CLIENT_CLASS":"django_redis.client.DefaultClient"}}}
else:
    CACHES={"default":{"BACKEND":"django.core.cache.backends.locmem.LocMemCache"}}
DEFAULT_AUTO_FIELD="django.db.models.BigAutoField"
OS_ENABLED=os.getenv("OS_ENABLED","0")=="1"
OS_URL=os.getenv("OS_URL","http://127.0.0.1:9200")
OS_INDEX=os.getenv("OS_INDEX","news_articles")
