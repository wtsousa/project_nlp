# Generated by Django 3.1.2 on 2021-03-04 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mandareceita', '0007_auto_20210304_1051'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ingrediente',
            name='votes',
        ),
        migrations.AddField(
            model_name='ingrediente',
            name='complemento_text',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
    ]
