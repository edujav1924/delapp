from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import url, include
from app import views
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('app.urls')),
    url(r'^api-auth/', include('rest_framework.urls')),
]
