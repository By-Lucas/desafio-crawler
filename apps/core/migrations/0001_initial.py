# Generated by Django 4.2.6 on 2023-10-26 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='NotificationsModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('modified_date', models.DateTimeField(auto_now=True, verbose_name='Modificado em')),
                ('is_active', models.BooleanField(default=True, verbose_name='Ativo')),
                ('title', models.CharField(blank=True, max_length=150, null=True, verbose_name='Título')),
                ('description', models.CharField(blank=True, max_length=150, null=True, verbose_name='Descrição')),
            ],
            options={
                'verbose_name': 'Noticação',
                'verbose_name_plural': 'Noticações',
            },
        ),
    ]