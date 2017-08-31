#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 18 00:47:22 2017

@author: ronaldo
"""
from string import ascii_letters

from itertools import product, chain

prefix = ["PY2"]

letters = list(ascii_letters[-26:])

letters_no_Q = letters.copy()

letters_no_Q.remove('Q')

suffix = product(letters_no_Q,letters, letters)

indicativos = []

for p in next(suffix):
    print(chain(p))
    
    
