from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

import flux.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', flux.views.home, name='home'),
    path('authentication/', include('authentication.urls')),
    path('accounts/', include('accounts.urls')),
    path('flux/', include('flux.urls')),
    path('post/', include('post.urls')),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
