from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
	path('', include('apps.confidencechronograms.urls')),
    path('grappelli/', include('grappelli.urls')), # grappelli URLS
    path('admin/', admin.site.urls), # admin site
    path('account/', include('apps.account.urls')),
    #path('account/', include('django.contrib.auth.urls')), #para urls app_name = 'account'
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
