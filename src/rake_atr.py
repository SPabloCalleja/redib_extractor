# -*- coding: utf-8 -*-

import sys
import io
from multi_rake import Rake

#!pip install multi-rake -q



def read_text(path):
    f = io.open(path, mode="r", encoding="utf-8")
    text = f.read()
    return text






def main(argv):
    file_text = argv[0]
    output_file = argv[1]
    text= read_text(file_text)


    rake = Rake(
        min_chars=2,
        max_words=7,
        min_freq=3,
        language_code='es',  # 'en'
        #stopwords=None,  # {'and', 'of'}
        #lang_detect_threshold=50,
        #max_words_unknown_lang=2,
        #generated_stopwords_percentile=80,
        #generated_stopwords_max_len=3,
        #generated_stopwords_min_freq=2,
    )

    keywords = rake.apply(text)

    f = io.open(output_file, mode="w", encoding="utf-8")
    f = io.open('myrake-res.txt', mode="w", encoding="utf-8")
    for k in keywords[:1000]:
      f.write(str(k[0])+'\t'+str(k[1])+'\n')

    

if __name__ == '__main__':
    main(sys.argv[1:])
    