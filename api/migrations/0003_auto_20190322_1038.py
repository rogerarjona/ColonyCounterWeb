# Generated by Django 2.1.5 on 2019-03-22 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20190321_2124'),
    ]

    operations = [
        migrations.AddField(
            model_name='colonyproyect',
            name='descripcion',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='colonyproyect',
            name='url_imagen',
            field=models.URLField(null=True),
        ),
    ]
