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
from fcm_django.models import FCMDevice
from django.contrib.auth.models import User
import threading
def manifest(request):
   return JsonResponse({"gcm_sender_id": "103953800507"})

def firebase_messaging_sw_js(request):
    filename = '/static/firebase-messaging-sw.js'
    jsfile = open('/home/edu/scripts/paginaweb/apirest/app/static/firebase-messaging-sw.js', 'rb')
    response = HttpResponse(content=jsfile)
    response['Content-Type'] = 'text/javascript'
    response['Content-Disposition'] = 'attachment; filename="%s"'%('/home/edu/scripts/paginaweb/apirest/app/static/firebase-messaging-sw.js')
    return response

def vistaini(request):
    if request.GET:
        return render(request,'')

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
            return render(request,'base_de_datos.html',{'clientes': a.data,'ip':"https://192.168.43.158:8000"})
    return render(request,'base_de_datos.html',{'error': "disculpe, no tiene permisos suficientes para acceder a esta pantalla"})

def respconsumer(device):
   print device
   device.send_message(title='title', body='message')
@api_view(['GET', 'POST'])

@login_required(login_url='/login/')
def vista_consulta(request,offset):
   credenciales = credentials(request.user,offset)
   if credenciales['conexion'] and int(credenciales['level'])>1:
      print 'entre'
      print credenciales['empresa']
      if request.method == 'GET':
         r = modelo_cliente.objects.filter(status=False,empresa=credenciales['empresa'])
         print r
         a = clienteSerializer(instance=r,many=True)
      #print json[0]
         queryset2 = modelo_encargado.objects.filter(empresa_id=credenciales['page'])
         return render(request,'ini.html',{'datos': a.data ,'encargados':queryset2,'valor':r.count(),'page':credenciales['page'],'ip':"https://192.168.43.158:8000"})
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
               a = FCMDevice.objects.filter(registration_id=p.token)

               if(a.count()==0):
                  device = FCMDevice.objects.create(name=p.nombre,active=True,registration_id=p.token,type='android')
                  print "1"
                  print device
               elif( a.count()==1):
                  device = FCMDevice.objects.get(registration_id=p.token)
                  print "2"
                  print device
               else:
                  print "3"
                  print device
                  device = a.last()

               hilo2 = threading.Thread(target=respconsumer,args=(device,))
               hilo2.start()



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
         productos = modelo_producto.objects.filter(empresa_id=credenciales['page'])
         return render(request,'agregar_nuevo.html',{'encargados':encargados,'productos':productos,'empresa':credenciales['empresa'],'page':credenciales['page']})
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
    def get(self,request,pk):
      encargado = modelo_encargado.objects.filter(empresa_id=pk)
      producto = modelo_producto.objects.filter(empresa_id=pk)
      a = productoSerializer(producto, many=True)
      b = encargadoSerializer(encargado, many=True)
      return JsonResponse({'productos':loads(dumps(a.data)),'encargados':loads(dumps(b.data))})

class api_token(APIView):
   def post(self,request):
      a = FCMDevice.objects.filter(name=request.user)
      if(a.count()==0):
         FCMDevice.objects.create(name=request.user,active=True,user_id=request.data.get('user_id'),registration_id=request.data.get('token'),type=request.data.get('type'))
         print "guardar"
      else:
         print 'actualizar'
         a = FCMDevice.objects.get(name=request.user)
         a.registration_id = request.data.get('token')
         a.save()

      return JsonResponse({'exitoso':'exitoso'})
   def get(self,request):
      us = User.objects.get(username='lucio')
      return render(request,'error.html')
#responde a solicitud de android

def enviar(device):

   device.send_message(title='DeliveryOn',body='Nuevo Pedido')

class api_cliente(APIView):


   def post(self,request):
      a=clienteSerializer(data=request.data)
      if(a.is_valid()):
         a.save()
         try:
            device = FCMDevice.objects.filter(user_id=request.data.get('empresa_id'))
            hilo = threading.Thread(target=enviar,args=device)
            hilo.start()
         except:
            print "error fcm api_cliente"
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
