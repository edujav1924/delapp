# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from rest_framework import generics
#from django.contrib.auth.models import Use
#from rest_framework import permissions
from app.models import *
from app.serializers import *
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.http import Http404
from rest_framework import status
import json

class productos(generics.ListCreateAPIView):
    queryset = modelo_producto.objects.all()
    serializer_class = productoSerializer

class consulta(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'otraprueba.html'
    def get(self, request):
        queryset = modelo_prueba.objects.all()
        queryset2 = modelo_encargado.objects.all()
        return Response({'datos': queryset,'encargados':queryset2})

    def post (self,request):
        print request.data.get('id')
        id_local = request.data.get('id')
        print request.data.get('comando')
        if(request.data.get('comando')!='eliminar'):
            query = modelo_prueba.objects.get(id=id_local)
            modelo_prueba_final.objects.create(nombre=query.nombre,apellido=query.apellido,celular=query.celular,producto=query.producto\
                                          ,cantidad=query.cantidad,encargado=request.data.get('encargado'))
        else:
            print "entre"
            query = modelo_prueba.objects.get(id=id_local).delete()
        return Response(status=status.HTTP_201_CREATED)


"""
class consulta(APIView):
    def get(self, request):
        return render(request,'prueba.html')

class pedidosaceptados(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'confirmados.html'
    def get(self,request):
        pedidosconfirmados = modelodespachopedido.objects.all()
        return Response({'pedidosconfirmados':pedidosconfirmados})
class modeloclienteview(generics.ListCreateAPIView):
    queryset = modelocliente.objects.filter(cliente_status=False)
    serializer_class = modeloclienteSerializer
class modeloencargadoview(generics.ListCreateAPIView):
    queryset = modeloencargado.objects.all()
    serializer_class = modeloencargadoSerializer
class pedidocliente(APIView):
    def get(self, request, format=None):
        queryset = modelodespachopedido.objects.all()
        serializer_class = modelopedidoSerializer

    def post(self,request,format=None):
        serializer = modelopedidoSerializer(data=request.data)
        print request.data
        if serializer.is_valid():
            serializer.save()
            try:
                p = modelocliente.objects.get(cliente_id=request.data.get('pedido_id'))
                p.cliente_status = True
                p.save()
            except:
                print "error"
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print 'error'
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = modelocliente.objects.all()
    serializer_class =  modeloclienteSerializer

class clienteview(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'cliente.html'
"""
