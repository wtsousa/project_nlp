# -*- coding: utf-8 -*-
"""
Created on Mon Feb 22 12:06:04 2021

@author: Will
"""

from django.urls import path

from . import views

app_name = 'mandareceita'

urlpatterns = [
    #path('', views.index, name='index'),
    #path('<int:receita_id>/', views.detail, name='detail'),
    #path('<int:receita_id>/results/', views.results, name='results'),
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:receita_id>/vote/', views.vote, name='vote'),
    path('<int:receita_id>/edit_ingredient/', views.edit_ingredient, name='edit_ingredient'),
    path('<int:ingrediente_id>/add_entity/', views.add_entity, name='add_entity'),
    path('add_receita/', views.add_receita, name='add_receita'),
    path('add_ingrediente/', views.add_ingrediente, name='add_ingrediente'),
    path('save_training_data/', views.save_training_data, name='save_training_data'),
]