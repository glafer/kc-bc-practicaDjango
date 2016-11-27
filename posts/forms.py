from django.forms import ModelForm
from django import forms

from categories.models import Category
from posts.models import Post


class DateInput(forms.DateInput):
    input_type = 'date'

class PostForm(ModelForm):

    title = forms.CharField(label="Titulo", required=True)
    short_description = forms.CharField(label="Introducción", required=True)
    body = forms.CharField(label="Texto", widget=forms.Textarea, required=True)
    image_url = forms.URLField(label="Imagen del post", required=True)
    publication_date = forms.DateTimeField(label="Fecha de publicación", required=True,
                                           widget=DateInput, input_formats=['%Y-%m-%d'])
    categories = forms.ModelMultipleChoiceField(queryset=Category.objects.all(), label="Categorias",
                                                widget=forms.CheckboxSelectMultiple, required=False)

    class Meta:
        model = Post
        exclude = ["owner"]
