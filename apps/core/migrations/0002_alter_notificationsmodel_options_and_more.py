# Generated by Django 4.2.6 on 2023-10-27 02:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='notificationsmodel',
            options={'verbose_name': 'Notificação', 'verbose_name_plural': 'Notificações'},
        ),
        migrations.AlterField(
            model_name='notificationsmodel',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='Descrição'),
        ),
    ]