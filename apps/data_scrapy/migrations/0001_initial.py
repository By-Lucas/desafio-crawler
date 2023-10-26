# Generated by Django 4.2.6 on 2023-10-26 18:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ScrapyQuotesModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('modified_date', models.DateTimeField(auto_now=True, verbose_name='Modificado em')),
                ('is_active', models.BooleanField(default=True, verbose_name='Ativo')),
                ('title', models.TextField(blank=True, null=True, verbose_name='Título')),
                ('author', models.CharField(blank=True, max_length=150, null=True, verbose_name='Autor')),
                ('born', models.CharField(blank=True, max_length=150, null=True, verbose_name='Nascimento')),
                ('location', models.CharField(blank=True, max_length=200, null=True, verbose_name='Localidade')),
                ('tags', models.CharField(blank=True, max_length=1000, null=True, verbose_name='Autor')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Descrição')),
            ],
            options={
                'verbose_name': 'Scrapy Quotes',
                'verbose_name_plural': 'Scrapy Quotes',
            },
        ),
    ]
