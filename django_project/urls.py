"""
URL configuration for django_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap, index
from django.urls import path, include

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from debug_toolbar.toolbar import debug_toolbar_urls

from posts.sitemaps import PostSiteMap


urlpatterns = i18n_patterns(
    path(settings.ADMIN_URL, admin.site.urls),
    path("blog/", include("posts.urls")),
    path("tinymce/", include("tinymce.urls")),
    path("doc/api/v1/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "doc/api/v1/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "doc/api/v1/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
    path("", include("pages.urls")),
)

urlpatterns += [
    path("blog/", include("posts.api_urls")),
    path(
        "auth/jwt/api/v1/token/",
        TokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
    path(
        "auth/jwt/api/v1/token/refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh",
    ),
    path(
        "auth/jwt/api/v1/token/verify/", TokenVerifyView.as_view(), name="token_verify"
    ),
]

sitemaps = {
    "posts": PostSiteMap,
}

urlpatterns += [
    path(
        "sitemap.xml",
        index,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.index",
    ),
    path(
        "sitemap-<section>.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
]

if settings.DEBUG:
    urlpatterns += (
        [
            path("__reload__/", include("django_browser_reload.urls")),
        ]
        + debug_toolbar_urls()
        + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    )
