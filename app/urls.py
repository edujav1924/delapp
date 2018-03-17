from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from app import views
from django.conf.urls import include

urlpatterns = [
    url(r'^pedidos/$', views.modeloclienteview.as_view()),
    url(r'^pedidos/(?P<pk>[0-9]+)/$', views.SnippetDetail.as_view()),
    url(r'^hola/$', views.ProfileList.as_view(),name='yo'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
