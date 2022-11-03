#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  3 09:30:47 2022

@author: Pablo
"""
import sys
import io

#!pip install pyate -q
#!python -m spacy download es_core_news_sm -q

import spacy
from pyate.term_extraction_pipeline import TermExtractionPipeline

def read_text(path):
    f = io.open(path, mode="r", encoding="utf-8")
    text = f.read()
    return text






def main(argv):
    file_text = argv[0]
    output_file = argv[1]
    text= read_text(file_text)

    
    
    nlp = spacy.load("es_core_news_sm")
    nlp.max_length=50000000
    nlp.add_pipe("combo_basic")
    doc = nlp(text)

    var = doc._.combo_basic.sort_values(ascending=False).head(1000)

    f = io.open(output_file, mode="w", encoding="utf-8")
    for k in var.items():
      f.write(str(k[0])+'\t'+str(k[1])+'\n')

    

if __name__ == '__main__':
    main(sys.argv[1:])
    