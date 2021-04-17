# Generated by Django 2.2.6 on 2021-04-12 20:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='slug',
            field=models.SlugField(help_text='Укажите ключ для страницы задачи. Используйте только латиницу, цифры, дефисы и знаки подчёркивания', unique=True, verbose_name='ключ для построения урла'),
        ),
        migrations.AlterField(
            model_name='post',
            name='group',
            field=models.ForeignKey(blank=True, help_text='Можете выбрать группу', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='posts', to='posts.Group', verbose_name='группы'),
        ),
        migrations.AlterField(
            model_name='post',
            name='text',
            field=models.TextField(help_text='Здесь Ваш текст', verbose_name='текст'),
        ),
    ]