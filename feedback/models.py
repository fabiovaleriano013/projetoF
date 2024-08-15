from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User

import os

# Função que adiciona as imagens do feedback dinamicamente na pasta static/img do app
def image_upload_path(instance, filename):
    # Obtém o nome do app do modelo
    app_label = instance._meta.app_label
    # Constrói o caminho de upload. Você pode modificar isso conforme necessário.
    upload_path = os.path.join('apps', app_label, 'static', 'img', filename)
    print(upload_path)
    return upload_path

class Questionario(models.Model):
    nome = models.CharField(max_length=255 ,null=True)
    # owner = models.CharField(max_length=50, null=True, verbose_name="Criado_por")
    # created_at = models.DateTimeField(null=True, auto_now_add=True)
    # last_update = models.DateTimeField(null=True, auto_now_add=True)
    link = models.CharField(max_length=25, null=True)
    link_resposta = models.CharField(max_length=25, null=True)
    
    class Meta:
        verbose_name = _("Questionário")
        verbose_name_plural = _("Questionário")

    def __str__(self):
        return self.nome
    
class Tipo(models.Model):
    tipo_opcoes = [
        ('Resposta Curta', 'Resposta Curta'),
        ('Resposta Longa', 'Resposta Longa'),
        ('Única Escolha', 'Única Escolha'),
        ('Várias Escolhas', 'Várias Escolhas'),
        ('Dropdown', 'Dropdown'),
        ('Imagem', 'Imagem'),
    ]
    tipo = models.CharField(max_length=50, choices=tipo_opcoes, unique=True)

    class Meta:
        verbose_name = _("Tipo")
        verbose_name_plural = _("Tipos")

    def __str__(self):
        return self.tipo

class Questao(models.Model):
    titulo = models.TextField(null=True, verbose_name="Nome")
    tipo = models.ForeignKey(Tipo, on_delete=models.DO_NOTHING)
    questionario_id = models.ForeignKey(Questionario, on_delete=models.CASCADE)
    area = models.BooleanField(default=False, unique=False)
    local = models.BooleanField(default=False, unique=False)
    # Tipo, se a questão tem como resposta texto, multiplas respostas, seleção única, ou caixa de seleção
    # 1 = Area
    # 2 = textarea
    # 3 = radio
    # 4 = checkbox
    # 5 = select
    
    class Meta:
        verbose_name = _("Questão")
        verbose_name_plural = _("Questões")

    def __str__(self):
        return str(self.titulo)

class Area(models.Model):
    area = models.TextField()
    
    class Meta:
        verbose_name = _("Área")
        verbose_name_plural = _("Áreas")

    def natural_key(self):
        return self.area

    def __str__(self):
        return str(self.area)

class Local(models.Model):
    local = models.TextField()
    
    class Meta:
        verbose_name = _("Local")
        verbose_name_plural = _("Locais")

    def natural_key(self):
        return self.local

    def __str__(self):
        return str(self.local)
        
class Status(models.Model):
    status = models.TextField(max_length=40)
    
    class Meta:
        verbose_name = _("Status")
        verbose_name_plural = _("Status")

    def natural_key(self):
        return self.status

    def __str__(self):
        return str(self.status)

class Feedback(models.Model):
    area = models.ForeignKey(Area, on_delete=models.DO_NOTHING, verbose_name="Área")
    local = models.ForeignKey(Local, on_delete=models.DO_NOTHING, verbose_name="Local")
    descricao = models.TextField(max_length=255, null=True, verbose_name="Descrição")
    imagem = models.ImageField(upload_to=image_upload_path, null=True, blank=True, verbose_name="Imagem")
    status = models.ForeignKey(Status, on_delete=models.DO_NOTHING, verbose_name="Status")
    datahora = models.DateTimeField(null=True, auto_now_add=True, verbose_name="Data e Hora")
    quantidade = models.IntegerField(blank=True, null=True, verbose_name="Quantidade")
    # userId = models.ForeignKey(Tabela_Usuario, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = _("Feedback")
        verbose_name_plural = _("Feedbacks")
    
    def __str__(self):
        return self.descricao
    
class Usuario(models.Model):
    nome = models.CharField(max_length=255)
    email = models.CharField(max_length=255)

    class Meta:
        verbose_name = _("Usuário")
        verbose_name_plural = _("Usuários")

    def natural_key(self):
        return self.nome

    def __str__(self):
        return self.nome

class Comentario(models.Model):
    comentario = models.TextField(null=True, verbose_name="Comentário", blank=True)
    imagem = models.ImageField(upload_to='apps/feedback/static/coment/img', null=True, blank=True, verbose_name="Imagem")
    usuario = models.ForeignKey(Usuario, on_delete=models.DO_NOTHING)
    datahora = models.DateTimeField(null=True, auto_now_add=True)
    feedback_id = models.ForeignKey(Feedback, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Comentário")
        verbose_name_plural = _("Comentários")

    def __str__(self):
        return str(self.comentario)