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
from rest_framework.renderers import JSONRenderer
from json import loads,dumps
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponse
from rest_framework.decorators import api_view
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login
from django.http import *
from custompermissions import levelpermissions,credentials

def logout_view(request):
    logout(request)
    print "salio"
    return HttpResponseRedirect('/login/')
@api_view(['GET', 'POST'])
def login_view(request):
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            permissions = levelpermissions(user)
            print permissions
            if permissions['level']>1:
                return HttpResponseRedirect('/home/'+str(permissions['page']))
            elif permissions['level']==1:
                return HttpResponseRedirect('/home/encargados/'+str(permissions['page']))
            else:
                return render(request,'login.html',{'error':'usuario o contrasenha no valida'})
        else:
            return render(request,'login.html',{'error':'usuario o contrasenha no valida'})

    elif request.method == 'GET':
        empresas = modelo_empresa.objects.all()
        return render(request,'login.html')

@api_view(['GET'])
@login_required(login_url='/login/')
def base_de_datos(request,offset):
    permisos = credentials(request.user,offset)
    if(permisos['level']>1 and permisos['conexion']==True):
        if request.method == 'GET':
            r = modelo_cliente.objects.filter(status=True,empresa=permisos['empresa'])
            a = clienteSerializer(instance=r,many=True)
            json = loads(dumps(a.data))
            return render(request,'base_de_datos.html',{'clientes': a.data})
    return render(request,'base_de_datos.html',{'error': "disculpe, no tiene permisos suficientes para acceder a esta pantalla"})

@api_view(['GET', 'POST'])
@login_required(login_url='/login/')
def vista_consulta(request,offset):
   credenciales = credentials(request.user,offset)
   if credenciales['conexion'] and int(credenciales['level'])>1:
      print 'entre'
      if request.method == 'GET':
         r = modelo_cliente.objects.filter(status=False,empresa=credenciales['empresa'])
         a = clienteSerializer(instance=r,many=True)
      #print json[0]
         queryset2 = modelo_encargado.objects.all()
         return render(request,'ini.html',{'datos': a.data ,'encargados':queryset2,'valor':r.count(),'page':credenciales['page']})
      #return Response({'datos': a.data ,'encargados':queryset2,'valor':r.count()})
      #preguntar si user es autenticado
      if request.method == 'POST':
      #print request.data.get('id')
         id_local = request.data.get('id')
         try:
            if(request.data.get('comando')!='eliminar'):
               p = modelo_cliente.objects.get(cliente_id=id_local)
               p.status=True
               p.encargado = request.data.get('encargado')
               p.save()
            else:
               p = modelo_cliente.objects.get(cliente_id=id_local).delete()
            return Response(status=status.HTTP_201_CREATED)
         except:
            return Response(status=status.HTTP_404_NOT_FOUND)
   else:
      print "error"
      return render(request,'error.html')



@api_view(['GET'])
@login_required(login_url='/login/')
def vista_agregar_nuevo(request,offset):
   credenciales = credentials(request.user,offset)
   if credenciales['conexion'] and int(credenciales['level'])>1:
      if request.method == 'GET':
         encargados = modelo_encargado.objects.all()
         productos = modelo_producto.objects.all()
         return render(request,'agregar_nuevo.html',{'encargados':encargados,'productos':productos})
   else:
      return render(request,'error.html')


@api_view(['GET'])
@login_required(login_url='/login/')
def vista_encargados(request,offset):

   if request.method == 'GET':
      credential = credentials(request.user,offset)
      if credential['conexion']==True:
         r = modelo_cliente.objects.filter(status=True,empresa=credential['empresa']).order_by('-hora')
         a = clienteSerializer(instance=r,many=True)
         return render(request,'cliente.html',{'datos': a.data})
      else:
         return render(request,'error.html')

class api_otro(generics.ListCreateAPIView):
    queryset = modelo_cliente.objects.filter(status=False).order_by('encargado')
    serializer_class = clienteSerializer

class api_encargado(APIView):
    def get(self,request):
        encargado = modelo_encargado.objects.all()
        producto = modelo_producto.objects.all()
        a = productoSerializer(producto, many=True)
        b = encargadoSerializer(encargado, many=True)
        return JsonResponse({'productos':loads(dumps(a.data)),'encargados':loads(dumps(b.data))})
#responde a solicitud de android
class api_cliente(APIView):
    def post(self,request):
        a=clienteSerializer(data=request.data)
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


class api_cliente_2(generics.ListCreateAPIView):
    queryset = modelo_cliente.objects.all()
    serializer_class = clienteSerializer

class api_productos(generics.ListCreateAPIView):
    queryset = modelo_producto.objects.all()
    serializer_class = productoSerializer

class api_empresa(generics.ListCreateAPIView):
    queryset = modelo_empresa.objects.all()
    serializer_class = empresaSerializer

#levanta pagina web de consulta admin

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
