from django.conf.urls import url,include
from django.contrib import admin
from app import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),
    url(r'^admin/', admin.site.urls),
    url(r'^', include('app.urls')),
    url(r'^api-auth/', include('rest_framework.urls')),
]
