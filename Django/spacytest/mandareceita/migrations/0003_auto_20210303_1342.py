# Generated by Django 3.1.2 on 2021-03-03 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mandareceita', '0002_ingrediente_votes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingrediente',
            name='medida',
            field=models.CharField(max_length=200, null=True),
        ),
    ]