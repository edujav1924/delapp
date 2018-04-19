from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from app import views
from app.views import vista_consulta,logout_view,login_view
from app.views import base_de_datos,vista_agregar_nuevo,vista_encargados
from django.conf.urls import include

urlpatterns = [
    url(r'^logout/$',logout_view,name='logout'),
    url(r'^home/encargados/$', vista_encargados),
    url(r'^home/$', vista_consulta),
    url(r'^home/nuevo/$',vista_agregar_nuevo),
    url(r'^home/datos/$', base_de_datos),
    url(r'^login/$',login_view,name='login'),
    url(r'^cliente/$', views.api_cliente.as_view(), name="hola"),
    url(r'^otro/$', views.api_otro.as_view()),
    url(r'^cliente_2/$', views.api_cliente_2.as_view()),
    url(r'^productos/$', views.api_productos.as_view()),
    url(r'^empresa/$', views.api_empresa.as_view()),
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
