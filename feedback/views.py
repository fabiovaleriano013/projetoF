from django.apps import apps
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.serializers import serialize
from django.db.models import Count
from django.http import Http404, JsonResponse, HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from .models import *
from datetime import datetime
import json

@login_required
def home_feedback(request):
    u_questionario = Questionario.objects.get()
    quests = Questao.objects.filter(questionario_id=u_questionario)
    areas = Area.objects.all()
    locais = Local.objects.all()
    historic = Feedback.objects.all().order_by('-id')
    status = Status.objects.all()

    # Defina hoje como o dia atual
    hoje = datetime.today().date().strftime('%d/%m/%Y')

    if request.user.is_staff:
        Eadm = True
        mails = Feedback.objects.all().order_by('-id')
        
        context = {
            'u_questionario': u_questionario,
             'quests': quests,
             'areas': areas,
             'locais': locais,
             'mails': mails,
             'historic': historic,
             'status': status,
             'hoje': hoje,
             'Eadm': Eadm
        }
    else:
        Eadm = False

        context = {
            'u_questionario': u_questionario,
            'quests': quests,
            'areas': areas,
            'locais': locais,
            'historic': historic,
            'status': status,
            'hoje': hoje,
            'Eadm': Eadm,
        }
    
    return render(request, "index_feedback.html", context)
    # historic = Feedback.objects.filter(user_id=$_SESSION['id'])

def salvar_Answer(request):
    # Decodificar os arrays do JSON
    array_pergunta = json.loads(request.POST.get("arrayP"))

    campos = ["area", "local", "descricao", "imagem"]
    status = Status.objects.get(status="Não Respondida")

    fb = Feedback(status=status, quantidade=1)
    for a, c in zip(array_pergunta, campos):
        if c == "area" or c == "local":
            try:
                if c == "area":
                    instance = Area.objects.get(id=request.POST.get(a))
                else:
                    instance = Local.objects.get(id=request.POST.get(a))
                setattr(fb, c, instance)
            except Area.DoesNotExist:
                print(f"A área com ID {a} não existe.")
            except Local.DoesNotExist:
                print(f"O local com ID {a} não existe.")
        elif c == "imagem":
            # Verificar se há uma imagem no request.FILES
            imagem = request.FILES.get(a)
            if imagem:
                fb.imagem = imagem
        else:
            inf = request.POST.get(a)
            setattr(fb, c, inf)

    fb.save()

    return HttpResponse(status=204)

    # except Exception as e:
    #     # Em caso de erro, redirecione para uma página de erro
    #     # return HttpResponse(
    #     # '<script>alert("Não foi possível responder, tente novamente - - - error_message"); window.location.href = "javascript:history.back()";</script>'
    #     # )
    #     error_message = f"Erro ao salvar o Feedback: {str(e)}"
    #     print(e)
    #     return render(request, "index_feedback.html", {"error_message": error_message})

def obter_feed(request, id):
    if id == 0:
        mails = Feedback.objects.all().select_related('area', 'local').order_by('-id')
    else: 
        mails = Feedback.objects.filter(area=id).select_related('area', 'local').order_by('-id')
    mails_serializados = serialize('json', mails, use_natural_foreign_keys=True)
    return JsonResponse(mails_serializados, safe=False)

def modal_feedback(request, id):
    feed = Feedback.objects.filter(id=id).select_related('area', 'local')
    feed_serializados = serialize('json', feed, use_natural_foreign_keys=True)
    return JsonResponse(feed_serializados, safe=False)

@login_required
def salvar_comentario(request):
    if request.method == 'POST':
        texto_comentario = request.POST.get('texto')
        imagem = request.FILES.get('coment_img')

        novo_comentario = Comentario()
        feedback_id = Feedback.objects.get(id=request.POST.get('feedback_id'))
        if texto_comentario != '-':
            novo_comentario.comentario = texto_comentario
        if imagem:
            novo_comentario.imagem = imagem
            
        # Verifique se o usuário existe
        # usuario_logado = User.objects.get(id=request.user.id)
        
        if request.user.is_superuser:
            usuario_logado = Usuario.objects.get(nome='admin')
        else:
            usuario_logado = Usuario.objects.get(nome='usuario_comum')

        # Crie o objeto de comentário e salve no banco de dados
        novo_comentario.usuario = usuario_logado
        setattr(novo_comentario, 'feedback_id', feedback_id)
        novo_comentario.save()

    # Em caso de método GET ou outros casos, você pode lidar conforme necessário
    return HttpResponse("Erro: Método não suportado ou dados ausentes.")

def obter_comentarios(request, id):
    comentarios = Comentario.objects.filter(feedback_id=id).select_related('usuario')
    comentarios_serializados = serialize('json', comentarios, use_natural_foreign_keys=True)
    return JsonResponse(comentarios_serializados, safe=False)

def atualizar_status(request):
    # Obter os dados enviados pela requisição AJAX
    id_feedback = request.POST.get('feedback_id2')

    # Buscar o feedback no banco de dados
    novo_status = Status.objects.get(id=request.POST.get('select_status'))
    fb = Feedback.objects.get(id=id_feedback)

    # Atualizar o status do feedback
    fb.status = novo_status
    fb.save()
    
    return HttpResponse(status=204)

def verifica(request):
    # Decodificar os arrays do JSON
    array_pergunta = json.loads(request.POST.get("arrayP"))

    campos = ["area", "local"]
    for a, c in zip(array_pergunta, campos):
        if c == "area":
            area_id = Area.objects.get(id=request.POST.get(a))
        elif c == "local":
            local_id = Local.objects.get(id=request.POST.get(a))
    print(area_id)
    print(local_id)

    # Realize a consulta filtrando por área e local
    feedbacks = Feedback.objects.filter(area_id=area_id, local_id=local_id)

    # Converta os feedbacks em um formato adequado para JSON
    feedback_data = [
        {
            'id': feedback.id,
            'descricao': feedback.descricao,
            'imagem': feedback.imagem.url if feedback.imagem else None, 
            'status': feedback.status.status, 
            'datahora': feedback.datahora.isoformat() 
        }
        for feedback in feedbacks
    ]
    
    print(feedback_data)

    return JsonResponse({'feedbacks': feedback_data})

@csrf_exempt
def increase(request):
    feedback_id = request.POST.get('feedback_id')  # Obtenha o ID do feedback
    print(feedback_id)
    feedback = Feedback.objects.get(id=feedback_id)
    feedback.quantidade += 1  # Incrementa a quantidade
    feedback.save()
    return HttpResponse(status=200)