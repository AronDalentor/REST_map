import pandas as pd
import numpy as np
import re, math

from tqdm import tqdm
tqdm.pandas()

import map_method.search_forma as search_forma
import map_method.search_doze as search_doze
import map_method.search_quantity as search_quantity
import map_method.search_trade_name as search_trade_name
import map_method.search_country as search_country
import map_method.search_company as search_company

import warnings
warnings.filterwarnings('ignore')

# функция получения общего количества таблеток во вторичной упаковке
def zero(arg1, arg2):
    if arg2 == 0:
        return arg1
    else:
        return arg1 * arg2

# считывание и подготовка данных элемент
def read_and_preprocess_element_data(route_to_element_db_csv):

    #read_data
    element_db_csv = pd.read_csv(route_to_element_db_csv, index_col=False)
    element_db_csv.reset_index(inplace=True)
    element_db_csv = element_db_csv.drop(['index'],axis=1)

    # Выбираем только таблетки и капсулы
    fil = [x for x in element_db_csv.DRUG_FORM_RU.unique() if x.startswith('таб') or x.startswith('капс')]
    element_db_csv = element_db_csv[element_db_csv['DRUG_FORM_RU'].isin(fil)]

    # preprocessing
    element_db_csv.fillna('0', inplace=True)
    element_db_csv['GNR_DRUG_STRENGTH'] = element_db_csv['GNR_DRUG_STRENGTH'].apply(lambda x: space_remover(x))

    # выбираем препараты со статусом активные
    element_db_csv = element_db_csv[element_db_csv.CERT_STATUS == 'A']

    # Добавим колонку отображающую количество таблеток во вторичной упаковке
    # element_db_csv['AMOUNT_OF_DRUGS_IN_SEC_PACK_TOTAL'] = element_db_csv['Q_TY_IN_PRIM_PACK'].astype('float64') * element_db_csv['AMOUNT_IN_SEC_PACK'].astype('float64')
    element_db_csv['AMOUNT_OF_DRUGS_IN_SEC_PACK_TOTAL'] = element_db_csv.apply(lambda x: zero(int(x['Q_TY_IN_PRIM_PACK']), int(x['AMOUNT_IN_SEC_PACK'])), axis = 1)
    element_db_csv['AMOUNT_OF_DRUGS_IN_SEC_PACK_TOTAL'] = element_db_csv['AMOUNT_OF_DRUGS_IN_SEC_PACK_TOTAL'].astype('object')


    return element_db_csv

# считывание и подготовка данных аптечных справочников
def read_and_preprocess_apt_db(route_to_apt_db):
    #'data/apt_spravochnik_bel.xlsx'

    #read_data
    try:
        apt_db_raw = pd.read_excel(route_to_apt_db, index_col=False)
    except:
        apt_db_raw = pd.read_csv(route_to_apt_db, index_col=False)

    # Выбираем только значимые поля из аптечного справочник
    try:
        apt_db_raw = apt_db_raw[apt_db_raw['Активен'] == 'Да']
    except KeyError:
        pass
    apt_db = apt_db_raw.loc[:,['Название товара','Страна','Фирма - производитель']]
    apt_db.fillna('no_data', inplace=True)
    apt_db['Название товара'] = apt_db['Название товара'].apply(lambda x: x.lower())

    return apt_db

# функция получения торговых наименованиц
def extract_trade_names(element_db):

    # список торговых препаратов
    tr_n = element_db['TRADE_NAME_RU'].unique()

    return tr_n

# Удаляем только пробелы
def space_remover(some_string):
    regex_spaces = r"\s+"
    final = re.sub(regex_spaces,'',some_string)
    return final

# функция фильтрования
def filter_function(data, filter_condition, column_name):
    """
    
    data - for the first iteration use <main_db_filtered>, all next iterations should be filted data bases from previous iterations
    filter_condition - this is vocabulary with parced data from apotheke database
    column_name - select column from main data base to filter the results
    
    """
    #print(filter_condition)

    try :
        new_data = data[data[column_name] == filter_condition]
        return new_data
    except TypeError and ValueError:
        new_data = data[data[column_name].isin(filter_condition)]
        return new_data

# парсинг строки справочника
def parcing_from_data_row(dict_from_data_frame_row, forma, medicine_tr_n):
    """
    dict_from_data_frame_row - строка в формате dict из дата фрейм пандас
    forma_identification  - форма препарата
    """

    if forma == 'таблетки':

        dict_from_data_frame_row['Торговое наименование (парсинг)'] = search_trade_name.lek_sred_name_search(dict_from_data_frame_row['Название товара'], medicine_tr_n)
        try:
            dict_from_data_frame_row['Фирма - производитель (парсинг)'] = search_company.search_company(dict_from_data_frame_row['Фирма - производитель'])
        except KeyError:
            dict_from_data_frame_row['Фирма - производитель (парсинг)'] = 'no_data'
        dict_from_data_frame_row['Дозировка (парсинг)'] = search_doze.search_concentration_tablet(dict_from_data_frame_row['Название товара'])
        dict_from_data_frame_row['Количество таблеток (парсинг)'] = search_quantity.search_quantity_tablet(dict_from_data_frame_row['Название товара'])
        dict_from_data_frame_row['Страна (парсинг)'] = search_country.search_country(dict_from_data_frame_row['Страна'])
        dict_from_data_frame_row['Форма (парсинг)'] = search_forma.tabletka_search(dict_from_data_frame_row['Название товара'])

    elif forma == 'капсулы':

        dict_from_data_frame_row['Торговое наименование (парсинг)'] = search_trade_name.lek_sred_name_search(dict_from_data_frame_row['Название товара'], medicine_tr_n)
        try:
            dict_from_data_frame_row['Фирма - производитель (парсинг)'] = search_company.search_company(dict_from_data_frame_row['Фирма - производитель'])
        except KeyError:
            dict_from_data_frame_row['Фирма - производитель (парсинг)'] = 'no_data'
        dict_from_data_frame_row['Дозировка (парсинг)'] = search_doze.search_concentration_tablet(dict_from_data_frame_row['Название товара'])
        dict_from_data_frame_row['Количество таблеток (парсинг)'] = search_quantity.search_quantity_tablet(dict_from_data_frame_row['Название товара'])
        dict_from_data_frame_row['Страна (парсинг)'] = search_country.search_country(dict_from_data_frame_row['Страна'])
        dict_from_data_frame_row['Форма (парсинг)'] = search_forma.tabletka_search(dict_from_data_frame_row['Название товара'])

    else:

        dict_from_data_frame_row['Торговое наименование (парсинг)'] = search_trade_name.lek_sred_name_search(dict_from_data_frame_row['Название товара'], medicine_tr_n)
        try:
            dict_from_data_frame_row['Фирма - производитель (парсинг)'] = search_company.search_company(dict_from_data_frame_row['Фирма - производитель'])
        except KeyError:
            dict_from_data_frame_row['Фирма - производитель (парсинг)'] = 'no_data'
        dict_from_data_frame_row['Дозировка (парсинг)'] = search_doze.search_concentration_tablet(dict_from_data_frame_row['Название товара'])
        dict_from_data_frame_row['Количество таблеток (парсинг)'] = search_quantity.search_quantity_tablet(dict_from_data_frame_row['Название товара'])
        dict_from_data_frame_row['Страна (парсинг)'] = search_country.search_country(dict_from_data_frame_row['Страна'])
        dict_from_data_frame_row['Форма (парсинг)'] = search_forma.tabletka_search(dict_from_data_frame_row['Название товара'])

    return dict_from_data_frame_row

###
###
###  ОСНОВНОЙ МЕТОД ЗАПУСКА ФУНКЦИИ
###
###
def main_function(filename):
    """
    filename - путь к *.csv файлу аптечного справочника
    """

    main_db = read_and_preprocess_element_data('data/DATA_FOR_MAPPING_v8.csv') # Считываем базы данных #apt_db = read_and_preprocess_apt_db('data/apt_spravochnik_bel.xlsx')
    apt_db = read_and_preprocess_apt_db(filename)
    only_tab_db = apt_db[apt_db['Название товара'].str.contains('капс')] # Выбираем из аптечного справочника только тбл|тб|таблетки|таб|ТАБ

    medicine_tr_n = main_db['TRADE_NAME_RU'].unique() # Список торговых препаратов

    # total_data - Результат маппинга
    # marker_dict - словарь маркеров для отметок результатов поиска результатам поиска
    total_data = {
                'id': [],
                'Название товара':[],
                'Страна': [],
                'Фирма - производитель': [],
                'PD SID': [],
                'Торговое наименование (парсинг)': [],
                'Форма выпуска (парсинг)': [],
                'Доза (парсинг)': [],
                'Страна (парсинг)': [],
                'Количество в первичной упаковке (парсинг)': [],
                'ЕИ для кол-ва в первичной упаковке':[],
                'Первичная упаковка':[],
                'Количество первичных упаковок во вторичной':[],
                'Вторичнаая упаковка':[],
                'Фирма - производитель (парсинг)': [],
                'Общее количество во вторичной упаковке':[],
                }
    marker_dict = {
                    'id':[],
                    'фильтр Дозировка (парсинг)':[],
                    'фильтр Количество таблеток (парсинг)':[],
                    'фильтр Страна (парсинг)':[],
                    'фильтр Фирма - производитель (парсинг)':[],
                    'фильтр Форма (парсинг)':[],
                    'фильтр Торговое наименование (парсинг)':[]
                }

    #apt_med_list - значения аптечного справочник, на которые мы хотим найти кандидаты
    apt_med_list = only_tab_db.iloc[:,:]

    # id_ это порядковый номер из аптечного справочника. Он присваивается во время маппинга, 
    # чтобы можно было состыковать 2 таблицы после маппинга, а также проще было определять 
    # к какой записи аптечного справочника относятся кандидаты
    id_ = 0

    # Цикл построчно считывает аптечный справочник
    for x in tqdm(range(len(apt_med_list))):

        # Изменяй последовательность позиций в словаре для приоритезации в фильтре
        # Генерируется словарь из известных данных
        data = dict(apt_med_list.iloc[x,:])
        forma  = search_forma.forma_identification(data['Название товара'])

        # Значения словаря заполняются с помощью функций парсинга
        data = parcing_from_data_row(data, forma, medicine_tr_n)

        keys_to_check = [ 'Торговое наименование (парсинг)', 'Фирма - производитель (парсинг)',  'Количество таблеток (парсинг)', 'Страна (парсинг)', 'Дозировка (парсинг)', 'Форма (парсинг)']

        # sorting_col_attr - это то, как называется колонка в базе по который мы будем выполнять
        # фильтр по базе МДМ по которым выполнять фильтр

        sorting_col_attr = {
                            'Торговое наименование (парсинг)':'TRADE_NAME_RU',
                            'Фирма - производитель (парсинг)':'ORG_NAME_RU',
                            'Форма (парсинг)':'DRUG_FORM_RU',
                            'Количество таблеток (парсинг)':'AMOUNT_OF_DRUGS_IN_SEC_PACK_TOTAL',
                            'Дозировка (парсинг)':'GNR_DRUG_STRENGTH',
                            'Страна (парсинг)':'COUNTRY_NAME_RU'
        }

        # в dict_with_attr_for_filtering попадают те признаки которые не равны "no_data", тоесть распарсились
        # это сделано для сокращения итераций

        dict_with_attr_for_filtering = {}

        for k,v in data.items():
            if k in keys_to_check:
                dict_with_attr_for_filtering[k] = data[k]

        # это собственно сама база данных, просто создаем копию на которую будем накладывать фильтр
        new_data = main_db.copy()

        #начинаем применять фильтр
        # в dict_with_attr_for_filtering входят те столбци в которых есть запись и входят в список keys_to_check и 
        for k,v in dict_with_attr_for_filtering.items():

                # у таблеток разные формы, случается так, что форма указана не верно
                # есть смысл идти от дочерних форм к родительским и включать в поиск по
                # форме родителю и производным ему формам
                if k == 'Форма (парсинг)':

                    # подставляtv существующие данные
                    check_data = filter_function(data = new_data, filter_condition = v, column_name = sorting_col_attr[k])

                    # применяем модиффицированную функцию маркеров
                    # если кандидаты есть - ставим еденицу в маркер
                    # и переназначаем результат выдачи

                    if len(check_data) != 0:
                        marker_dict['фильтр '+ k].append(1)
                        new_data = check_data

                    # если кандидатов после фильтра нет - берется родитель формы и
                    # осуществляется поиск по родителю и его производным
                    else:

                        # p_n - родитель формы, он переименовывается для того,
                        # чтобы можно было выйти на уровень выше, если фильтр не сработает

                        p_n = search_forma.parent_name_search(v)

                        #  родитель и его производные
                        v = search_forma.parent_name_list_to_provide_search(p_n)


                        check_data = filter_function(data = new_data, filter_condition = v, column_name = sorting_col_attr[k])

                        if len(check_data) != 0:
                            marker_dict['фильтр '+ k].append(1)
                            new_data = check_data

                        # если кандидаты не нашлись

                        else:
                            # идем вверх по родителю
                            p_n = search_forma.parent_name_search(p_n)
                            v = search_forma.parent_name_list_to_provide_search(p_n)

                            if p_n == 'таблетки':

                                check_data = filter_function(data = new_data, filter_condition = v, column_name = sorting_col_attr[k])

                                if len(check_data) != 0:
                                    marker_dict['фильтр '+ k].append(1)
                                    new_data = check_data
                                else:
                                    marker_dict['фильтр '+ k].append(0)

                            else:

                                check_data = filter_function(data = new_data, filter_condition = v, column_name = sorting_col_attr[k])

                                if len(check_data) != 0:
                                    marker_dict['фильтр '+ k].append(1)
                                    new_data = check_data
                                else:
                                    marker_dict['фильтр '+ k].append(0)
                else:
                    # list of candidates after filtering
                    check_data = filter_function(data = new_data, filter_condition = v, column_name = sorting_col_attr[k])

                    # выполняем проверку того, сколько кандидатов осталось
                    # в том числе ставим флаги на против признаков по которым удалось выполнить поиск

                    # ставим 1 если фильтр был выполнен и остались кандидаты
                    if len(check_data) != 0:
                        marker_dict['фильтр '+ k].append(1)
                        new_data = check_data
                    # ставим 0 в если то, что распарсил алгоритм - не дало кандидатов
                    else:
                        marker_dict['фильтр '+ k].append(0)

        # словарь кандидатов после применения фильтра        
        candidates = [v for k,v in dict(new_data.transpose()).items()]

        #print(data)

        for candidate in candidates:
            c = dict(candidate)

            total_data['id'].append(id_)
            total_data['Название товара'].append(data['Название товара']),
            total_data['Страна'].append(data['Страна']),
            total_data['Фирма - производитель'].append(data['Фирма - производитель']),
            total_data['PD SID'].append(c['PACK_CODE'])

            # сумма всех значений для кандидата

            total_data['Торговое наименование (парсинг)'].append(c['TRADE_NAME_RU'])
            total_data['Форма выпуска (парсинг)'].append(c['DRUG_FORM_RU'])
            total_data['Доза (парсинг)'].append(c['GNR_DRUG_STRENGTH'])
            total_data['Страна (парсинг)'].append(c['COUNTRY_NAME_RU'])
            total_data['Количество в первичной упаковке (парсинг)'].append(c['Q_TY_IN_PRIM_PACK'])
            total_data['ЕИ для кол-ва в первичной упаковке'].append(c['MEASURE_UNITS_PRIM_PACK_DRUGS'])
            total_data['Первичная упаковка'].append(c['PRIM_PACK_NAME_RU'])
            total_data['Количество первичных упаковок во вторичной'].append(c['AMOUNT_IN_SEC_PACK'])
            total_data['Вторичнаая упаковка'].append(c['SEC_PACK_NAME_RU'])
            total_data['Фирма - производитель (парсинг)'].append(c['ORG_NAME_RU'])
            total_data['Общее количество во вторичной упаковке'].append(c['AMOUNT_OF_DRUGS_IN_SEC_PACK_TOTAL'])

        id_ += 1

    marker_dict_new = marker_dict

    marker_dict_new['id'] = list(range(0,len(marker_dict_new['фильтр Торговое наименование (парсинг)'])))
    marker_data_frame = pd.DataFrame(marker_dict_new)
    result = pd.DataFrame(total_data)
    total_result = pd.merge(result, marker_data_frame, on=['id', 'id'])

    return total_result