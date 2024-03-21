from django.urls import path
from .views import * 

urlpatterns = [
    path('', home_feedback, name="home_feedback"),
    path('feedback/salvarAnswer/', salvarAnswer, name="salvarAnswer"),
    path('feedback/obter_feed/<int:id>/', obter_feed, name='obter_feed'),
    path('feedback/modal_feedback/<int:id>/', modal_feedback, name='modal_feedback'),
    path('feedback/salvar_comentario/', salvar_comentario, name='salvar_comentario'),
    path('feedback/obter_comentarios/<int:id>/', obter_comentarios, name='obter_comentarios'),
]