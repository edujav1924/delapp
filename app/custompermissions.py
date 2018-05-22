from rest_framework import permissions
from django.contrib.auth.models import User, Group
from rest_framework import exceptions
from app.models import *
from django.http import HttpResponseRedirect, HttpResponse
def levelpermissions(user):
    if user.is_superuser:
        return {'level':10,'conexion':True}
    elif user.is_active:
        try:
            usuario = User.objects.get(username=user)
            try:
                encargado = modelo_encargado.objects.get(nombre_id=usuario.id)
                if encargado.puesto=='Sp':
                    return {'level':2,'page':encargado.empresa_id,'empresa':modelo_empresa.objects.get(id=encargado.empresa_id).empresa}
                elif encargado.puesto == 'En':
                    return {'level':1,'page':encargado.empresa_id,'empresa':modelo_empresa.objects.get(id=encargado.empresa_id).empresa}
            except modelo_encargado.DoesNotExist as e:
                print "no exite encargado"
                return {'level':0,'conexion':False}
        except User.DoesNotExist as e:
            return {'level':0,'conexion':False}
    else:
        return{'conexion':False,'level':0}

def credentials(user,offset):
    if user.is_superuser:
        return {'level':10,'conexion':True}
    else:
        permisos = levelpermissions(user)
        if(int(permisos['page'])==int(offset)):
            return {'level':permisos['level'],'page':permisos['page'],'conexion':True,'empresa':permisos['empresa']}
        else:
            return {'level':0,'conexion':False}

'''if user.is_superuser:
    return{'level':10}
elif user.is_staff:
    group = Group.objects.filter(user=user)
    group = str(group[0])
    flag = group.find('_')
    empresa = group[:flag]
    cargo = group[flag+1:]
    if (cargo == "supervisor"):
        res = modelo_empresa.objects.get(empresa=empresa)
        return {'level':2,'page':res.id,'empresa':res.empresa}
elif user.is_active:
    group = Group.objects.filter(user=user)
    group = str(group[0])
    flag = group.find('_')
    empresa = group[:flag]
    cargo = group[flag+1:]
    if (cargo == "encargado"):
        res = modelo_empresa.objects.get(empresa=empresa)
        return {'level':1,'page':int(res.id),'empresa':res.empresa}'''
