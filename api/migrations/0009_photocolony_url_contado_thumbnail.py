# Generated by Django 2.1.5 on 2019-03-27 06:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_auto_20190325_1846'),
    ]

    operations = [
        migrations.AddField(
            model_name='photocolony',
            name='url_contado_thumbnail',
            field=models.URLField(blank=True, null=True),
        ),
    ]
