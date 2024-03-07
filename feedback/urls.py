from django.urls import path
from .views import * 

urlpatterns = [
    path('', home, name="home"),
    path('<int:cod>/', home, name="home_with_cod"),
    path('salvarAnswer/', salvarAnswer, name="salvarAnswer"),
    path('obter_feed/<int:id>/', obter_feed, name='obter_feed'),
    path('modal_feedback/<int:id>/', modal_feedback, name='modal_feedback'),
    path('salvar_comentario/', salvar_comentario, name='salvar_comentario'),
    path('obter_comentarios/<int:id>/', obter_comentarios, name='obter_comentarios'),
]