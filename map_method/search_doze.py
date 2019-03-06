import re


# функция удаления пустых элементов списка
def check_no_space(matches):
    raw_matches_no_space = []
    for match in matches:
        for item in match:
            if len(item) > 0:
                raw_matches_no_space.append(item)
    return(raw_matches_no_space)

# функция проверки строки без цифр
def check_no_value(raw_matches_no_space):
    res = []
    for item in raw_matches_no_space:
        if item == 'мкг' or item == 'мг' or item == 'г':
            continue
        else:
            res.append(item)
    return res

# функция проверки наличия обозначения размерностей
# если размерность не указана - то к значению добавлется мг
def check_no_number(list_of_no_spaces):
    #print(list_of_no_spaces)
    res = []
    for match in list_of_no_spaces:
        regex = r"[А-Яа-я]"
        result = re.search(regex, match)
        if result == None:
            match = match.replace(',','.')
            try:
                if float(match) > 0 and float(match) < 1:
                    res.append(str(int(float(match)*1000))+'мг')
                else:
                    res.append(match+'мг')
            except:
                return res
        else:
            res.append(match)
    
    return res
# конвертирует г в мг
def convertation(result):
    num_regex = r"([0-9][.,][0-9])"
    num = re.search(num_regex, result)
    num = num.group(0)
    if ',' in num: 
        num = num.replace(',','.')
    
    num = int(float(num)*1000)
    text = 'мг'
    
    return [str(num)+text]

def search_concentration_tablet(text):
    
    try:
        regex = r"(\d+\s+(мкг|мг|г))|(\d[,.]\d(мкг|мг|г)\d)|(\d[,.]\d\s)|(\d+[.,]\d+(мкг|мг|г))|(\d+(мкг|мг|г))|(\d+\+\d+(мг))|(\d+\+\d+)"

        raw_matches = re.findall(regex, text)
        #print("Чистый парсинг  ", raw_matches)

        # удаляем пустые строки и делаем единый список
        raw_matches_no_space = check_no_space(raw_matches)
        #print("Удаленные пустые элементы ",raw_matches_no_space)

        # удаляем обозначения размерности без цифр
        raw_no_space_no_units = check_no_value(raw_matches_no_space)
        #print('Удаленные единицы без размерности ', raw_no_space_no_units)

        if '+' in raw_no_space_no_units[0]:
        #если запись сложная - ее необходимо разделить пр: ['250+125мг'] => ['250', '125мг']
        #тогда можно будет дописать размерность

            # нолевой элемент берется потому что нужно извлечь значение из списка
            raw_no_space_no_units = raw_no_space_no_units[0].split('+')
            #print("Проверка на отсутствие размероности и добавление таковой ", raw_no_space_no_units)

        # проверка нет ли в строке мг и мкг, если есть - нужно оставить только мкг
        test = ''.join(raw_no_space_no_units)

        if 'мг' in test and 'мкг' in test:
            raw_no_space_no_units = [x for x in raw_no_space_no_units if "мкг" in x]
        if 'г' in test and ',' in test or '.' in test:
            number_regex  = r"([0-9][,.][0-9])"
            number = re.match(number_regex, test)
            try:
                number = number.group().replace(',','.')
                if float(number) > 1:
                    raw_no_space_no_units = [str(number)+'мг']
                else:
                    raw_no_space_no_units = convertation(test)
            except AttributeError:
                raw_no_space_no_units

        # ставим размерность, если пропущена
        raw_result = check_no_number(raw_no_space_no_units)

        # объеденяем писок
        raw_result = '+'.join(raw_result)
    
        # удаляем пробелы и заменяем запятые на точки
        result = raw_result.replace(' ','')
        result = result.replace(',','.')
        
        return result
    
    except IndexError:
        return 'no_data'