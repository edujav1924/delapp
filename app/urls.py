from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from app import views
from django.conf.urls import include

urlpatterns = [
    url(r'^consulta/$', views.consulta.as_view()),
    url(r'^pedidos/$', views.modeloclienteview.as_view()),
    url(r'^encargados/$', views.modeloencargadoview.as_view()),
    url(r'^pedidos/(?P<pk>[0-9]+)/$', views.SnippetDetail.as_view()),
    url(r'^pedidosrecientes/$', views.ProfileList.as_view(),name='pedidosrecientes'),
    url(r'^pedidosaceptados/$', views.pedidosaceptados.as_view(),name='pedidosaceptados'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
