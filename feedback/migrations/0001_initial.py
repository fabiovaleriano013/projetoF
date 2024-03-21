# Generated by Django 4.2.7 on 2024-03-18 10:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('area', models.TextField()),
            ],
            options={
                'verbose_name': 'Área',
                'verbose_name_plural': 'Áreas',
            },
        ),
        migrations.CreateModel(
            name='Local',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('local', models.TextField()),
            ],
            options={
                'verbose_name': 'Local',
                'verbose_name_plural': 'Locais',
            },
        ),
        migrations.CreateModel(
            name='Questionario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=255, null=True)),
                ('link', models.CharField(max_length=25, null=True)),
                ('link_resposta', models.CharField(max_length=25, null=True)),
            ],
            options={
                'verbose_name': 'Questionário',
                'verbose_name_plural': 'Questionário',
            },
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.TextField(max_length=40)),
            ],
            options={
                'verbose_name': 'Status',
                'verbose_name_plural': 'Status',
            },
        ),
        migrations.CreateModel(
            name='Tipo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(choices=[('Resposta Curta', 'Resposta Curta'), ('Resposta Longa', 'Resposta Longa'), ('Única Escolha', 'Única Escolha'), ('Várias Escolhas', 'Várias Escolhas'), ('Dropdown', 'Dropdown'), ('Imagem', 'Imagem')], max_length=50, unique=True)),
            ],
            options={
                'verbose_name': 'Tipo',
                'verbose_name_plural': 'Tipos',
            },
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=255)),
                ('email', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'Usuário',
                'verbose_name_plural': 'Usuários',
            },
        ),
        migrations.CreateModel(
            name='Questao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.TextField(null=True, verbose_name='Nome')),
                ('area', models.BooleanField(default=False)),
                ('local', models.BooleanField(default=False)),
                ('questionario_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='feedback.questionario')),
                ('tipo', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='feedback.tipo')),
            ],
            options={
                'verbose_name': 'Questão',
                'verbose_name_plural': 'Questões',
            },
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao', models.TextField(max_length=255, null=True, verbose_name='Descrição')),
                ('imagem', models.ImageField(blank=True, null=True, upload_to='apps/feedback/static/img/', verbose_name='Imagem')),
                ('datahora', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Data e Hora')),
                ('area', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='feedback.area', verbose_name='Área')),
                ('local', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='feedback.local', verbose_name='Local')),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='feedback.status', verbose_name='Status')),
            ],
            options={
                'verbose_name': 'Feedback',
                'verbose_name_plural': 'Feedbacks',
            },
        ),
        migrations.CreateModel(
            name='Comentario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comentario', models.TextField(blank=True, null=True, verbose_name='Comentário')),
                ('imagem', models.ImageField(blank=True, null=True, upload_to='apps/feedback/static/coment/img', verbose_name='Imagem')),
                ('datahora', models.DateTimeField(auto_now_add=True, null=True)),
                ('feedback_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='feedback.feedback')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='feedback.usuario')),
            ],
            options={
                'verbose_name': 'Comentário',
                'verbose_name_plural': 'Comentários',
            },
        ),
    ]
