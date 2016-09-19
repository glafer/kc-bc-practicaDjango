from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect
from django.utils.datetime_safe import datetime
from django.utils.decorators import method_decorator
from django.views import View

from blogs.forms import LoginForm, UserCreateForm
from posts.models import Post


class ListView(View):

    @method_decorator(login_required())
    def get(self, request):
        """
        Renderiza la index con el listado de los últimos posts de los usuarios
        :param request: objeto HttpRequest con los datos de la petición
        :return: objeto HttpResponse con los datos de la respuesta
        """
        # recupera todas las fotos de la base de datos
        blogs_list = User.objects.all()
        context = {'blogs_list': blogs_list[:5]}
        return render(request, 'blogs/list.html', context)

class SignUpView(View):

    def get(self, request):
        """
        Presenta el formulario de signup y gestiona el signup de un usuario
        :param request: objeto HttpRequest con los datos de la petición
        :return: objeto HttpResponse con los datos de la respuesta
        """
        if not request.user.is_authenticated:
            signup_form = UserCreateForm()
            context = {'form': signup_form}
            return render(request, 'blogs/signup.html', context)
        else:
            return redirect('posts_home')

    def post(self, request):
        """
        Presenta el formulario de signup y gestiona el signup de un usuario
        :param request: objeto HttpRequest con los datos de la petición
        :return: objeto HttpResponse con los datos de la respuesta
        """
        user_form = UserCreateForm(request.POST)
        if user_form.is_valid():
            user_form.save()
            username = request.POST.get('username')
            password = request.POST.get('password1')
            user = authenticate(username=username, password=password)
            django_login(request, user)
            return redirect('posts_home')

        context = {'form': user_form}
        return render(request, 'blogs/signup.html', context)

class LoginView(View):

    def get(self, request):
        """
        Presenta el formulario de login y gestiona el login de un usuario
        :param request: objeto HttpRequest con los datos de la petición
        :return: objeto HttpResponse con los datos de la respuesta
        """
        error_message = ""
        login_form = LoginForm(request.POST) if request.method == "POST" else LoginForm()
        context = {'error': error_message, 'form': login_form}
        return render(request, 'blogs/login.html', context)

    def post(self, request):
        """
        Presenta el formulario de login y gestiona el login de un usuario
        :param request: objeto HttpRequest con los datos de la petición
        :return: objeto HttpResponse con los datos de la respuesta
        """
        error_message = ""
        login_form = LoginForm(request.POST) if request.method == "POST" else LoginForm()
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('pwd')
            user = authenticate(username=username, password=password)
            if user is None:
                error_message = "Usuario o contraseña incorrecto"
            else:
                if user.is_active:
                    django_login(request, user)
                    return redirect(request.GET.get('next', 'posts_home'))
                else:
                    error_message = "Cuenta de usuario inactiva"
        context = {'error': error_message, 'form': login_form}
        return render(request, 'blogs/login.html', context)


class LogoutView(View):

    def get(self, request):
        """
        Hace el logout de un usuario y redirige al home
        :param request: objeto HttpRequest con los datos de la petición
        :return: objeto HttpResponse con los datos de la respuesta
        """
        if request.user.is_authenticated():
            django_logout(request)
        return redirect('posts_home')


class BlogQueryset(object):

    @staticmethod
    def get_posts_from_blog_by_user(owner, loged_user):
        possibles_posts = Post.objects.all().select_related("owner")
        if loged_user.is_superuser or owner[0] == loged_user:
            possibles_posts = possibles_posts.filter(owner=owner).order_by('-created_at')
        else:
            possibles_posts = possibles_posts.filter(publication_date__lt=datetime.now(), owner=owner).order_by('-created_at')
        return possibles_posts


class BlogView(View):

    def get(self, request, username):
        """
        Renderiza la página del blog del usuario pintando solo sus posts publicados
        :param request: objeto HttpRequest con los datos de la petición
        :return: objeto HttpResponse con los datos de la respuesta
        """
        owner = User.objects.filter(username=username.replace('@', ''))

        if len(owner) == 0:
            return HttpResponseNotFound("No hemos encontrado ese usuario")
        blog_posts = BlogQueryset.get_posts_from_blog_by_user(owner, request.user)


        context = {'posts': blog_posts, 'owner': owner[0] }

        return render(request, 'blogs/userblog.html', context)
