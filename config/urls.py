from django.contrib import admin
from django.urls import path, include
from captcha.views import captcha_refresh
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('captcha/', include('captcha.urls')),
    path('', include("chat.urls")),
    path('captcha/refresh/', captcha_refresh, name='captcha-refresh'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
