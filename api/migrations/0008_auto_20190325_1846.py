# Generated by Django 2.1.5 on 2019-03-25 23:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_photocolony_total'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photocolony',
            name='created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
