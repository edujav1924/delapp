from rest_framework import permissions
from django.contrib.auth.models import User, Group
from rest_framework import exceptions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_permission(self, request, view):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method == 'GET':
            username = request.user
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                raise exceptions.AuthenticationFailed('No such user')
            try:
                group = Group.objects.get(user=username)
                print type(str(group))
                if (str(group) == "encargados"):
                    print 'entre'
                    return True
            except:
                raise exceptions.AuthenticationFailed('NO existe grupo')
        return False
