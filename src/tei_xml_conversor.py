#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 16 12:30:43 2022

@author: Pablo
"""

#for beautifulsoup
#!pip install beautifulsoup4

#for lmxl parser
#!pip install lxml


#####


import json
from bs4 import BeautifulSoup 
import logging

import sys

def remove_bib(element):
    for e in element.find_all('ref'):
        e.decompose()
    return element

def remove_figures(element):
    for e in element.find_all('figure'):
        e.decompose()
    return element

def remove_formula(element):
    for e in element.find_all('formula'):
        e.decompose()
    return element







###




def get_sections(element):
    body = element.find('body') 

    secciones = body.find_all('div') 
    
    
    sections=[]
    for sec in secciones:
        sec=remove_formula(sec)
        paragraphs = sec.find_all('p')
        parr_sec=[]
        sect={}
        head = sec.find('head')
        sect['head']=head.text
        for p in paragraphs:
            p= remove_bib(p)
            p= remove_figures(p)
            parr_sec.append(p.text)
        sect['p']=parr_sec
        sections.append(sect)
    return sections

    

def get_authors(element):
    authors={}
    lis_authors=[]
    authors = element.find('teiHeader').find_all('persName') 
    for a in authors:
        name = a.find('forename')
        surname= a.find('surname')
        if name == None:
            name=''
        else:
            name=name.text
        if surname == None:
            surname=''
        else:
            surname=surname.text
        lis_authors.append(name+' '+surname)
    #authors['authors']=lis_authors
    return lis_authors

def get_header(element):
    
    # Finding all instances of tag   
    b_unique = element.find_all('abstract') 
    b_text = b_unique[0].find('div')
    
    abstract= {}
    parr=[]
    paragraphs = b_text.find_all('p')
    for p in paragraphs:
        p = remove_bib(p)
        
        parr.append(p.text)

    return parr
   

def write_json_paper(file,content):
    with open(file, "w", encoding='utf8') as write_file:
        json.dump(content, write_file, indent=4,ensure_ascii=False)
def write_txt_paper(file,content):
    with open(file, "w", encoding='utf8') as write_file:
        for c in content:
            write_file.write(str(c)+'\n')

def create_json_paper(file):
    # Reading the data inside the xml file to a variable under the name  data
    with open(file, 'r') as f:
        data = f.read() 
    
    
    my_json={}
    
    # Passing the stored data inside the beautifulsoup parser 
    bs_data = BeautifulSoup(data, 'xml')
    abst_p={}
    
    try:
        abst_p['p']=get_header(bs_data)
    except Exception as e:
        logging.error('Error creating header '+e)
        raise Exception("Error")
        
    my_json['abstract']=abst_p
    
    
    try: 
        my_json['body']=get_sections(bs_data)
    except Exception as e:
        logging.error('Error creating body '+e)
        raise Exception("Error")
    
    
    try:
        my_json['authors']=get_authors(bs_data)
    except Exception as e:
        logging.error('Error creating authors '+e)
        raise Exception("Error")
    return my_json


def create_txt_paper(file):
    # Reading the data inside the xml file to a variable under the name  data
    with open(file, 'r') as f:
        data = f.read() 
    
    
    my_json=[]
    
    # Passing the stored data inside the beautifulsoup parser 
    bs_data = BeautifulSoup(data, 'xml')
    text_header=''
    
    try:
        text_header=get_header(bs_data)
    except Exception as e:
        logging.error('Error creating header '+e)
        raise Exception("Error")
     
    for p in text_header:
        my_json.append(p)
    
    
    try: 
        data_body=get_sections(bs_data)
        for d in data_body:
            my_json.append(str(d['head']))
            for p in d['p']:
                my_json.append(str(p))

    except Exception as e:
        logging.error('Error creating body '+e)
        raise Exception("Error")
    

    return my_json


import os
def convert_folder_tojson(folder_name,output_folder):

    # dirs=directories
    for (root, dirs, files) in os.walk(folder_name):
        for f in files:
            
            if  f.endswith('.tei.xml' ):
                print(f)
                try:
                    #path=    '/Users/Pablo/Downloads/REDIB_SML/training_tips.tei.xml' 
                    mj= create_json_paper(os.path.join(root, f))
                   
                    write_json_paper(os.path.join(output_folder,f+'.json'),mj)
                except  Exception as e:
                    logging.error('Error in: '+f+' '+str(e))
                    print('Error in: '+f)
                    
                
def convert_folder_totxt(folder_name,output_folder):

    # dirs=directories
    for (root, dirs, files) in os.walk(folder_name):
        for f in files:
            
            if  f.endswith('.tei.xml' ):
                print(f)
                try:
                    #path=    '/Users/Pablo/Downloads/REDIB_SML/training_tips.tei.xml' 
                    mj= create_txt_paper(os.path.join(root, f))
                   
                    write_txt_paper(os.path.join(output_folder,f+'.txt'),mj)
                except  Exception as e:
                    logging.error('Error in: '+f+' '+str(e))
                    print('Error in: '+f)
                    



def main(argv):
    input_folder = argv[0]
    output_folder = argv[1]
    
    logging.basicConfig(filename='tei_xml_conversor.log', level=logging.INFO)
    logging.info('Started')
    convert_folder_totxt(input_folder,output_folder)
    logging.info('Finished')

if __name__ == '__main__':
    main(sys.argv[1:])

