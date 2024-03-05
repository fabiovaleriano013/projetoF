from django.urls import path
from .views import * 

urlpatterns = [
    path('', home, name="index"),
    path('salvarAnswer/', salvarAnswer, name="salvarAnswer"),
    path('ver_form/<int:cod>/', ver_form, name="ver_form"),
    path('obter_feed/<int:id>/', obter_feed, name='obter_feed'),
    path('salvarcomentario/', salvar_comentario, name='salvar_comentario'),
    path('obter_comentarios/<int:id>/', obter_comentarios, name='obter_comentarios'),
]