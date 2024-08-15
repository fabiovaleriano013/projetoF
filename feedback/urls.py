
from django.urls import path
from .views import * 

urlpatterns = [
    path('', home_feedback, name="home_feedback"),
    path('salvar_Answer/', salvar_Answer, name="salvar_Answer"),
    path('obter_feed/<int:id>/', obter_feed, name='obter_feed'),
    path('modal_feedback/<int:id>/', modal_feedback, name='modal_feedback'),
    path('salvar_comentario/', salvar_comentario, name='salvar_comentario'),
    path('obter_comentarios/<int:id>/', obter_comentarios, name='obter_comentarios'),
    path('atualizar_status/', atualizar_status, name='atualizar_status'),
    path('verifica/', verifica, name='verifica'),
    path('increase', increase, name='increase'),
]
