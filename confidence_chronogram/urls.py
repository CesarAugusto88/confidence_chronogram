from django.contrib import admin
from django.urls import path, include

urlpatterns = [
	path('', include('confidence_chronograms.urls')),
    path('admin/', admin.site.urls),
    path('account/', include('account.urls')),
    path('account/', include('django.contrib.auth.urls')),
]

