from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from app import views
from app.views import *
from django.conf.urls import include

urlpatterns = [
    url(r'^logout/$',logout_view,name='logout'),
    url(r'^admin_site/$',admin_site),
    url(r'^home/encargados/(\d{1,2})$', vista_encargados),
    url(r'^home/(\d{1,2})$', vista_consulta),
    url(r'^home/nuevo/(\d{1,2})$',vista_agregar_nuevo),
    url(r'^home/datos/(\d{1,2})$', base_de_datos),
    url(r'^home/misproductos/(\d{1,2})$', misproductoses),
    url(r'^firebase-messaging-sw.js', views.firebase_messaging_sw_js),
    url(r'^manifest.json', views.manifest),
    url(r'^login/$',login_view,name='login'),
    url(r'^cliente/$', views.api_cliente.as_view(), name="hola"),
    url(r'^otro/$', views.api_otro.as_view()),
    url(r'^cliente_2/$', views.api_cliente_2.as_view()),
    url(r'^productos/$', views.api_productos.as_view()),
    url(r'^empresa/$', views.api_empresa.as_view()),
    url(r'^en/(?P<pk>[0-9]+)/$', views.api_encargado.as_view()),
    url(r'^token/$', views.api_token.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
