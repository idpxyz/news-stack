from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.views.generic import TemplateView
import portal.views
from wagtail import urls as wagtail_urls
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls

urlpatterns = [
    path("admin/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
    path("auth/", include("authapp.urls")),
    path("community/", include("community.urls")),
    path("", portal.views.home_view, name="home"),  # 添加首页视图
    path("api/home", portal.views.api_home, name="api-home"),
    path("api/portal", portal.views.api_portal, name="api-portal"),
    path("search/", portal.views.search_view, name="search"),
    path("fragments/more-items/", TemplateView.as_view(template_name="fragments/more_items.html"), name="more-items"),
    path("wagtail/", include(wagtail_urls)),  # 将Wagtail URL移到子路径
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
