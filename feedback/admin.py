from django.contrib import admin
from .models import *

# link aleatorio
import nested_admin
import random
import string
from django.utils.html import format_html
from django.urls import reverse

# Register your models here.

class QuestaoInline(nested_admin.NestedStackedInline):
    model = questao
    extra = 1

def link_resposta(obj):
    # return f'http://127.0.0.1:8000/questionario/{obj.link_resposta}'
    return format_html(
            '<a style="color: lightblue; text-decoration: underline;" href="{}" target="_blank">'
            'Visualizar Respostas'
            '</a>',
            reverse('ver_form', args=[1]),
        )

class QuestionarioAdmin(nested_admin.NestedModelAdmin):
    list_display = ('id', 'nome', link_resposta)
    list_editable = ('nome',)
    exclude = ('link', 'link_resposta')
    
    inlines = [QuestaoInline]

    # readonly_fields = ('link',)  # Define 'link' como somente leitura

    def save_model(self, request, obj, form, change):
        if not obj.link:
            # Gere um código aleatório de 25 caracteres
            obj.link = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(25))

        if not obj.link_resposta:
            # Gere um código aleatório de 25 caracteres
            obj.link_resposta = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(25))

        obj.save()

class QuestaoAdmin(admin.ModelAdmin):
    list_display = ('id', 'titulo')

class ComentarioAdmin(admin.ModelAdmin):
    list_display = ('id', 'comentario', 'datahora', 'feedback_id')

class ComentarioInline(admin.TabularInline):  # Use admin.StackedInline se preferir exibição empilhada
    fields = ('comentario', 'usuario', 'datahora')
    readonly_fields = ('datahora',)  # Adicione 'datahora' aqui
    model = comentario
    extra = 1  # Número de formulários em branco exibidos para novos Comentarios

class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'descricao', 'datahora')
    inlines = [ComentarioInline]

class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'email')

admin.site.register(feedback, FeedbackAdmin)
admin.site.register(area)
admin.site.register(local)
admin.site.register(status)
admin.site.register(comentario, ComentarioAdmin)
admin.site.register(usuario, UsuarioAdmin)

admin.site.register(questionario, QuestionarioAdmin)
admin.site.register(tipo)
admin.site.register(questao, QuestaoAdmin)