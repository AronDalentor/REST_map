from nltk.tokenize import RegexpTokenizer
from nltk.util import ngrams
import re, math
from nltk import ngrams
import re, math
from collections import Counter as c

def get_cosine(text1, text2):
    
    token1 = list([''.join(x) for x in list(ngrams((text1.lower()), 1))])+list([''.join(x) for x in list(ngrams((text1.lower()), 3))])+list([''.join(x) for x in list(ngrams((text1.lower()), 2))])
    token2 = list([''.join(x) for x in list(ngrams((text2.lower()), 1))])+list([''.join(x) for x in list(ngrams((text2.lower()), 3))])+list([''.join(x) for x in list(ngrams((text2.lower()), 2))])
    
    vec1 = {}
    vec2 = {}
     
    for x in token1:
        if x in vec1.keys():
            vec1[x]=vec1[x]+1
        else:
            vec1[x] = 1
    for x in token2:
        if x in vec2.keys():
            vec2[x]=vec2[x]+1
        else:
            vec2[x] = 1

    intersection = set(vec1.keys()) & set(vec2.keys())

    numerator = sum([vec1[x] * vec2[x] for x in intersection])

    sum1 = sum([vec1[x]**2 for x in vec1.keys()])
    sum2 = sum([vec2[x]**2 for x in vec2.keys()])
    denominator = math.sqrt(sum1) * math.sqrt(sum2)

    if not denominator:
        return 0.0
    else:
        return float(numerator) / denominator
# подготовка текста
def text_preprocessing(input_text):
    
    input_text = input_text.replace("-",' ')
    input_text = input_text.replace("/",'')

    if 'г/хл' in input_text:
        input_text = input_text.replace('г/хл','гидрохлорид')
    if 'h' in input_text:
        input_text = translit(input_text,'h')
    if 'x' in input_text:
        input_text = translit(input_text,'x')
    if 'l' in input_text:
        input_text = translit(input_text,'l')
    if 'c' in input_text:
        input_text = translit(input_text,'c')

    if 'таб' in input_text:
        if 'таб' in input_text.split()[0]:
            result = input_text.replace(',','')
            result = result.split()
            return ''.join(result[:4])
        else:
            result = re.search(r'(.*таб)', input_text)
    else:
        result = re.search(r'(.*тбл)|(.*тб)|(.*табл)|(.+\,)', input_text)
    try:
        result = re.sub(r'тбл|,|тб|табл','', result.group())
        if len(result)>1:
            return(result)
        else:
            return(result[0])
    except AttributeError:
        return(input_text)
# замена некоторых латинских букв русскими
def translit(string, letter):
    
    translit = {
        'h': 'н',
        'b': 'б',
        'x': 'х',
        'l': 'л',
        'o': 'о',
        'c': 'с'
    }
    translit_text = string.replace(letter, translit[letter])
    return translit_text
# поиск наиболее совпадающих
def lek_sred_name_search(raw_text, medicine_tr_n):
    
    raw_text = text_preprocessing(raw_text.lower())
    test = raw_text.split()
    #print(raw_text)
    if len(test) > 1 and len(test[1]) > 2:
        medicine_tr_test = search_similar_in_text_2(test[0],test[1][:4], medicine_tr_n)
        if len(medicine_tr_test) < 1:
            medicine_tr_test = search_similar_in_text_2(test[0][:4],test[1][:4], medicine_tr_n)
            if len(medicine_tr_test) < 1:
                medicine_tr_test = search_similar_in_text(test[0][:4],medicine_tr_n)
                if len(medicine_tr_test) < 1:
                    pass
            else:
                medicine_tr_n = medicine_tr_test
        else:
            medicine_tr_n = medicine_tr_test   
    else:
        medicine_tr_test = search_similar_in_text(test[0][:6],medicine_tr_n)
        if len(medicine_tr_test) < 1:
            pass
        else:
            medicine_tr_n = medicine_tr_test
    
    raw_text = raw_text.replace(" ","")
    # проверка наличия латинских букв
    
    new_data = []
    new_data.append(raw_text)
    total_res = {}
    
    for preproc_n_gramm in new_data:
        result = {} 
    
        #print('Preproc_n_gram', preproc_n_gramm)
        
        for text in medicine_tr_n:
            text_modifyed = text.lower()

            # делим текст с которым собираемся выполнять сверку по токенам
            text_modifyed = text_modifyed.replace("-",'')
            text_modifyed = text_modifyed.replace(" ","")
            text_modifyed = text_modifyed.replace('"','')
            text_modifyed = text_modifyed.replace('«','')
            text_modifyed = text_modifyed.replace('»','')
            if 'o' in text_modifyed:
                text_modifyed = translit(text_modifyed,'o')
            if 'h' in text_modifyed:
                text_modifyed = translit(text_modifyed,'h')
            if 'b' in text_modifyed:
                text_modifyed = translit(text_modifyed,'b')
            if 'l' in text_modifyed:
                text_modifyed = translit(text_modifyed,'l')
            if 'c' in text_modifyed:
                text_modifyed = translit(text_modifyed,'c')
            
            #print(text)
            
            # в результат записываем оригинальное значение но для подсчета сходимости используем усеченную версию
            result[text] = get_cosine(text_modifyed, preproc_n_gramm)
        #print(result)
        try:
            max_value = max(result.values())
            final_dict = {k:v for k, v in result.items() if v == max_value}
            for k,v in final_dict.items():
                total_res[k] = v
        except ValueError:
            return 'no_data'
    #print(total_res)
    try:
        max_result_from_total_res = max(total_res.values())
        if max_result_from_total_res <0.1:
            return 'no_data'
        else:
            final_dict = [k for k, v in total_res.items() if v == max_result_from_total_res]
            return final_dict[0]
    except ValueError:
        return 'no_data'
# проверка включений в тексты части слов
def search_similar_in_text(text_fragment, medicine_tr_n):
    res = []
    for x in medicine_tr_n:
        if text_fragment.lower() in x.lower():
            res.append(x)
    return res

def search_similar_in_text_2(text_fragment1,text_fragment2, medicine_tr_n):
    res = []
    for x in medicine_tr_n:
        if text_fragment1.lower() in x.lower() and text_fragment2.lower() in x.lower():
            res.append(x)
    return res

#import pandas as pd
#medicine_tr_n = pd.read_csv('data/DATA_FOR_MAPPING_old.csv')
#medicine_tr_n = pd.read_csv('data/DATA_FOR_MAPPING.csv')
#medicine_tr_n = medicine_tr_n.TRADE_NAME_RU.unique()
#print(lek_sred_name_search('атенолол тбл 100мг №30',medicine_tr_n))

#print(search_similar_in_text('слив',medicine_tr_n))
#print(search_similar_in_text_2('канд','б6'))
#print('Энап-H'.lower())
#print(text_preprocessing("табекс, тбл п/п/о 1.5мг №100"))
