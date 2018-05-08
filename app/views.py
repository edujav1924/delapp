# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from app.models import *
from app.serializers import *
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404, redirect,render
from rest_framework import status, generics
from rest_framework.renderers import JSONRenderer
from json import loads,dumps
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from rest_framework.decorators import api_view
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login,logout
from django.http import *
from custompermissions import levelpermissions,credentials
from fcm_django.models import FCMDevice
from django.contrib.auth.models import User
import threading
from django.contrib.auth import models
import datetime
from milog import write

def manifest(request):
   return JsonResponse({"gcm_sender_id": "103953800507"})

def firebase_messaging_sw_js(request):
    filename = '/static/firebase-messaging-sw.js'
    jsfile = open('/home/edu/scripts/paginaweb/apirest/app/static/firebase-messaging-sw.js', 'rb')
    response = HttpResponse(content=jsfile)
    response['Content-Type'] = 'text/javascript'
    response['Content-Disposition'] = 'attachment; filename="%s"'%('/home/edu/scripts/paginaweb/apirest/app/static/firebase-messaging-sw.js')
    return response

@api_view(['GET', 'POST'])
@login_required(login_url='/login/')
def misproductoses(request,offset):
   encargado = ""
   supervisor = ""
   permisos = credentials(request.user,offset)
   if request.method == 'GET':
      if(permisos['level']>1) and permisos['conexion']==True:
         empresa = modelo_empresa.objects.get(id=offset)
         namegroup = models.Group.objects.filter(name__startswith=empresa.empresa)
         for i in range(0,namegroup.count()):
            group = models.Group.objects.get(name=namegroup[i])
            users = group.user_set.all()
            a = group.name.find('_')
            cargo = group.name[a+1:]
            if(cargo=='supervisor'):
               supervisor = users

            if(cargo=='encargado'):
               encargado = users

         productos = modelo_producto.objects.filter(empresa_id=int(offset))
         return render(request,'misproductos.html',{'productos':productos,'supervisores':supervisor,'encargados':encargado,'page':permisos['page']})
      return render(request,"error.html")

   elif request.method == 'POST':
      if(permisos['level']>1) and permisos['conexion']==True:
         if(request.data.get('method') == 'edit'):
            extraer_producto = modelo_producto.objects.get(id=request.data.get('id'))
            extraer_producto.producto = request.data.get('producto')
            extraer_producto.precio = request.data.get('precio')
            extraer_producto.save()
            return Response(status=status.HTTP_202_ACCEPTED)
         elif (request.data.get('method') == 'new'):
            modelo_producto.objects.create(empresa_id=int(offset),producto=request.data.get('producto'),precio=request.data.get('precio'))
            return Response(status=status.HTTP_201_CREATED)

         elif (request.data.get('method') == 'delete'):
            elemento = modelo_producto.objects.get(id=request.data.get('id'))
            elemento.delete()
            return Response(status=status.HTTP_201_CREATED)
         return Response(status=status.HTTP_400_BAD_REQUEST)
      print("no autorizado")
      return Response(status=status.HTTP_401_UNAUTHORIZED)

def logout_view(request):
    logout(request)
    print "salio"
    return HttpResponseRedirect('/login/')

@login_required(login_url='/login/')
def admin_site(request):
   if request.user.is_superuser:
      if request.method=='GET':
         empresas = modelo_empresa.objects.all()
         data = modelo_cliente.objects.filter(status=True)
         return render(request,'admin.html',{'clientes':data,'empresas':empresas})
      if request.method=='POST':
         empresas = modelo_empresa.objects.all()
         empresa = request.POST['empresa']
         desde = request.POST['desde'].replace("/","-")
         hasta = request.POST['hasta'].replace("/","-")
         print empresa +"--"+desde+"--"+hasta
         clientes = modelo_cliente.objects.filter(empresa=empresa,fecha__range=[desde,hasta])
         print clientes
         return render(request,'admin.html',{'clientes':clientes,'empresas':empresas})
   return render(request,'error.html')

@api_view(['GET', 'POST'])
def login_view(request):
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            permissions = levelpermissions(user)
            if user.is_superuser:
               return HttpResponseRedirect('/admin_site/')

            elif permissions['level']>1:
                return HttpResponseRedirect('/home/'+str(permissions['page']))
            elif permissions['level']==1:
                return HttpResponseRedirect('/home/encargados/'+str(permissions['page']))
            else:
                return render(request,'login.html',{'error':'usuario o contrasenha no valida'})
        else:
            return render(request,'login.html',{'error':'usuario o contrasenha no valida'})

    elif request.method == 'GET':
      if(request.user.is_anonymous):
         empresas = modelo_empresa.objects.all()
         return render(request,'login.html')
      else:
         permissions = levelpermissions(request.user)
         if permissions['level']>1:
             return HttpResponseRedirect('/home/'+str(permissions['page']))
         elif permissions['level']==1:
             return HttpResponseRedirect('/home/encargados/'+str(permissions['page']))


@api_view(['GET'])
@login_required(login_url='/login/')
def base_de_datos(request,offset):
    permisos = credentials(request.user,offset)
    if(permisos['level']>1 and permisos['conexion']==True):
        if request.method == 'GET':
            r = modelo_cliente.objects.filter(status=True,empresa=permisos['empresa'])
            a = clienteSerializer(instance=r,many=True)
            json = loads(dumps(a.data))
            return render(request,'base_de_datos.html',{'clientes': a.data,'page':permisos['page']})
    return render(request,'base_de_datos.html',{'error': "disculpe, no tiene permisos suficientes para acceder a esta pantalla"})

def respconsumer(device):
   device.send_message(title='Delivery On',icon='/static/logito2.png', body='Pedido aceptado')
@api_view(['GET', 'POST'])

@login_required(login_url='/login/')
def vista_consulta(request,offset):
   credenciales = credentials(request.user,offset)
   if credenciales['conexion'] and int(credenciales['level'])>1:
      if request.method == 'GET':
         r = modelo_cliente.objects.filter(status=False,empresa=credenciales['empresa'])
         a = clienteSerializer(instance=r,many=True)
      #print json[0]
         queryset2 = modelo_encargado.objects.filter(empresa_id=credenciales['page'])
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
               a = FCMDevice.objects.filter(registration_id=p.token)

               if(a.count()==0):
                  device = FCMDevice.objects.create(name=p.nombre,active=True,registration_id=p.token,type='android')
                  print device
               elif( a.count()==1):
                  device = FCMDevice.objects.get(registration_id=p.token)
                  print device
               else:
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


@api_view(['GET', 'POST'])
@login_required(login_url='/login/')
def vista_encargados(request,offset):

   credential = credentials(request.user,offset)
   if credential['conexion']==True:
      if request.method == 'GET':
         a =  datetime.date.today()

         return render(request,'encargados_table.html',{'datos':modelo_cliente.objects.filter(fecha__range=[a,a],status=True),'page':credential['page']})
      if request.method == 'POST':
         desde = request.POST['fecha_desde']
         hasta = request.POST['fecha_hasta']
         if desde=="" or hasta=="":
            print "vacio"
            return render(request,'encargados_table.html',{'error':"ingrese fechas validas"})
         clientes = modelo_cliente.objects.filter(fecha__range=[desde, hasta],status=True)
         return render(request,'encargados_table.html',{'datos':clientes,'page':credential['page']})

   return render(request,'error.html')
class api_otro(generics.ListCreateAPIView):
    queryset = modelo_cliente.objects.filter(status=False).order_by('encargado')
    serializer_class = clienteSerializer



def log(texto):
   hilo = threading.Thread(target=write,args=(texto,))
   hilo.start()

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
         log('actualizar')
         print 'actualizar'
         a = FCMDevice.objects.get(name=request.user,user_id=request.data.get('user_id'))
         a.registration_id = request.data.get('token')
         a.save()

      return JsonResponse({'exitoso':'exitoso'})

#responde a solicitud de android

def enviar(device):
   device.send_message(title='Delivery On',icon='/static/logito2.png', body='Nuevo Pedido')

class api_cliente(APIView):
   def post(self,request):
      a=clienteSerializer(data=request.data)
      a.is_valid()
      if(a.is_valid()):
         a.save()
         if request.is_ajax()==False:
             try:
                device = FCMDevice.objects.filter(user_id=request.data.get('empresa_id'))
                hilo = threading.Thread(target=enviar,args=(device,))
                hilo.start()
                return JsonResponse({'status':'exitoso'})
             except:
                print "error fcm api_cliente"

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
