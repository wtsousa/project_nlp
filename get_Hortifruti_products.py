# -*- coding: utf-8 -*-
"""
Created on Sun Mar  7 14:59:49 2021

@author: Will
"""

import pandas as pd
import requests
import json
import time
import random
from scrapy import Selector

##### GENERAL FUNCTIONS ####

def find_between(s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return "Deu Ruim find_between"

urls = ['https://delivery.hortifruti.com.br/produtos/hortifruti-flamengo/setores/carnes-aves-e-peixes/bovinas/',
        'https://delivery.hortifruti.com.br/produtos/hortifruti-flamengo/setores/carnes-aves-e-peixes/suinas/',
        'https://delivery.hortifruti.com.br/produtos/hortifruti-flamengo/setores/carnes-aves-e-peixes/aves/',
        'https://delivery.hortifruti.com.br/produtos/hortifruti-flamengo/setores/carnes-aves-e-peixes/peixes-e-frutos-do-mar/',
        'https://delivery.hortifruti.com.br/produtos/hortifruti-flamengo/setores/carnes-aves-e-peixes/exoticas-e-especiais/',
        'https://delivery.hortifruti.com.br/produtos/hortifruti-flamengo/setores/carnes-aves-e-peixes/paes-alho/',
        'https://delivery.hortifruti.com.br/produtos/hortifruti-flamengo/setores/happy-hour-natural-da-terra/',
        'https://delivery.hortifruti.com.br/produtos/hortifruti-flamengo/setores/mercearia/alimentos-basicos/',
        'https://delivery.hortifruti.com.br/produtos/hortifruti-flamengo/setores/mercearia/hersheys/',
        'https://delivery.hortifruti.com.br/produtos/hortifruti-flamengo/setores/mercearia/lacta-em-casa/',
        'https://delivery.hortifruti.com.br/produtos/hortifruti-flamengo/setores/mercearia/cafes-e-chas/',
        'https://delivery.hortifruti.com.br/produtos/hortifruti-flamengo/setores/mercearia/massas-e-molhos/',
        'https://delivery.hortifruti.com.br/produtos/hortifruti-flamengo/setores/mercearia/conservas-e-enlatados/',
        'https://delivery.hortifruti.com.br/produtos/hortifruti-flamengo/setores/mercearia/temperos-e-condimentos/',
        'https://delivery.hortifruti.com.br/produtos/hortifruti-flamengo/setores/mercearia/doces-e-sobremesas/',
        'https://delivery.hortifruti.com.br/produtos/hortifruti-flamengo/setores/mercearia/barra-de-cereais/',
        'https://delivery.hortifruti.com.br/produtos/hortifruti-flamengo/setores/mercearia/nuts-snacks-natural-da-terra/',
        'https://delivery.hortifruti.com.br/produtos/hortifruti-flamengo/setores/mercearia/biscoitos-e-salgadinhos/',
        'https://delivery.hortifruti.com.br/produtos/hortifruti-flamengo/setores/mercearia/sementes-nozes-frutas-secas/',       
        'https://delivery.hortifruti.com.br/produtos/hortifruti-flamengo/setores/mercearia/cereais-graos-farinhas-funcionais/',
        'https://delivery.hortifruti.com.br/produtos/hortifruti-flamengo/setores/mercearia/suplementos/',
        'https://delivery.hortifruti.com.br/produtos/hortifruti-flamengo/setores/mercearia/familia-gallo/',
        'https://delivery.hortifruti.com.br/produtos/hortifruti-flamengo/setores/mercearia/promocao-pepsico/',
        'https://delivery.hortifruti.com.br/produtos/hortifruti-flamengo/setores/mercearia/mundo-das-delicias/',
        'https://delivery.hortifruti.com.br/produtos/hortifruti-flamengo/setores/mercearia/nissin/',
        'https://delivery.hortifruti.com.br/produtos/hortifruti-flamengo/setores/dia-das-mulheres-natural-da-terra/',
        'https://delivery.hortifruti.com.br/produtos/hortifruti-flamengo/setores/semana-leve-tudo-hortifruti/',
        'https://delivery.hortifruti.com.br/produtos/hortifruti-flamengo/setores/organicos-natural-da-terra/hortifruti-organicos-natural-da-terra/',
        'https://delivery.hortifruti.com.br/produtos/hortifruti-flamengo/setores/organicos-natural-da-terra/padaria-organicos-natural-da-terra/',
        'https://delivery.hortifruti.com.br/produtos/hortifruti-flamengo/setores/organicos-natural-da-terra/mercearia-organicos-natural-da-terra/',
        'https://delivery.hortifruti.com.br/produtos/hortifruti-flamengo/setores/organicos-natural-da-terra/bebidas-organicos-natural-da-terra/',
        'https://delivery.hortifruti.com.br/produtos/hortifruti-flamengo/setores/organicos-natural-da-terra/acougue-peixaria-organicos-natural-da-terra/',
        'https://delivery.hortifruti.com.br/produtos/hortifruti-flamengo/setores/verao-natural-da-terra/',
        'https://delivery.hortifruti.com.br/produtos/hortifruti-flamengo/setores/piquenique-natural-da-terra/',
        'https://delivery.hortifruti.com.br/produtos/hortifruti-flamengo/setores/produtos-sadia/',
        'https://delivery.hortifruti.com.br/produtos/hortifruti-flamengo/setores/pascoa/conservas-e-enlatados/',
        'https://delivery.hortifruti.com.br/produtos/hortifruti-flamengo/setores/pascoa/temperos-e-condimentos/',
        'https://delivery.hortifruti.com.br/produtos/hortifruti-flamengo/setores/pascoa/doces-e-sobremesas/',
        'https://delivery.hortifruti.com.br/produtos/hortifruti-flamengo/setores/pascoa/ovos-de-pascoa/',
        'https://delivery.hortifruti.com.br/produtos/hortifruti-flamengo/setores/pascoa/chocolate/',
        'https://delivery.hortifruti.com.br/produtos/hortifruti-flamengo/setores/pascoa/colomba-pascal-pascoa/',
        'https://delivery.hortifruti.com.br/produtos/hortifruti-flamengo/setores/pascoa/destilados/',
        'https://delivery.hortifruti.com.br/produtos/hortifruti-flamengo/setores/pascoa/peixes-e-frutos-do-mar/',
        'https://delivery.hortifruti.com.br/produtos/hortifruti-flamengo/setores/pascoa/vinhos-e-espumantes/',
        'https://delivery.hortifruti.com.br/produtos/hortifruti-flamengo/setores/pascoa/geleias-cremes/',
        'https://delivery.hortifruti.com.br/produtos/hortifruti-flamengo/setores/pascoa/doces-padaria/',
        'https://delivery.hortifruti.com.br/produtos/hortifruti-flamengo/setores/pascoa/mundo-das-delicias/',
        'https://delivery.hortifruti.com.br/produtos/hortifruti-flamengo/setores/hortifruti/ta-na-safra-natural-da-terra/',
        'https://delivery.hortifruti.com.br/produtos/hortifruti-flamengo/setores/hortifruti/prontinho-pra-você-natural-da-terra/',
        'https://delivery.hortifruti.com.br/produtos/hortifruti-flamengo/setores/hortifruti/saladas-natural-da-terra/',
        'https://delivery.hortifruti.com.br/produtos/hortifruti-flamengo/setores/hortifruti/frutas/',
        'https://delivery.hortifruti.com.br/produtos/hortifruti-flamengo/setores/hortifruti/legumes/',
        'https://delivery.hortifruti.com.br/produtos/hortifruti-flamengo/setores/hortifruti/pronto-para-consumo/',
        'https://delivery.hortifruti.com.br/produtos/hortifruti-flamengo/setores/hortifruti/verduras/',
        'https://delivery.hortifruti.com.br/produtos/hortifruti-flamengo/setores/hortifruti/temperos-frescos/',
        'https://delivery.hortifruti.com.br/produtos/hortifruti-flamengo/setores/hortifruti/ovos/',
        'https://delivery.hortifruti.com.br/produtos/hortifruti-flamengo/setores/hortifruti/mais-hortifruti/',
        'https://delivery.hortifruti.com.br/produtos/hortifruti-flamengo/setores/padaria-e-confeitaria/padaria-fabricacao-propria/',
        'https://delivery.hortifruti.com.br/produtos/hortifruti-flamengo/setores/padaria-e-confeitaria/paes/',
        'https://delivery.hortifruti.com.br/produtos/hortifruti-flamengo/setores/padaria-e-confeitaria/torradas-cruttons/',
        'https://delivery.hortifruti.com.br/produtos/hortifruti-flamengo/setores/padaria-e-confeitaria/geleias-cremes/',
        'https://delivery.hortifruti.com.br/produtos/hortifruti-flamengo/setores/padaria-e-confeitaria/matinais/',
        'https://delivery.hortifruti.com.br/produtos/hortifruti-flamengo/setores/padaria-e-confeitaria/bolos/',
        'https://delivery.hortifruti.com.br/produtos/hortifruti-flamengo/setores/padaria-e-confeitaria/doces-padaria/',
        'https://delivery.hortifruti.com.br/produtos/hortifruti-flamengo/setores/frios-e-laticinios/fatiados-e-aperitivos/',
        'https://delivery.hortifruti.com.br/produtos/hortifruti-flamengo/setores/frios-e-laticinios/embutidos-finos/',
        'https://delivery.hortifruti.com.br/produtos/hortifruti-flamengo/setores/frios-e-laticinios/frios-e-embutidos/',
        'https://delivery.hortifruti.com.br/produtos/hortifruti-flamengo/setores/frios-e-laticinios/queijos/',
        'https://delivery.hortifruti.com.br/produtos/hortifruti-flamengo/setores/frios-e-laticinios/fondue-queijo/',
        'https://delivery.hortifruti.com.br/produtos/hortifruti-flamengo/setores/frios-e-laticinios/vigor/',
        'https://delivery.hortifruti.com.br/produtos/hortifruti-flamengo/setores/frios-e-laticinios/saudaveis/',
        'https://delivery.hortifruti.com.br/produtos/hortifruti-flamengo/setores/lacteos/danone/',
        'https://delivery.hortifruti.com.br/produtos/hortifruti-flamengo/setores/lacteos/iogurtes-e-coalhadas/',
        'https://delivery.hortifruti.com.br/produtos/hortifruti-flamengo/setores/lacteos/requeijao/',
        'https://delivery.hortifruti.com.br/produtos/hortifruti-flamengo/setores/lacteos/cream-cheese/',
        'https://delivery.hortifruti.com.br/produtos/hortifruti-flamengo/setores/lacteos/sobremesas-lacteas/',
        'https://delivery.hortifruti.com.br/produtos/hortifruti-flamengo/setores/lacteos/margarinas-e-manteigas/',
        'https://delivery.hortifruti.com.br/produtos/hortifruti-flamengo/setores/lacteos/outros-lacteos/',
        'https://delivery.hortifruti.com.br/produtos/hortifruti-flamengo/setores/lacteos/vigor/',
        'https://delivery.hortifruti.com.br/produtos/hortifruti-flamengo/setores/lacteos/saudaveis/',
        'https://delivery.hortifruti.com.br/produtos/hortifruti-flamengo/setores/bebidas/sucos-refrescos-e-refrigerantes/',
        'https://delivery.hortifruti.com.br/produtos/hortifruti-flamengo/setores/bebidas/agua-energeticos-e-chas/',
        'https://delivery.hortifruti.com.br/produtos/hortifruti-flamengo/setores/bebidas/bebidas-natural-da-terra/',
        'https://delivery.hortifruti.com.br/produtos/hortifruti-flamengo/setores/bebidas/leites-e-correlatos/',
        'https://delivery.hortifruti.com.br/produtos/hortifruti-flamengo/setores/bebidas/cervejas/',
        'https://delivery.hortifruti.com.br/produtos/hortifruti-flamengo/setores/bebidas/destilados/',
        'https://delivery.hortifruti.com.br/produtos/hortifruti-flamengo/setores/bebidas/whisky/',
        'https://delivery.hortifruti.com.br/produtos/hortifruti-flamengo/setores/bebidas/vinhos-e-espumantes/',
        'https://delivery.hortifruti.com.br/produtos/hortifruti-flamengo/setores/bebidas/kit-vinhos/',
        'https://delivery.hortifruti.com.br/produtos/hortifruti-flamengo/setores/congelados/sorvetes-sucos-e-sobremesas/',
        'https://delivery.hortifruti.com.br/produtos/hortifruti-flamengo/setores/congelados/petiscos-e-empanados/',
        'https://delivery.hortifruti.com.br/produtos/hortifruti-flamengo/setores/congelados/pratos-prontos/',
        'https://delivery.hortifruti.com.br/produtos/hortifruti-flamengo/setores/congelados/hamburguer/',
        'https://delivery.hortifruti.com.br/produtos/hortifruti-flamengo/setores/congelados/legumes-congelados/',
        'https://delivery.hortifruti.com.br/produtos/hortifruti-flamengo/setores/congelados/frutas-congeladas/',
        'https://delivery.hortifruti.com.br/produtos/hortifruti-flamengo/setores/congelados/paes-congelados/',
        'https://delivery.hortifruti.com.br/produtos/hortifruti-flamengo/setores/limpeza/uso-geral/',
        'https://delivery.hortifruti.com.br/produtos/hortifruti-flamengo/setores/limpeza/roupas/',
        'https://delivery.hortifruti.com.br/produtos/hortifruti-flamengo/setores/limpeza/cozinha/',
        'https://delivery.hortifruti.com.br/produtos/hortifruti-flamengo/setores/limpeza/banheiro/',
        'https://delivery.hortifruti.com.br/produtos/hortifruti-flamengo/setores/higiene-e-beleza/produtos-johnson-and-johnson/',
        'https://delivery.hortifruti.com.br/produtos/hortifruti-flamengo/setores/higiene-e-beleza/higiene/',
        'https://delivery.hortifruti.com.br/produtos/hortifruti-flamengo/setores/higiene-e-beleza/corpo/',
        'https://delivery.hortifruti.com.br/produtos/hortifruti-flamengo/setores/higiene-e-beleza/cabelos/',
        'https://delivery.hortifruti.com.br/produtos/hortifruti-flamengo/setores/higiene-e-beleza/johnson-and-johnson/',
        'https://delivery.hortifruti.com.br/produtos/hortifruti-flamengo/setores/utilidades-domesticas/filme-pvc-sacos-plasticos/',
        'https://delivery.hortifruti.com.br/produtos/hortifruti-flamengo/setores/utilidades-domesticas/guardanapo-toalha-de-papel/',
        'https://delivery.hortifruti.com.br/produtos/hortifruti-flamengo/setores/utilidades-domesticas/papel-aluminio-papel-manteiga/',
        'https://delivery.hortifruti.com.br/produtos/hortifruti-flamengo/setores/utilidades-domesticas/filtro-cafe/',
        'https://delivery.hortifruti.com.br/produtos/hortifruti-flamengo/setores/utilidades-domesticas/fosforos-acendedores/',
        'https://delivery.hortifruti.com.br/produtos/hortifruti-flamengo/setores/utilidades-domesticas/outros-utilidades-domesticas/',
        'https://delivery.hortifruti.com.br/produtos/hortifruti-flamengo/setores/utilidades-domesticas/descartaveis-festas/',
        'https://delivery.hortifruti.com.br/produtos/hortifruti-flamengo/setores/utilidades-domesticas/carvao-e-lenha/',
        'https://delivery.hortifruti.com.br/produtos/hortifruti-flamengo/setores/bebe/',
        ]

#Initializing DataFrame
df_columns = ['product_id', 'brand', 'category_id', 'category_name', 'category_slug',
              'image_thumbnail', 'in_stock', 'name', 'price', 'slug', 'unit_amount',
              'unit_label', 'sector_id', 'sector_name', 'sector_slug', 'sector_icon']
DF_H = pd.DataFrame(columns=df_columns)

#Scraping data from website
#url = "https://delivery.hortifruti.com.br/produtos/hortifruti-flamengo/setores/carnes-aves-e-peixes/bovinas"

for url in urls[49:]:
    req = requests.get(url)
    hortifruti_html = req.text
    html_selector = Selector(text=hortifruti_html)
    
    #Read dictionary
    start_str = '<script id="__NEXT_DATA__" type="application/json">'
    end_str = "</script>"
    products_str = find_between(hortifruti_html,start_str,end_str)
    products_dict = json.loads(products_str)['props']['initialState']['products']['categories'][0]
    print(products_dict['name'])
    products_list = products_dict['items']
    
    for product in products_list:
        row_dict = dict.fromkeys(df_columns)
        row_dict['sector_id'] = products_dict['id']
        row_dict['sector_name'] = products_dict['name']
        row_dict['sector_slug'] = products_dict['slug']
        row_dict['sector_icon'] = products_dict['icon']
        for column in df_columns[0:-4]:
            row_dict[column] = product[column]
        DF_H = DF_H.append(row_dict, ignore_index=True)
    
    waittime = 5 + random.randint(1,3)
    print("... waiting {} seconds ...".format(waittime))
    time.sleep(waittime)
    
DF_H.groupby('sector_id').count()

DF_DIR = 'C:\\Users\\Will\\Documents\\Data Science\\Projeto NLP'
DF_CSV = DF_DIR + '\\Hortifruti.csv'
DF_H.to_csv(DF_CSV)

df_columns_short = ['product_id', 'brand', 'image_thumbnail', 'in_stock', 
              'name', 'price', 'slug', 'unit_amount', 'unit_label']

DF_H_short = DF_H[df_columns_short].drop_duplicates()
DF_CSV = DF_DIR + '\\Hortifruti_Short.csv'
DF_H_short.to_csv(DF_CSV)



#####################

DF_DIR = 'C:\\Users\\Will\\Documents\\Data Science\\Projeto NLP'
DF_CSV = DF_DIR + '\\Receitas_Produtos.csv'
DF_REC = pd.read_csv(DF_CSV, index_col=None, header=0)
DF_REC.drop('Unnamed: 0',axis=1, inplace=True)

from fuzzywuzzy import process, fuzz

for product in DF_REC.PRD.sort_values().unique()[:-1]:
    str2Match = product
    strOptions = DF_H_short.name.values
    print(product.upper())
    #Ratios = process.extract(str2Match,strOptions, scorer=fuzz.token_set_ratio)
    #print(Ratios)
    best_issuers = process.extractBests(str2Match, strOptions, 
                                        score_cutoff=80, 
                                        limit=20,
                                        scorer=fuzz.token_set_ratio)
    print(best_issuers)
    # You can also select the string with the highest matching percentage
    highest = process.extractOne(str2Match,strOptions, scorer=fuzz.token_set_ratio)
    print(highest, '\n')
