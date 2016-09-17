from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View

from blogs.forms import LoginForm


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
                    return redirect(request.GET.get('next', 'photos_home'))
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