# Generated by Django 2.2.6 on 2021-04-20 09:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0007_auto_20210419_0006'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ('-pub_date',), 'verbose_name': 'пост', 'verbose_name_plural': 'Посты'},
        ),
    ]