from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from app import views
from app.views import base_de_datos
from django.conf.urls import include

urlpatterns = [
    url(r'^home/login/$', views.vista_encargados.as_view()),
    url(r'^home/encargados/$', views.vista_encargados.as_view()),
    url(r'^home/$', views.vista_consulta.as_view()),
    url(r'^home/nuevo/$', views.vista_agregar_nuevo.as_view()),
    url(r'^home/datos/$', views.base_de_datos.as_view()),

    url(r'^cliente/$', views.api_cliente.as_view(), name="hola"),
    url(r'^otro/$', views.api_otro.as_view()),
    url(r'^cliente_2/$', views.api_cliente_2.as_view()),
    url(r'^productos/$', views.api_productos.as_view()),
    url(r'^en/$', views.api_encargado.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
"""url(r'^consulta/$', views.consulta.as_view()),
url(r'^pedidosweb/$', views.pedidocliente.as_view()),
url(r'^pedidos/$', views.modeloclienteview.as_view()),
url(r'^encargados/$', views.modeloencargadoview.as_view()),
url(r'^pedidos/(?P<pk>[0-9]+)/$', views.SnippetDetail.as_view()),
url(r'^pedidosrecientes/$', views.ProfileList.as_view(),name='pedidosrecientes'),
url(r'^pedidosaceptados/$', views.pedidosaceptados.as_view(),name='pedidosaceptados'),"""
