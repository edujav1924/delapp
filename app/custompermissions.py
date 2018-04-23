from rest_framework import permissions
from django.contrib.auth.models import User, Group
from rest_framework import exceptions
from app.models import *

def levelpermissions(user):
    if user.is_superuser:
        return 10
    elif user.is_staff:
        return 2
    elif user.is_active:
        group = Group.objects.filter(user=user)
        if (str(group[0]) == "encargados"):
            emp = str(group[1])
            a = emp.find("_")
            b = emp[a+1:]
            print b
            res = modelo_empresa.objects.get(empresa=b)
            return {'level':1,'page':res}
        return 0
