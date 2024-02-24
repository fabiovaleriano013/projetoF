from django.shortcuts import render, redirect
from .models import *
from django.db.models import Count
from django.http import Http404, JsonResponse, HttpResponseBadRequest
from datetime import datetime
import json
from django.views import View


# Create your views here.
def home(request):
    u_questionario = questionario.objects.get()
    quests = questao.objects.filter(questionario_id=u_questionario)
    areas = area.objects.all()
    locais = local.objects.all()
    historic = feedback.objects.all()
    
    # historic = feedback.objects.filter(user_id=$_SESSION['id'])
    
    return render(
        request,
        "index_feedback.html",
        {'u_questionario': u_questionario,
         'quests': quests,
         'areas': areas,
         'locais': locais,
         'historic': historic}
    )

def salvarAnswer(request):
    try:
        # Decodificar os arrays do JSON
        array_pergunta = json.loads(request.POST.get("arrayP"))

        campos = ["titulo", "area", "local", "descricao"]
        Status = status.objects.get(status="Não Respondida")
        hora_atual = datetime.now()

        fb = feedback(status = Status, datahora = hora_atual)
        for a, c in zip(array_pergunta, campos):
            if c == "area" or c == "local":
            # Verifique se 'a' é um objeto 'area'
                try:
                    instance = area.objects.get(id=a) if c == "area" else local.objects.get(id=a)
                    setattr(fb, c, instance)
                except area.DoesNotExist:
                    # Lide com o caso em que a área não existe
                    print(f"A área com ID {a} não existe.")
                except local.DoesNotExist:
                    # Lide com o caso em que o local não existe
                    print(f"O local com ID {a} não existe.")
            else:
                inf = request.POST.get(a)
                setattr(fb, c, inf)

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

def get_feedback(request, id):
    # request.is_ajax() is deprecated since django 3.1
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    if is_ajax:
        if request.method == 'GET':
            feedback_obj = feedback.objects.get(id=id)
            context = {
                'feedback_obj': feedback_obj
            }
            return JsonResponse(context)
        return JsonResponse({'status': 'Invalid request'}, status=400)
    else:
        return HttpResponseBadRequest('Invalid request')

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