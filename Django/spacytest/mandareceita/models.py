from django.db import models
from django.utils import timezone

import datetime

# Create your models here.

class Receita(models.Model):
    receita_title = models.CharField(max_length=400, default='')
    receita_text = models.TextField(max_length=4000, default='')
    receita_completa = models.BooleanField(default=False)
    
    def __str__(self):
        return self.receita_title

    # def was_published_recently(self):
    #     return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

class Ingrediente(models.Model):
    receita = models.ForeignKey(Receita, on_delete=models.CASCADE)
    ingrediente_text = models.TextField(max_length=400)
    ingrediente_entities = models.CharField(max_length=500, blank=True, default='')
    quantidade = models.FloatField(default=-1)
    quantidade_text = models.CharField(max_length=200, default='-1')
    medida_text = models.CharField(max_length=200, blank=True, default='')
    produto_text = models.CharField(max_length=200, blank=True, default='') 
    complemento_text = models.CharField(max_length=200, blank=True, default='') 
    #votes = models.IntegerField(default=0)
    
    def __str__(self):
        return self.ingrediente_text
    
