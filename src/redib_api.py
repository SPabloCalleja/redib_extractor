#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 26 15:29:46 2023

@author: Pablo
"""

from redib_elastic import query_term,getLocalConnection

import streamlit as st

# to run this file
#!streamlit run web.py


st.set_page_config(
    page_title="Tesauro de Psicología - REDIB",
    page_icon=":books:",
    layout="wide"
)

st.title("Tesauro de Psicología - REDIB")



#user_input = st.text_input("Put your term here to search", '')
word = st.sidebar.text_input('Introduce la palabra a buscar:')




es = getLocalConnection()  


if word:
    df= query_term(es,'redib_doc',word)
    
    #df = pd.DataFrame(data)
    
    # Visualización de los resultados
    st.write(f'Se han encontrado {len(df)} resultados para "{word}":')
    st.markdown(df.to_html(render_links=True, escape=False), unsafe_allow_html=True)
    #st.dataframe(df)
    #st.dataframe(data= dataframe, use_container_width=False)
else:
    st.write('Introduce una palabra para buscar.')


   
    
    

    


       







