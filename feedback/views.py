from django.shortcuts import render, redirect
from .models import *
from django.db.models import Count
from django.http import Http404, JsonResponse
from datetime import datetime
import json
from django.views import View

# Create your views here.
def home(request):
    u_questionario = questionario.objects.get()
    quests = questao.objects.filter(questionario_id=u_questionario)
    areas = area.objects.all()
    historic = feedback.objects.all()
    
    # historic = feedback.objects.filter(user_id=$_SESSION['id'])
    
    return render(
        request,
        "index_feedback.html",
        {'u_questionario': u_questionario,
         'quests': quests,
         'areas': areas,
         'historic': historic}
    )

class GetFeedbacksView(View):
    def get(self, request, *args, **kwargs):
        try:
            # Buscar todos os registros da tabela feedback ordenados pelo ID decrescente
            feedbacks = feedback.objects.all().order_by('-id')

            # Construir uma lista de dicionários com os dados
            feedbacks_list = [
                {
                    'id': feedback.id,
                    'Title': feedback.Title,
                    'area': feedback.area.area,
                    'Descricao': feedback.Descricao,
                    'status': feedback.status.status,
                    'Time': feedback.Time.strftime("%Y-%m-%d %H:%M:%S"),
                }
                for feedback in feedbacks
            ]

            # Retornar os dados em formato JSON
            return JsonResponse({'feedbacks': feedbacks_list})

        except Exception as e:
            # Tratar exceções conforme necessário
            return JsonResponse({'error': str(e)}, status=500)
        
def salvarAnswer(request):
    try:    
        # Crie um objeto questionario com o nome
        questionario_id = request.POST.get("idQuestionario")
        Questionario = questionario.objects.get(id=questionario_id)

        titulo = request.POST.get("titulo")
        Area = area.objects.get(id=request.POST.get("area"))
        descricao = request.POST.get("descricao")
        Status = status.objects.get(status="Não Respondida")
        hora_atual = datetime.now()

        fb = feedback(titulo = titulo, area = Area, descricao = descricao, status = Status, datahora = hora_atual)
        fb.save()

        # Redirecione para a página de sucesso ou faça o que for necessário
        return redirect(home)

    except Exception as e:
        # Em caso de erro, redirecione para uma página de erro
        # return HttpResponse(
        # '<script>alert("Não foi possível responder, tente novamente - - - error_message"); window.location.href = "javascript:history.back()";</script>'
        # )
        error_message = f"Erro ao salvar o Feedback: {str(e)}"
        return render(request, "index_feedback.html", {"error_message": error_message})


def ver_form(request, link):
    try:
        # Tente buscar pelo campo 'link'
        u_questionario = questionario.objects.get(link=link)
    except:
        u_questionario = questionario.objects.get(link_resposta=link)
    quests = questao.objects.filter(questionario_id=u_questionario)
    areas = area.objects.all()
    historic = feedback.objects.all()
    
    # historic = feedback.objects.filter(user_id=$_SESSION['id'])
    
    return render(
        request,
        "index_feedback.html",
        {'u_questionario': u_questionario,
         'quests': quests,
         'areas': areas,
         'historic': historic}
    )