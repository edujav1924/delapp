from rest_framework import permissions
from django.contrib.auth.models import User, Group
from rest_framework import exceptions
from app.models import *
from django.http import HttpResponseRedirect, HttpResponse
def levelpermissions(user):
    if user.is_superuser:
        return HttpResponseRedirect('/admin_site/')
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
            return {'level':1,'page':int(res.id),'empresa':res.empresa}


def credentials(user,offset):
    if user.is_superuser:
        print "superiserer"
        return {'level':10,'conexion':True}
    else:
        permisos = levelpermissions(user)
        if(int(permisos['page'])==int(offset)):
            return {'level':permisos['level'],'page':permisos['page'],'conexion':True,'empresa':permisos['empresa']}
        else:
            return {'level':0,'conexion':False}
