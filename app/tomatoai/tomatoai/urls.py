from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('restaurant_manager/', include('restaurant_manager.urls'))
]
