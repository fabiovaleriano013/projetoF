from django.shortcuts import render, redirect
from django.urls import reverse
from .models import *
from django.db.models import Count
from django.core.serializers import serialize
from django.http import Http404, JsonResponse, HttpResponse, HttpResponseBadRequest
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
        "pagina2.html",
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

        fb = feedback(status = Status)
        for a, c in zip(array_pergunta, campos):
            if c == "area" or c == "local":
                try:
                    if c == "area":
                        instance = area.objects.get(id=request.POST.get(a))
                    else:
                        instance = local.objects.get(id=request.POST.get(a))
                    setattr(fb, c, instance)
                except area.DoesNotExist:
                    print(f"A área com ID {a} não existe.")
                except local.DoesNotExist:
                    print(f"O local com ID {a} não existe.")
            else:
                inf = request.POST.get(a)
                setattr(fb, c, inf)

        fb.save()

        rota = request.POST.get("log")

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

def salvar_comentario(request):
    if request.method == 'POST':
        texto_comentario = request.POST.get('texto', '')
        feedback_id = feedback.objects.get(id=request.POST.get('feedback_id', ''))
        rota = request.POST.get('log2', '')
        user = usuario.objects.get(nome=rota)

        # Crie o objeto de comentário e salve no banco de dados
        novo_comentario = comentario(comentario=texto_comentario, usuario=user, feedback_id=feedback_id)
        novo_comentario.save()


        if rota == "adm":
            # Redirecione para a página de sucesso ou faça o que for necessário
            return redirect(reverse('ver_form', args=[0]))
        elif rota == "usuario_comum":
            return redirect(home)

    # Em caso de método GET ou outros casos, você pode lidar conforme necessário
    return HttpResponse("Erro: Método não suportado ou dados ausentes.")

def obter_comentarios(request, id):
    comentarios = comentario.objects.filter(feedback_id=id)
    comentarios_serializados = serialize('json', comentarios)
    return JsonResponse(comentarios_serializados, safe=False)