from rest_framework import permissions


class UserPermissionOnBlogs(permissions.BasePermission):

    def has_permission(self, request, view):
        if view.action == 'list':
            return True
        elif view.action == 'create':
            return True
        elif view.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            return request.user.is_authenticated()
        else:
            return False

    def has_object_permission(self, request, view, obj):
        if view.action == 'list':
            return True
        elif view.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            return request.user.is_authenticated() and (obj == request.user or request.user.is_staff)
        else:
            return False


class UserPermissionOnPosts(permissions.BasePermission):

    def has_permission(self, request, view):
        if view.action in ['list', 'retrieve']:
            return True
        elif view.action in ['retrieve', 'create', 'update', 'partial_update', 'destroy']:
            return request.user.is_authenticated()
        else:
            return False

    def has_object_permission(self, request, view, obj):
        if view.action in ['list', 'retrieve']:
            return True
        elif view.action == 'create':
            return request.user.is_authenticated()
        elif view.action in ['update', 'partial_update', 'destroy']:
            return (obj.owner == request.user or request.user.is_staff)
        else:
            return False
