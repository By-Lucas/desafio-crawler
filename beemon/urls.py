from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path, include, re_path


urlpatterns = [
    re_path(r'^jet/', include(('jet.urls', 'jet'))),
    re_path(r'^jet/dashboard/', include(('jet.dashboard.urls'), namespace="jet-dashboard")),
    re_path(r'^admin/', admin.site.urls),

    path('', include('core.urls'), name='home'),
    path('', include('data_scrapy.urls'), name='data_scrapy'),
]

# LOAD STATICS / MIDIAS
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)