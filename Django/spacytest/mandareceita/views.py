from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.views import generic
from django.http import Http404
from django.utils import timezone

from .models import Receita, Ingrediente

from ast import literal_eval
import pickle
import re

# Create your views here.

def index(request):
    #Carrega todas as receitas
    receita_list = Receita.objects.all()
    #Coloca as receitas como argumento de contexto
    context = {'receita_list': receita_list}
    #Renderiza contexto de acordo com o template 'mandareceita/index.html'
    return render(request, 'mandareceita/index.html', context)

def results(request, receita_id):
    receita = get_object_or_404(Receita, pk=receita_id)
    context =  {'receita': receita}
    return render(request, 'mandareceita/results.html', context)

def detail(request, receita_id):
     receita = get_object_or_404(Receita, pk=receita_id)
     context =  {'receita': receita}
     return render(request, 'mandareceita/detail.html', context)

class IndexView(generic.ListView):
    template_name = 'mandareceita/index.html'
    context_object_name = 'receita_list'

    def get_queryset(self):
        return Receita.objects.all()
        
class DetailView(generic.DetailView):
    model = Receita
    template_name = 'mandareceita/detail.html'    
    
class ResultsView(generic.DetailView):
    model = Receita
    template_name = 'mandareceita/results.html'
    
class EditIngredientView(generic.DetailView):
    model = Ingrediente
    template_name = 'mandareceita/edit_ingredient.html'
    
def add_receita(request):
    context = {}
    #Renderiza contexto de acordo com o template '.html'
    return render(request, 'mandareceita/add_receita.html', context)

def pre_process_ingrediente(ingrediente_text):
    words = ingrediente_text.lower().split()
    text_list = []
    
    #New patterns
    #pattern = re.compile("^([A-Z][0-9]+)+$")
    only_digits_pattern = re.compile("\d+")
    g_pattern = re.compile("\d+g$")
    kg_pattern = re.compile("\d+kg$")
    l_pattern = re.compile("\d+l$")
    ml_pattern = re.compile("\d+ml$")
    
    for word in words:
        if (g_pattern.search(word) != None):
            digits_text = only_digits_pattern.match(word).group()
            text_list.append(digits_text)
            text_list.append("g")
        elif (kg_pattern.search(word) != None):
            digits_text = only_digits_pattern.match(word).group()
            text_list.append(digits_text)
            text_list.append("kg")
        elif (l_pattern.search(word) != None):
            digits_text = only_digits_pattern.match(word).group()
            text_list.append(digits_text)
            text_list.append("l")
        elif (ml_pattern.search(word) != None):
            digits_text = only_digits_pattern.match(word).group()
            text_list.append(digits_text)
            text_list.append("ml")            
        else:
            text_list.append(word)
            
    new_ingredient_text = ' '.join(text_list)
    return new_ingredient_text

def add_ingrediente(request):
    receita_title = request.POST['receita_title']
    receita_text = request.POST['receita_text']
    receita = Receita(receita_title = receita_title, receita_text = receita_text)
    receita.save()
    ingredientes_list = receita_text.splitlines()
    #print(ingredientes_list)
    for ingrediente_text in ingredientes_list:
        if (ingrediente_text != ''):
            ingrediente_text = pre_process_ingrediente(ingrediente_text)
            ingrediente = Ingrediente(receita = receita, ingrediente_text = ingrediente_text)
            ingrediente.save()
    context = {}
    #Renderiza contexto de acordo com o template '.html'
    return render(request, 'mandareceita/add_receita.html', context)
    
def vote(request, receita_id):
    receita = get_object_or_404(Receita, pk=receita_id)
    try:
        selected_ingrediente = receita.ingrediente_set.get(pk=request.POST['ingrediente'])
    except (KeyError, Ingrediente.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'mandareceita/detail.html', {
            'receita': receita,
            'error_message': "You didn't select a Ingrediente.",
        })
    else:
        #selected_ingrediente.votes += 1
        receita.receita_completa = True
        receita.save()
        selected_ingrediente.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('mandareceita:results', args=(receita.id,)))
    
def edit_ingredient(request, receita_id):
    receita = get_object_or_404(Receita, pk=receita_id)
    #print(f"Recebi: {request.POST['ingrediente']}")
    try:
        selected_ingrediente = receita.ingrediente_set.get(pk=request.POST['ingrediente'])
    except (KeyError, Ingrediente.DoesNotExist):
        # Redisplay the question voting form.
        print("Deu ruim")
        return render(request, 'mandareceita/detail.html', {
            'receita': receita,
            'error_message': "Você não selecionou um ingrediente.",
        })
    else:
        #selected_ingrediente.votes += 1
        #selected_ingrediente.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        #return HttpResponseRedirect(reverse('mandareceita:edit_ingredient', args=(selected_ingrediente.id,)))
        context =  {'ingrediente': selected_ingrediente}
        return render(request, 'mandareceita/edit_ingredient.html', context)
    
def add_entity(request, ingrediente_id):
    ingrediente = get_object_or_404(Ingrediente, pk=ingrediente_id)
    qtd_words = request.POST.getlist('qtd_checked_words []')
    med_words = request.POST.getlist('med_checked_words []')
    prd_words = request.POST.getlist('prd_checked_words []')
    cmp_words = request.POST.getlist('cmp_checked_words []')
    print(f"QTD: {qtd_words}")
    print(f"MED: {med_words}")
    print(f"PRD: {prd_words}")
    print(f"CMP: {cmp_words}")
    entities_list = []
    ingrediente_text = ingrediente.ingrediente_text
    ingrediente.quantidade_text = ' '.join(qtd_words)
    ingrediente.medida_text = ' '.join(med_words)
    ingrediente.produto_text = ' '.join(prd_words)
    ingrediente.complemento_text = ' '.join(cmp_words)
    if (len(qtd_words) != 0): entities_list.append(create_entity_tuple(ingrediente_text,qtd_words,'QTD'))
    if (len(med_words) != 0): entities_list.append(create_entity_tuple(ingrediente_text,med_words,'MED'))
    if (len(prd_words) != 0): entities_list.append(create_entity_tuple(ingrediente_text,prd_words,'PRD'))
    if (len(cmp_words) != 0): entities_list.append(create_entity_tuple(ingrediente_text,cmp_words,'CMP'))
    ingrediente.ingrediente_entities = (ingrediente_text,{'entities':entities_list})
    ingrediente.save()
    #return HttpResponseRedirect(reverse('mandareceita:edit_ingredient', args=(ingrediente.receita.id,)))
    return HttpResponseRedirect(reverse('mandareceita:results', args=(ingrediente.receita.id,)))

def create_entity_tuple(ingrediente_text,entity_list,category):
    if (len(entity_list) != 0):
        entity_text = ' '.join(entity_list)
        start_pos = ingrediente_text.find(entity_text)
        end_pos = start_pos + len(entity_text)
        return start_pos, end_pos, category
    else:
        print("No " + category)
        return None

def save_training_data(request):
    #get all ingredients into a list
    #save list as file
    ingredientes_list = Ingrediente.objects.all()
    training_data = []
    for ingrediente in ingredientes_list:
        entities = ingrediente.ingrediente_entities
        if (len(entities)!= 0):
            training_data.append(literal_eval(ingrediente.ingrediente_entities))
    #print(training_data)
    with open('C:\\Users\\Will\\Documents\\Data Science\\Projeto NLP\\training.data', 'wb') as filehandle:
        pickle.dump(training_data, filehandle)
    with open('C:\\Users\\Will\\Documents\\Data Science\\Projeto NLP\\training.data', 'rb') as filehandle:
        training_data = pickle.load(filehandle)
    #print(training_data)
    
    #Save Test Data
    test_data = []
    for ingrediente in ingredientes_list:
        ingrediente_text = ingrediente.ingrediente_text
        entities = ingrediente.ingrediente_entities
        if ((len(ingrediente_text)!= 0) & (len(entities)== 0)):
            test_data.append(ingrediente_text)
    with open('C:\\Users\\Will\\Documents\\Data Science\\Projeto NLP\\test.data', 'wb') as filehandle:
        pickle.dump(test_data, filehandle)
    with open('C:\\Users\\Will\\Documents\\Data Science\\Projeto NLP\\test.data', 'rb') as filehandle:
        test_data = pickle.load(filehandle)
    print(test_data)
    
    return HttpResponseRedirect(reverse('mandareceita:index'))
    