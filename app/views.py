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
from app.serializers import modelopedidoSerializer,modeloclienteSerializer,modeloencargadoSerializer
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
class consulta(APIView):
    def get(self, request):
        return render(request,'prueba.html')

class ProfileList(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'ini.html'

    def get(self, request):
        queryset = modelocliente.objects.filter(cliente_status=False)
        queryset2 = modeloencargado.objects.all()
        return Response({'profiles': queryset,'encargados':queryset2})

    def post(self,request):
        try:
            last_id= modelodespachopedido.objects.order_by('-id')[0]
            id_despacho = last_id.id
        except:
            id_despacho=0
        p = modelodespachopedido(pedido_id=modelodespachopedido.objects.count()+1,encargado=request.POST.get('encargado'),\
                                 pedido_cliente=request.POST.get('pedido'),\
                                 pedido_cliente_nombre=request.POST.get('nombre'))
        p.save()
        p = modelocliente.objects.get(cliente_id=request.POST.get('id'))
        p.cliente_status = True
        p.save()
        return redirect('/pedidosrecientes/')

class pedidosaceptados(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'confirmados.html'
    def get(self,request):
        pedidosconfirmados = modelodespachopedido.objects.all()
        print pedidosconfirmados
        return Response({'pedidosconfirmados':pedidosconfirmados})


class modeloclienteview(generics.ListCreateAPIView):
    queryset = modelocliente.objects.all()
    serializer_class = modeloclienteSerializer

class modeloencargadoview(generics.ListCreateAPIView):
    queryset = modeloencargado.objects.all()
    serializer_class = modeloencargadoSerializer

class pedidocliente(generics.ListCreateAPIView):
    queryset = modelodespachopedido.objects.all()
    serializer_class = modelopedidoSerializer

class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = modelocliente.objects.all()
    serializer_class =  modeloclienteSerializer
