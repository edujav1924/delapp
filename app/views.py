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
from rest_framework.renderers import JSONRenderer
from json import loads,dumps
from django.http import JsonResponse
class encargado(APIView):
    def get(self,request):
        encargado = modelo_encargado.objects.all()
        producto = modelo_producto.objects.all()
        a = productoSerializer(producto, many=True)
        b = encargadoSerializer(encargado, many=True)
        return JsonResponse({'productos':loads(dumps(a.data)),'encargados':loads(dumps(b.data))})

class agregar_nuevo(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'agregar_nuevo.html'
    def get (self,request):
        encargados = modelo_encargado.objects.all()
        productos = modelo_producto.objects.all()
        return Response({'encargados':encargados,'productos':productos})


class vista_encargados(generics.ListCreateAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'cliente.html'
    def get(self,request):
        r = modelo_cliente.objects.filter(status=True).order_by('encargado')

        a = clienteSerializer(instance=r,many=True)
        json = loads(dumps(a.data))
        return Response({'datos': a.data})

class otro(generics.ListCreateAPIView):
    queryset = modelo_cliente.objects.filter(status=False).order_by('encargado')
    serializer_class = clienteSerializer

#responde a solicitud de android
class cliente(APIView):
    def post(self,request):
        a=clienteSerializer(data=request.data)
        print request.data
        if(a.is_valid()):
            a.save()
            return JsonResponse({'status':'exitoso'})
        return JsonResponse({'status':'error'})
    def get(self,request):
        r = modelo_cliente.objects.filter(status=False)

        a = clienteSerializer(instance=r,many=True)
        json = loads(dumps(a.data))
        #print json[0]
        return Response(json)


class productos(generics.ListCreateAPIView):
    queryset = modelo_producto.objects.all()
    serializer_class = productoSerializer

#levanta pagina web de consulta admin
class consulta(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'ini.html'
    def get(self, request):
        r = modelo_cliente.objects.filter(status=False)
        a = clienteSerializer(instance=r,many=True)
        json = loads(dumps(a.data))
        #print json[0]
        queryset2 = modelo_encargado.objects.all()
        return Response({'datos': a.data ,'encargados':queryset2,'valor':r.count()})

    def post (self,request):
        #print request.data.get('id')
        id_local = request.data.get('id')
        print request.data.get('comando')
        try:
            if(request.data.get('comando')!='eliminar'):
                print id_local
                p = modelo_cliente.objects.get(cliente_id=id_local)
                print p
                p.status=True
                p.encargado = request.data.get('encargado')
                p.save()
            else:
                print "entre"
                p = modelo_cliente.objects.get(cliente_id=id_local).delete()
            return Response(status=status.HTTP_201_CREATED)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)


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
