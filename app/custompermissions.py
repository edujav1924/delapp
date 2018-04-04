from rest_framework import permissions
from django.contrib.auth.models import User, Group
from rest_framework import exceptions

def levelpermissions(user):
    if user.is_superuser:
        return 10
    elif user.is_staff:
        return 2
    elif user.is_active:
        group = Group.objects.get(user=user)
        print type(str(group))
        if (str(group) == "encargados"):
            return 1
        return 0    


def isencargado(username):
    group = Group.objects.get(user=username)
    print type(str(group))
    if (str(group) == "encargados"):
        return True
    return False
