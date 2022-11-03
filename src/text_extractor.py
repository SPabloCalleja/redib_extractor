# -*- coding: utf-8 -*-

import sys

from os import listdir
from os.path import isfile, join


import io





def extract_files(path):
    onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
    
    return onlyfiles    

def get_text(onlyfiles,path):
  text = ''
  for file in onlyfiles:
    f = io.open(join(path,file), mode="r", encoding="utf-8")
    text = text + f.read() + '\n'
  return text





def main(argv):
    path = argv[0]
    output_file = argv[1]
    onlyfiles= extract_files(path)
    text= get_text(onlyfiles,path)

    f = io.open(output_file, mode="w", encoding="utf-8")
    f.write(text)

    

if __name__ == '__main__':
    main(sys.argv[1:])
    