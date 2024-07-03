from django.contrib import admin
from django.urls import path, include
from captcha.views import captcha_refresh

urlpatterns = [
    path('admin/', admin.site.urls),
    path('captcha/', include('captcha.urls')),
    path('', include("chat.urls")),
    path('captcha/refresh/', captcha_refresh, name='captcha-refresh'),
]
