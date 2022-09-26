#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 19 17:12:18 2022

@author: Pablo
"""

from parsr_client import ParsrClient as client
from time import sleep
import re
import logging
from PyPDF2 import PdfWriter, PdfReader
import sys
import os

#!pip install PyPDF2


parsr = client('localhost:3001')

config_file= 'defaultConfig.json'

counter_jobs = 0



def wait_for_process(jobid):
    
    wait= True
    while wait:
        if "markdown" in parsr.get_status(jobid)['server_response']:
            
            wait= False
        else:
            sleep(5)
            

def refine_section(title, text):
    text= text.replace(title,'').strip()
    text = re.sub(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}','',text)
    text= text.strip()
    paragraphs=text.split('\n')
    new_paragraph=[]
    
    
    for p in paragraphs:
        if len(p) < 13:
            continue
        if 'palabras clave' in p.lower():
            continue
        if 'keywords' in p.lower():
            continue
        if 'key words' in p.lower():
            continue
        new_paragraph.append(p)
        
    
    return '\n'.join(new_paragraph).strip()

def split_by_quotes(text):
    
    
    pattern = r'(\*{2}[A-Za-z .:-]+\*{2})'
    l = re.split(pattern, text)
    
    
    cond=False
    head=''
    lis=[]
    for i in l:
        i=i.strip()
        test=i.replace('\n','')
        if test == '':
            continue
        if not i.startswith('*') and cond == False:
            lis.append(i)
            continue
        if not i.startswith('*') and cond== True:
            lis.append(head+' '+i)
            cond=False
            head=''
            continue
        if i.startswith('*') and cond== True:
            head=head+' '+i.replace('*','')
            cond=True
            continue
        if i.startswith('*'):
            head=i.replace('*','')
            cond=True
            
        
    return lis
            
def extract_sections(markdown_text,name,folder):

    txt = re.sub("#+", "#", markdown_text)
    
    segments= txt.split('#')
    
    new_segments=[]
    for n in segments:
        new_segments.extend(split_by_quotes(n))
        
    
    
    for s in new_segments:
        
        
        s= s.strip()
        if len(s) < 15:
            continue
        
        if 'abstract' in s[:15].lower():
            text= refine_section('Abstract',s)
            write_file(os.path.join(folder, name.replace('.pdf','-abstract.txt')),text)
        if 'resumen' in s[:15].lower():
            text= refine_section('Resumen',s)
            write_file(os.path.join(folder, name.replace('.pdf','-resumen.txt')),text)
        if 'summary' in s[:15].lower():
            text= refine_section('Summary',s)
            write_file(os.path.join(folder, name.replace('.pdf','-abstract.txt')),text)


    

def send_doc(file_path,filename):
    
    global counter_jobs

    if counter_jobs > 400:
        parsr = client('localhost:3001')
        counter_jobs=0

    job = parsr.send_document(
        file_path=file_path,
        config_path=config_file,
        document_name=filename,
        wait_till_finished=False,
        save_request_id=True,
        silent=True
    )
    jobid= job['server_response']
    wait_for_process(jobid)
    
    txt= parsr.get_markdown()
    
    counter_jobs = counter_jobs+1
    return txt
    



def create_compressed_pdf(original_file,compressed_file):
     
    infile = PdfReader(original_file, 'rb')
    output = PdfWriter()
    
    for i in range(len(infile.pages) ):
        if i< 2:
            p = infile.getPage(i)
            output.add_page(p)
        else:
            break
    
    with open(compressed_file, 'wb') as f:
        output.write(f)
    




def process_psr_pdf(file_path, filename, output_folder,mode):
    
    
     ## first part: if markdown exists
    mark_file = os.path.join(output_folder, filename.replace('.pdf','-Mark.md'))
    exis = os.path.exists(mark_file)
    
    
    if exis==True and mode == 'light':
        print('Light mode: skipping processing '+filename)
        return
    
    
    
    ## third part: send doc to parsr

    if exis== True and mode !='force':
        logging.info('Markdown file already existis. Skipping parsing: '+filename)
        print('Markdown file already existis. Skipping parsing: '+filename)
        txt= read_file(mark_file)
        
    else:
         ## first part: get only 2 pages
        fout = os.path.join(output_folder, filename.replace('.pdf','_comprissed.pdf'))
        create_compressed_pdf(file_path,fout)
        
        txt = send_doc(fout,filename)
        write_file(mark_file,txt)
        #remove file
        os.remove(fout)
        
    
    
    logging.info('Extracting sections '+filename)
    print('Extracting sections '+filename)
    extract_sections(txt,filename,output_folder)
        
    
   
    
    
    
    
    
  
    
    





def convert_folder(folder_name,output_folder,mode):

    # dirs=directories
    for (root, dirs, files) in os.walk(folder_name):
        for f in files:
            
            if  f.endswith('.pdf' ):
                logging.info('processing:'+f)
                print('processing:'+f)
                try:
                    #path=    '/Users/Pablo/Downloads/REDIB_SML/training_tips.tei.xml' 
                    filepath = os.path.join(root, f)
                    process_psr_pdf(filepath,f,output_folder,mode)
                   
                    
                except  Exception as e:
                    logging.error('Error in: '+f+' '+str(e))
                    print('Error in: '+f+str(e))
                    
                


import io
def write_file(name,content):

    with io.open(name,'w',encoding='utf8') as f:
        f.write(content)
        
def read_file(name):

    with io.open(name,'r',encoding='utf8') as f:
        return f.read()



def main(argv):
    input_folder = argv[0]
    output_folder = argv[1]
    if len(argv) >2:
        mode = argv[2]
    else:
        mode='normal'
    
    logging.basicConfig(filename='parsr_extractot.log', level=logging.INFO)
    logging.info('Started')
    convert_folder(input_folder,output_folder,mode)
    logging.info('Finished')

if __name__ == '__main__':
    main(sys.argv[1:])
    
    


'''
pattern = r'(\*{2}[A-Za-z .:]+\*{2})'
l = re.split(pattern, s)
l
'''