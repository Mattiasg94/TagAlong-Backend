
from django.contrib import admin
from django.views.i18n import JavaScriptCatalog
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path(r'admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('', include('website.urls')),
    path('api/', include(('accounts.auth.routers', 'tagalong'), namespace='tagalong-api')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
