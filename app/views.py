# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework import permissions
from pygments.lexers import get_lexer_by_name
from pygments.formatters.html import HtmlFormatter
from pygments import highlight
from app.models import modelodespachopedido,modelocliente,modeloencargado
from app.serializers import modelopedidoSerializer,modeloclienteSerializer
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect

class ProfileList(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'index.html'

    def get(self, request):
        queryset = modelocliente.objects.all()
        queryset2 = modeloencargado.objects.all()
        print modelodespachopedido.objects.count()
        return Response({'profiles': queryset,'encargados':queryset2})

    def post(self,request):
        try:
            last_id= modelodespachopedido.objects.order_by('-id')[0]
            print last_id.id
            id_despacho = last_id.id
        except:
            id_despacho=0
        p = modelodespachopedido(pedido_id=modelodespachopedido.objects.count()+1,encargado=request.POST.get('encargado'),\
                                 pedido_cliente=request.POST.get('pedido'),\
                                 pedido_cliente_nombre=request.POST.get('nombre'))
        p.save()
        print request.POST.get('id')
        p = modelocliente.objects.get(cliente_id=request.POST.get('id'))
        p.cliente_status = True
        p.save()
        return redirect('/hola/')

class modeloclienteview(generics.ListCreateAPIView):
    queryset = modelocliente.objects.all()
    serializer_class = modeloclienteSerializer

class pedidocliente(generics.ListCreateAPIView):
    queryset = modelodespachopedido.objects.all()
    serializer_class = modelopedidoSerializer

class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = modelocliente.objects.all()
    serializer_class =  modeloclienteSerializer
