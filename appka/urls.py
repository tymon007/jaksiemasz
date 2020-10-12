from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main_page.urls'))
]

urlpatterns += [
    path('', include('django.contrib.auth.urls')),
]
