from rest_framework.permissions import BasePermission


class IsModerator(BasePermission):

    def has_permission(self, request, view):
        """ Jestli je user moderator """
        return request.user.groups.filter(name='moderator').exists()

class IsOwner(BasePermission):
    def has_permission(self, request, view):
        print("IsOwner permission check")
        return request.user == view.get_object().owner


"""
práce v shell
python manage.py shell
>>> from users.models import User
>>> u = User.objects.get(pk=1)
>>> u.__dict__ etc...
"""