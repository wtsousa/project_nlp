from django.contrib import admin

# Register your models here.

from .models import Receita, Ingrediente

admin.site.register(Receita)
admin.site.register(Ingrediente)