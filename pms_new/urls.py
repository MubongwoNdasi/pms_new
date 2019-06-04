from django.contrib import admin
from django.urls import path, include

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings

from core import views


urlpatterns = [
    # path('', views.IndexView.as_view(), name='home'),
    path('home/', views.IndexView.as_view(), name='home'),

    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),

    # app_urls
    path('core/', include('core.urls')),
    path('drug/', include('drug.urls')),
    path('search/', include('search.urls')),
    path('cart/', include('cart.urls')),
]


if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


