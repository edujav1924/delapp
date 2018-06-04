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
from datetime import datetime,date
from milog import write
import os
import sys
from django.core.mail import send_mail

def manifest(request):
   return JsonResponse({"gcm_sender_id": "113198272779"})

def firebase_messaging_sw_js(request):
    filename = '/static/firebase-messaging-sw.js'
    jsfile = open(os.getcwd()+'/static/firebase-messaging-sw.js', 'rb')
    response = HttpResponse(content=jsfile)
    response['Content-Type'] = 'text/javascript'
    response['Content-Disposition'] = 'attachment; filename="%s"'%(os.getcwd()+'/static/firebase-messaging-sw.js')
    log(os.getcwd()+'/static/firebase-messaging-sw.js')
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
         supervisor = modelo_encargado.objects.filter(empresa_id=offset,puesto='Sp')
         encargado = modelo_encargado.objects.filter(empresa_id=offset,puesto='En')
         productos = modelo_producto.objects.filter(empresa_id=int(offset))
         return render(request,'misproductos.html',{'productos':productos,'supervisores':supervisor,'encargados':encargado,'page':permisos['page'],'empresa':permisos['empresa']})
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
    return HttpResponseRedirect('/login/')

@login_required(login_url='/login/')
def admin_site(request):
   if request.user.is_superuser:
      if request.method=='GET':
         empresas = modelo_empresa.objects.all()
         data = modelo_cliente.objects.filter(status=1).order_by('-cliente_id')
         contador = modelo_contador.objects.all()
         return render(request,'admin.html',{'clientes':data,'empresas':empresas,'contador':contador})
      if request.method=='POST':
         empresas = modelo_empresa.objects.all()
         empresa = request.POST['empresa']
         desde = request.POST['desde'].replace("/","-")
         hasta = request.POST['hasta'].replace("/","-")
         print empresa +"--"+desde+"--"+hasta
         clientes = modelo_cliente.objects.filter(empresa=empresa,fecha_aceptado__range=[desde,hasta]).exclude(status=0).order_by('-cliente_id')
         log(str(clientes))
         contador = modelo_contador.objects.all()
         return render(request,'admin.html',{'clientes':clientes,'empresas':empresas,'contador':contador})
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
            print permissions
            if user.is_superuser:
               return HttpResponseRedirect('/admin_site/')
            elif permissions['level']==2:
               return HttpResponseRedirect('/home/'+str(permissions['page']))
            elif permissions['level']==1:
               return HttpResponseRedirect('/home/encargados/'+str(permissions['page']))
            elif permissions['level']==0:
               return render(request,'login.html',{'error':'no existe este encargado'})
            else:
               return render(request,'login.html',{'error':'error en contrasenha o username'})
        else:
            return render(request,'login.html',{'error':'usuario o contrasenha no valida'})

    elif request.method == 'GET':
      if(request.user.is_anonymous):
         return render(request,'login.html')
      else:
         permissions = levelpermissions(request.user)
         if int(permissions['level'])==10:
            return HttpResponseRedirect('/admin_site/')
         elif permissions['level']==2:
             return HttpResponseRedirect('/home/'+str(permissions['page']))
         elif permissions['level']==1:
             return HttpResponseRedirect('/home/encargados/'+str(permissions['page']))
         else:
            logout(request)
            return render(request,'login.html',{'error':'no hemos encontrado a ningun grupo al que pertenezca'})


@api_view(['GET'])
@login_required(login_url='/login/')
def base_de_datos(request,offset):
    permisos = credentials(request.user,offset)
    if(permisos['level']>1 and permisos['conexion']==True):
        if request.method == 'GET':
            r = modelo_cliente.objects.filter(empresa=permisos['empresa']).exclude(status=0).order_by('-cliente_id')

            return render(request,'base_de_datos.html',{'clientes': r ,'page':permisos['page'],'empresa':permisos['empresa']})
    return render(request,'base_de_datos.html',{'error': "disculpe, no tiene permisos suficientes para acceder a esta pantalla"})

def respconsumer(device,text):
   a = device.send_message(title='Delivery On',icon='/static/logito2.png', body=text)
   print a

@api_view(['GET', 'POST'])

@login_required(login_url='/login/')
def vista_consulta(request,offset):
   credenciales = credentials(request.user,offset)
   if(credenciales['conexion'] and int(credenciales['level'])==10):
      return HttpResponseRedirect('/admin_site/')
   elif credenciales['conexion'] and int(credenciales['level'])>1:
      if request.method == 'GET':
         #report_tread = threading.Thread(target=reportar,args=(str(request.data),str(request.META)))
         #report_tread.start()
         r = modelo_cliente.objects.filter(status=0,empresa=credenciales['empresa']).order_by('-cliente_id')
         queryset2 = modelo_encargado.objects.filter(empresa_id=credenciales['page'],puesto='En')
         return render(request,'ini.html',{'datos': r ,'encargados':queryset2,'valor':r.count(),'page':credenciales['page'],'empresa':credenciales['empresa']})
      #return Response({'datos': a.data ,'encargados':queryset2,'valor':r.count()})
      #preguntar si user es autenticado
      if request.method == 'POST':
      #print request.data.get('id')
         id_local = request.data.get('id')
         try:
            if(request.data.get('comando')!='eliminar'):
               p = modelo_cliente.objects.get(cliente_id=id_local)
               p.status=1
               p.fecha_aceptado = datetime.now().strftime('%Y-%m-%d')
               p.hora_aceptado = datetime.now().time().strftime('%H:%M:%S.%f')
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
               text = 'Pedido Aceptado! '+u'\U0001F60A'
               hilo2 = threading.Thread(target=respconsumer,args=(device,text))
               hilo2.start()
            elif request.data.get('comando')=='eliminar':
               print "comado eliminar"
               p = modelo_cliente.objects.get(cliente_id=id_local)
               p.status=3
               p.fecha_aceptado = datetime.now().strftime('%Y-%m-%d')
               p.hora_aceptado = datetime.now().time().strftime('%H:%M:%S.%f')
               text = 'Lo sentimos, pedido Rechazado. '+u'\U0001F614'
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
               hilo2 = threading.Thread(target=respconsumer,args=(device,text))
               hilo2.start()
               p.save()
            return Response(status=status.HTTP_201_CREATED)
         except AttributeError as b:
            log(b)

            return Response(status=status.HTTP_404_NOT_FOUND)
   else:
      log("error")
      return render(request,'error.html')

def reportar(request,meta):
    send_mail("Error",request+" "+meta,"deliveryon.gmail.com",["edujav22@gmail.com"],fail_silently=False)

@api_view(['GET'])
@login_required(login_url='/login/')
def vista_agregar_nuevo(request,offset):
   credenciales = credentials(request.user,offset)
   if credenciales['conexion'] and int(credenciales['level'])>1:
      if request.method == 'GET':
         encargados = modelo_encargado.objects.filter(empresa_id=offset,puesto='En')
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
         a =  date.today()
         return render(request,'encargados_table.html',{'datos':
                                                        modelo_cliente.objects.filter(fecha_aceptado__range=[a,a],
                                                        status=1).order_by('-cliente_id'),'empresa':credential['empresa'],
                                                        'page':credential['page']})
      if request.method == 'POST':
         if request.is_ajax()==True:
            if request.data.get('method')=="confirmar":
               print request.data.get('id')
               cliente = modelo_cliente.objects.get(cliente_id=request.data.get('id'))
               cliente.status = 2
               cliente.save()
               return Response(status=status.HTTP_201_CREATED)
         else:
            desde = request.POST['fecha_desde']
            hasta = request.POST['fecha_hasta']
            if desde=="" or hasta=="":
               print "vacio"
               return render(request,'encargados_table.html',{'error':"ingrese fechas validas"})
            clientes = modelo_cliente.objects.filter(fecha_aceptado__range=[desde, hasta],status=1).order_by('-cliente_id')
            return render(request,'encargados_table.html',{'datos':clientes,'page':credential['page'],'empresa':credential['empresa']})
   return render(request,'error.html')
class api_otro(generics.ListCreateAPIView):
    queryset = modelo_cliente.objects.filter(status=0).order_by('encargado')
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
   h = device.send_message(title='Delivery On',icon='/static/logito2.png', body='Nuevo Pedido')

def fecha_valida(fecha,dias):
    try:
        if fecha >= date.today():
            print "la fecha seleccionada es: "+str(fecha)
            dia_prog= fecha.isoweekday()
            print "dia programada: "+str(dia_prog)
            print "dias disponibles: "+str(dias)
            if dias.find(str(dia_prog))!=-1:
                return 1
            else:
                return 2
        else:
            return 3
    except:
        log("error de fecha")
        return 5

def hora_valida(hora_ini,hora_fin,actual):
    am = datetime.strptime("23:59:59",'%H:%M:%S').time()
    pm = datetime.strptime("00:00:00",'%H:%M:%S').time()
    print "hora apertura empresa: "+str(hora_ini)
    print "hora cierre empresa: "+str(hora_fin)
    print "hora programada por usuario: "+str(actual)
    if hora_ini<hora_fin:
        if actual>=hora_ini and actual<hora_fin:
            return 1
        else: return 2
    elif hora_ini>hora_fin:
        if (actual>=hora_ini and actual<am) or (actual>=pm and actual<hora_fin):
            return 3
        else: return 2
    else:
        return 4


class api_cliente(APIView):
    def post(self,request):
        a=clienteSerializer(data=request.data)
        a.is_valid()
        print a.is_valid()
        print a.errors
        if(a.is_valid()):
            if request.is_ajax()==False:
                print "ajax false"
                try:
                    hora = request.data.get('fecha_programado')
                    fecha = request.data.get('hora_programado')
                    consulta = modelo_empresa.objects.get(id=request.data.get('empresa_id'))
                    hora_ini = consulta.hora_atencion_inicio
                    hora_fin =consulta.hora_atencion_fin
                    dia =consulta.fechas_de_atencion
                    buscar = modelo_cliente.objects.filter(token=request.data.get('token'))
                except Exception as e:
                    return JsonResponse({'status':1,'msj':'hubo un error al procesar su solicitud, reintente'})
                    log("error al recibir pedido,1")
                    print "error 1"
                if hora==None and fecha==None:
                    print "hora none"
                    try:
                        fecha = date.today()
                        hora_actual = datetime.time(datetime.now())
                        fechaisValid = fecha_valida(fecha,dia)
                        hora_isValid = hora_valida(hora_ini,hora_fin,hora_actual)
                        print "hora is valid: "+str(hora_isValid)
                        print "fecha is valid: "+str(fechaisValid)
                    except Exception as e:
                        print e
                        return JsonResponse({'status':1,'msj':'hubo un error al procesar su solicitud, reintente'})
                        log(e)
                    if fechaisValid == 3:
                        print "error fecha pasada"
                        return JsonResponse({'status':1,'msj':'Fecha pasada seleccionada, elija de nuevo.'})
                    elif fechaisValid == 2:
                        return JsonResponse({'status':1,'msj':'Dia no esta disponible para atencion al cliente.'})
                    elif fechaisValid == 5:
                        print "hubo un error al procesar su solicitud"
                        return JsonResponse({'status':1,'msj':'hubo un error al procesar su solicitud, reintente'})
                    elif fechaisValid == 1:
                        if hora_isValid == 3 or hora_isValid==1:
                            print 'exitoso'
                            a.save()
                            try:
                                device = FCMDevice.objects.filter(user_id=request.data.get('empresa_id'))
                                print device
                                hilo = threading.Thread(target=enviar,args=(device,))
                                hilo.start()
                                return JsonResponse({'status':0,'msj': 'Pedido enviado!, pedido_id ='+str(buscar.last().cliente_id)})
                            except Exception as b:
                                print b
                                log("error envio de respuesta,2")
                        elif hora_isValid == 2:
                            return JsonResponse({'status':1,'msj': 'Horario fuera de rango de atencion al cliente.'})

                elif hora!=None and fecha!=None:
                    try:
                        fecha = datetime.date(datetime.strptime(request.data.get('fecha_programado'),'%Y-%m-%d'))
                        hora_actual = datetime.strptime(request.data.get('hora_programado'),'%H:%M').time()
                        fechaisValid = fecha_valida(fecha,dia)
                        hora_isValid = hora_valida(hora_ini,hora_fin,hora_actual)
                        print "hora is valid: "+str(hora_isValid)
                        print "fecha is valid: "+str(fechaisValid)

                    except Exception as e:
                        log(e)
                        print "hubo un error al procesar su solicitud"
                        return JsonResponse({'status':1,'msj':'hubo un error al procesar su solicitud, reintente'})

                    if fechaisValid == 3:
                        print "error fecha pasada"
                        return JsonResponse({'status':1,'msj':'Fecha pasada seleccionada, elija de nuevo.'})
                    elif fechaisValid == 2:
                        print "error  dia no disponible"
                        return JsonResponse({'status':1,'msj':'Dia no esta disponible para atencion al cliente.'})
                    elif fechaisValid == 5:
                        print "hubo un error al procesar su solicitud"
                        return JsonResponse({'status':1,'msj':'hubo un error al procesar su solicitud, reintente'})
                    elif fechaisValid == 1:
                        if hora_isValid == 3 or hora_isValid==1:
                            a.save()
                            try:
                                device = FCMDevice.objects.filter(user_id=request.data.get('empresa_id'))
                                print device
                                hilo = threading.Thread(target=enviar,args=(device,))
                                hilo.start()
                                return JsonResponse({'status':0,'msj': 'Exitoso, pedido_id ='+str(buscar.last().cliente_id)})
                            except:
                                print "error fcm api_cliente"
                        elif hora_isValid == 2:
                            print "hora no esta en el rango"
                            return JsonResponse({'status':1,'msj': 'Horario fuera de rango de atencion al cliente.'})
        print request.data
        return JsonResponse({'status':1,'msj':'error'})

    def get(self,request):
        r = modelo_cliente.objects.filter(status=0)
        a = clienteSerializer(instance=r,many=True)
        json = loads(dumps(a.data))
        #print json[0]
        return Response(json)

#df7800
#f21010
class api_cliente_2(generics.ListCreateAPIView):
    queryset = modelo_cliente.objects.all()
    serializer_class = clienteSerializer

class api_comentarios(APIView):
    def post(self,request):
        comentario = comentarioSerializer(data = request.data)
        if comentario.is_valid():
            comentario.save()
            return JsonResponse({'status':0})
        else:
            return JsonResponse({'status':1})
        return JsonResponse({'status':1})
    def get(self,request):
        return render(request,'error.html')


class api_productos(generics.ListCreateAPIView):
    queryset = modelo_producto.objects.all()
    serializer_class = productoSerializer

class api_empresa(APIView):
   def get(self,request):
      try:
         user = modelo_contador.objects.get(fecha=datetime.now().strftime('%Y-%m-%d'))
         user.cantidad = user.cantidad+1
         user.save()
      except modelo_contador.DoesNotExist:
         modelo_contador.objects.create(fecha=datetime.now().strftime('%Y-%m-%d'),cantidad=1)
      queryset = modelo_empresa.objects.all()
      a = empresaSerializer(queryset,many=True)
      json = loads(dumps(a.data))
      return JsonResponse(json,safe=False)
