from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path, include, re_path


urlpatterns = [
    # re_path(r'^jet/', include(('jet.urls', 'jet'))),  # Django JET URLS
    # re_path(r'^jet/dashboard/', include(('jet.dashboard.urls'), namespace="jet-dashboard")),   # Django JET dashboard URLS
    # re_path(r'^admin/', admin.site.urls),

    path('', include('core.urls'), name='home'),
    path('company/', include('company.urls'), name='company'),
    path('accounts/', include('accounts.urls'), name='accounts'),
]

# LOAD STATICS / MIDIAS
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)