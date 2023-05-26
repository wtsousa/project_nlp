# Generated by Django 3.1.2 on 2021-03-03 18:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mandareceita', '0004_auto_20210303_1345'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ingrediente',
            old_name='medida',
            new_name='medida_text',
        ),
        migrations.AddField(
            model_name='ingrediente',
            name='produto_text',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AddField(
            model_name='ingrediente',
            name='quantidade_text',
            field=models.CharField(default='1', max_length=200),
        ),
        migrations.AddField(
            model_name='receita',
            name='receita_title',
            field=models.CharField(default='Sem Nome', max_length=400),
        ),
        migrations.AlterField(
            model_name='ingrediente',
            name='ingrediente_text',
            field=models.TextField(max_length=400),
        ),
        migrations.AlterField(
            model_name='ingrediente',
            name='quantidade',
            field=models.FloatField(default=1),
        ),
        migrations.AlterField(
            model_name='receita',
            name='receita_text',
            field=models.TextField(default='Sem Descrição', max_length=4000),
        ),
    ]