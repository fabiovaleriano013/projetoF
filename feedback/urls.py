from django.urls import path
from .views import * 

urlpatterns = [
    path('', home, name="index"),
    path('salvarAnswer/', salvarAnswer, name="salvarAnswer"),
    path('get_feedback/<int:id>/', get_feedback, name='get_feedback'),
    path('<str:link>', ver_form, name="ver_form"),
]