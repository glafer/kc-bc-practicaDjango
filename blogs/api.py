from django.contrib.auth.models import User
from rest_framework.generics import get_object_or_404

from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_202_ACCEPTED, HTTP_204_NO_CONTENT
from rest_framework.views import APIView

from blogs.serializers import BlogSerializer, BlogListSerializer
from practica.permissions import UserIsOwnerOrAdmin


class BlogDetailAPI(APIView):
    """
    Endpoin detalle/creación/modificación usuarios/blogs
    """

    permission_classes = (UserIsOwnerOrAdmin,)

    def get(self, request, pk):
        blog = get_object_or_404(User, pk=pk)
        self.check_object_permissions(request, blog)
        serializer = BlogSerializer(blog)
        return Response(serializer.data)

    def put(self, request, pk):
        blog = get_object_or_404(User, pk=pk)
        self.check_object_permissions(request, blog)
        serializer = BlogSerializer(blog, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_202_ACCEPTED)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
         blog = get_object_or_404(User, pk=pk)
         self.check_object_permissions(request, blog)
         blog.delete()
         return Response(status=HTTP_204_NO_CONTENT)


class BlogListAPI(APIView):
    """
    Endpoint de listado de usuarios
    """

    def get(self, request):
        blogs = User.objects.all()
        serializer = BlogListSerializer(blogs, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = BlogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        else:
            return Response(serializer.data, status=HTTP_400_BAD_REQUEST)
