from django.shortcuts import render
from django.utils.datetime_safe import datetime
from django.views import View

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
        context = {'posts_list': posts[:3]}
        return render(request, 'posts/home.html', context)
