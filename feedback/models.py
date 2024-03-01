from django.db import models
from django.utils.translation import gettext_lazy as _

class questionario(models.Model):
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
    
class tipo(models.Model):
    tipo_opcoes = [
        ('Resposta Curta', 'Resposta Curta'),
        ('Resposta Longa', 'Resposta Longa'),
        ('Única Escolha', 'Única Escolha'),
        ('Várias Escolhas', 'Várias Escolhas'),
        ('Dropdown', 'Dropdown'),
    ]
    tipo = models.CharField(max_length=50, choices=tipo_opcoes, unique=True)

    class Meta:
        verbose_name = _("Tipo")
        verbose_name_plural = _("Tipos")

    def __str__(self):
        return self.tipo

class questao(models.Model):
    titulo = models.TextField(null=True, verbose_name="Nome")
    tipo = models.ForeignKey(tipo, on_delete=models.DO_NOTHING)
    questionario_id = models.ForeignKey(questionario, on_delete=models.DO_NOTHING)
    area = models.BooleanField(default=False, unique=False)
    local = models.BooleanField(default=False, unique=False)
    # tipo, se a questão tem como resposta texto, multiplas respostas, seleção única, ou caixa de seleção
    # 1 = area
    # 2 = textarea
    # 3 = radio
    # 4 = checkbox
    # 5 = select
    
    class Meta:
        verbose_name = _("Questão")
        verbose_name_plural = _("Questões")

    def __str__(self):
        return str(self.titulo)

class area(models.Model):
    area = models.CharField(max_length=20)
    
    class Meta:
        verbose_name = _("Área")
        verbose_name_plural = _("Áreas")

    def __str__(self):
        return str(self.area)

class local(models.Model):
    local = models.CharField(max_length=50)
    
    class Meta:
        verbose_name = _("Local")
        verbose_name_plural = _("Locais")

    def __str__(self):
        return str(self.local)
        
class status(models.Model):
    status = models.CharField(max_length=20)
    
    class Meta:
        verbose_name = _("Status")
        verbose_name_plural = _("Status")

    def __str__(self):
        return str(self.status)

class feedback(models.Model):
    titulo = models.CharField(max_length=255, null=True, verbose_name="Título")
    area = models.ForeignKey(area, on_delete=models.DO_NOTHING)
    local = models.ForeignKey(local, on_delete=models.DO_NOTHING)
    descricao = models.TextField(max_length=255, null=True)
    status = models.ForeignKey(status, on_delete=models.DO_NOTHING)
    datahora = models.DateTimeField(null=True, auto_now_add=True)
    # userId = models.ForeignKey(Tabela_Usuario, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = _("Feedback")
        verbose_name_plural = _("Feedbacks")
    
    def __str__(self):
        return self.titulo


class usuario(models.Model):
    nome = models.CharField(max_length=255)
    email = models.CharField(max_length=255)

    class Meta:
        verbose_name = _("Usuário")
        verbose_name_plural = _("Usuários")

    def __str__(self):
        return self.nome

class comentario(models.Model):
    comentario = models.TextField(null=True, verbose_name="Comentário")
    usuario = models.ForeignKey(usuario, on_delete=models.DO_NOTHING)
    datahora = models.DateTimeField(null=True, auto_now_add=True)
    feedback_id = models.ForeignKey(feedback, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Comentário")
        verbose_name_plural = _("Comentários")

    def __str__(self):
        return str(self.comentario)