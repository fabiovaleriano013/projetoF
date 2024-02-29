from django.shortcuts import render, redirect
from django.urls import reverse
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
        # array_pergunta = json.loads(request.POST.get("arrayP"))

        # campos = ["titulo", "area", "local", "descricao"]
        Status = status.objects.get(status="Não Respondida")
        hora_atual = datetime.now()
        a = area.objects.get(id=request.POST.get("area"))
        b = local.objects.get(id=request.POST.get("local"))
        c = request.POST.get("titulo")
        d = request.POST.get("descricao")

        fb = feedback(status = Status, datahora = hora_atual)
        # for a, c in zip(array_pergunta, campos):
        #     if c == "area" or c == "local":
        #     # Verifique se 'a' é um objeto 'area'
        #         try:
        #             try:
        #                 instance = area.objects.get(id=a)
        #             except:
        #                 instance = local.objects.get(id=a)
        #             setattr(fb, c, instance)
        #         except area.DoesNotExist:
        #             # Lide com o caso em que a área não existe
        #             print(f"A área com ID {a} não existe.")
        #         except local.DoesNotExist:
        #             # Lide com o caso em que o local não existe
        #             print(f"O local com ID {a} não existe.")
        #     else:
        #         inf = request.POST.get(a)
        #         setattr(fb, c, inf)

        fb.save()

        rota = request.POST.get("permissao")

        if rota == "adm":
            # Redirecione para a página de sucesso ou faça o que for necessário
            return redirect(reverse('ver_form', args=[0]))
        elif rota == "user":
            return redirect(home)

    except Exception as e:
        # Em caso de erro, redirecione para uma página de erro
        # return HttpResponse(
        # '<script>alert("Não foi possível responder, tente novamente - - - error_message"); window.location.href = "javascript:history.back()";</script>'
        # )
        error_message = f"Erro ao salvar o Feedback: {str(e)}"
        return render(request, "index_feedback.html", {"error_message": error_message})

def get_feedback(request, id):
    # Faça a consulta no banco de dados
    feedback_list = feedback.objects.filter(area=id)

    # Retorne os dados como JSON
    return JsonResponse(feedback_list, safe=False)

def ver_form(request, cod):
    u_questionario = questionario.objects.get()
    if cod == 0:
        mails = feedback.objects.all()
    else:
        mails = feedback.objects.filter(area = cod)
    quests = questao.objects.filter(questionario_id=u_questionario)
    areas = area.objects.all()
    locais = local.objects.all()
    historic = feedback.objects.all()
    
    # historic = feedback.objects.filter(user_id=$_SESSION['id'])
    
    return render(
        request,
        "pagina2.html",
        {'u_questionario': u_questionario,
         'quests': quests,
         'areas': areas,
         'locais': locais,
         'mails': mails,
         'historic': historic}
    )