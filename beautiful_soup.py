#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 10 21:38:56 2017

@author: ronaldo
"""

from bs4 import BeautifulSoup as soup

import requests

file = 'sei.txt'

with open(file, 'r', encoding='utf8') as f:
            
    sei = soup(f, "lxml")
    
    print(type(sei))
    
processos = sei("tr", {"class":'infraTrClara'})


#Investigar o contador superior para saber quantas paginas há
page_counter = sei.find(id = 'selRecebidosPaginacaoSuperior').contents


# get the total number of pages and ignore trailing characters
pages = max([int(p.string) for p in page_counter if p.string != '\n'])




tables = sei.find_all('tr')

  
anchors = sei.find_all('a')
    
links = [link.get('href') for link in anchors]
    

