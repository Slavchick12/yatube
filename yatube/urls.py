from django.conf import settings
from django.conf.urls import handler404, handler500
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from posts import views


handler404 = 'posts.views.page_not_found'   # noqa
handler500 = 'posts.views.server_error'   # noqa

urlpatterns = [
    path('404/', views.server_error),
    path('500/', views.page_not_found),
    path('auth/', include('users.urls')),
    path('auth/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
    path('about/', include('about.urls', namespace='about')),
    path('', include('posts.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    from rest_framework.authtoken import views
    urlpatterns += path('__debug__/', include(debug_toolbar.urls)),
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
    )
    urlpatterns += path('api-token-auth/', views.obtain_auth_token),
