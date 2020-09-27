# Generated by Django 2.0 on 2020-09-27 00:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('confidencechronograms', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comentario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dt_entrada', models.DateTimeField(auto_now=True, verbose_name='Data de Entrada')),
                ('nome_cliente', models.CharField(max_length=30, verbose_name='Nome do cliente')),
                ('assunto', models.CharField(max_length=50, verbose_name='Assunto')),
                ('descricao', models.TextField(verbose_name='Descrição')),
                ('arquivo', models.FileField(blank=True, null=True, upload_to='chamado/arquivos/')),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='cliente', to='confidencechronograms.Cliente')),
                ('funcionario', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='funcionario', to='confidencechronograms.Funcionario')),
            ],
            options={
                'verbose_name': 'Comentário',
                'verbose_name_plural': 'Comentários',
                'ordering': ['dt_entrada'],
            },
        ),
    ]