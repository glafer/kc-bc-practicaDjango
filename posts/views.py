from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.http import HttpResponseNotFound
from django.shortcuts import render
from django.utils.datetime_safe import datetime
from django.utils.decorators import method_decorator
from django.views import View

from posts.forms import PostForm
from posts.models import Post


class HomeView(View):

    def get(self, request):
        """
        Renderiza la index con el listado de los últimos posts de los usuarios
        :param request: objeto HttpRequest con los datos de la petición
        :return: objeto HttpResponse con los datos de la respuesta
        """
        # recupera todas las fotos de la base de datos
        posts = Post.objects.filter(publication_date__lt=datetime.now()).order_by('-created_at')
        context = {'posts_list': posts}
        return render(request, 'posts/home.html', context)


class PostView(View):

    @staticmethod
    def get_post_by_pk_owner(user, loged_user, pk):
        post = Post.objects.all().select_related("owner")
        if loged_user.is_superuser or user[0] == loged_user:
            post = post.filter(owner=user, pk=pk)
        else:
            post = post.filter(publication_date__lt=datetime.now(), owner=user, pk=pk).order_by('-created_at')
        return post

    def get(self, request, username, pk):
        """
        Pinta la vista detalle de un post
        :param request: objeto HttpRequest con los datos de la petición
        :param username: el nombre del usuari propietario del post
        :param pk: el id del posts a visualizar
        :return: objeto HttpResponse con los datos de la respuesta
        """
        post = self.get_post_by_pk_owner(User.objects.filter(username=username.replace('@', '')), request.user, pk)

        if len(post) == 0:
            return HttpResponseNotFound("No hemos encontrado ese post de este usuario")
        elif len(post) > 1:
            return HttpResponse("Múltiples opciones", status=300)
        else:
            return render(request, 'posts/detail.html', {'post': post[0]})


class PostCreationView(View):

    @method_decorator(login_required())
    def get(self, request):
        """
        Muestra el formulario de creación de post a un usuario logado
        :param request: objeto HttpRequest con los datos de la petición
        :return: objeto HttpResponse con los datos de la respuesta
        """
        post_form = PostForm()
        context = {'form': post_form}
        return render(request, 'posts/create.html', context)

    @method_decorator(login_required())
    def post(self, request):
        """
        Presenta el formulario para crear un post y, en caso de la peticion sea POST la valida y la crea en caso de que sea válida
        :param request:  objeto HttpRequest con los datos de la petición
        :return:  objeto HttpResponse con los datos de la respuesta
        """
        new_post_pk = None
        username = '@' + request.user.username
        post_with_user = Post(owner=request.user)
        post_form = PostForm(request.POST, instance=post_with_user)
        if post_form.is_valid():
            new_post = post_form.save()
            post_form = PostForm()
            new_post_pk = new_post.pk
        context = {'form': post_form, 'new_photo_pk': new_post_pk, 'username': username}
        return render(request, 'posts/create.html', context)
