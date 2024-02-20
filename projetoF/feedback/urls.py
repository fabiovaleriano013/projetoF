from django.urls import path
from .views import * 

urlpatterns = [
    path('', home, name="index"),

    path('salvarAnswer/', salvarAnswer, name="salvarAnswer"),
    path('get_feedbacks/', GetFeedbacksView.as_view(), name='get_feedbacks'),

    path('<str:link>', ver_form, name="ver_form"),
]