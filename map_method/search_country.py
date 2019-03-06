country_dict = { 
                 'Словения': 'Республика Словения',
                 'Россия': 'Российская Федерация',
                 'Германия': 'Федеративная Республика Германия',
                 'Франция': 'Французская Республика',
                 'Великобритания': 'Соединенное Королевство Великобритании и Северной Ирландии',
                 'Индия': 'Республика Индия',
                 'Латвия': 'Латвийская Республика',
                 'Италия': 'Итальянская Республика',
                 'Австрия': 'Австрийская Республика',
                 'Беларусь': 'Республика Беларусь',
                 'Сербия': 'Республика Сербия',
                 'Бельгия': 'Королевство Бельгии',
                 'Македония': 'Республика Македония',
                 'Израиль': 'Государство Израиль',
                 'Испания': 'Королевство Испания',
                 'Хорватия': 'Республика Хорватия',
                 'Польша': 'Республика Польша',
                 'Швеция': 'Королевство Швеция',
                 'Украина': 'Украина',
                 'Венгрия': 'Венгрия',
                 'Болгария': 'Республика Болгария',
                 'Мальта': 'Республика Мальта',
                 'Армения': 'Республика Армения',
                 'США': 'Соединенные Штаты Америки',
                 'Румыния': 'Румыния',
                 'Эстония': 'Эстонская Республика',
                 'Словакия': 'Словацкая Республика',
                 'Дания': 'Королевство Дания',
                 'Вьетнам': 'Социалистическая Республика Вьетнам',
                 'Турция': 'Турецкая Республика',
                 'Китай': 'Китайская Народная Республика',
                 'Швейцария': 'Швейцарская Конфедерация',
                 'Нидерланды': 'Королевство Нидерландов',
                 'Мексика': 'Мексиканские Соединенные Штаты',
                 'Босния и Герцеговина': 'Босния и Герцеговина',
                 'Аргентина': 'Аргентинская Республика',
                 'Канада': 'Канада',
                 'Ирландия': 'Ирландия',
                 'Югославия': 'Югославия',
                 'Молдавия': 'Республика Молдова',
                 'Казахстан': 'Республика Казахстан',
                 'Чешская Республика': 'Чешская Республика',
                 'Словацкая республика': 'Словацкая Республика',
                 'Исландия': 'Республика Исландия',
                 'Пакистан': 'Исламская Республика Пакистан',
                 'Япония': 'Япония',
                 'Греция': 'Греческая Республика',
                 'Финляндия': 'Финляндская Республика',
                 'Австралия': 'Австралия',
                 'Португалия': 'Португальская Республика',
                 'Норвегия': 'Королевство Норвегия',
                 'Египет': 'Арабская Республика Египет',
                 'Пуэрто-Рико': 'Пуэрто-Рико',
                 'Литва': 'Литовская Республика',
                 'Грузия': 'Грузия',
                 'Черногория': 'Черногория',
                 'Индонезия': 'Республика Индонезия',
                 'Иордания': 'Иорданское Хашимитское Королевство',
                 'Саудовская Аравия': 'Королевство Саудовская Аравия',
                 'Корея': 'Республика Корея',
                 'Таиланд': 'Королевство Таиланд',
                 'Сербия и Черногория': 'Сербия и Черногория',
                 'Сингапур': 'Республика Сингапур',
                 'Россия/Сербия': ['Российская Федерация','Республика Сербия'],
                 'Швеция-Германия': ['Королевство Швеция','Федеративная Республика Германия'],
                 'Россия-Словения': ['Российская Федерация','Республика Словения'],
                 'Греция-Хорватия': ['Греческая Республика','Республика Хорватия'],
                 'Франция-Италия': ['Французская Республика','Итальянская Республика'],
                 'Венгрия-Румыния': ['Венгрия','Румыния'],
                 'Франция-Германия': ['Французская Республика','Федеративная Республика Германия'],
                 'Испания-Германия': ['Королевство Испания','Федеративная Республика Германия'],
                 'Россия-Франция': ['Российская Федерация','Французская Республика'],
                 'Монако': "?",
                 'Португалия-Венгрия': ['Португальская Республика','Венгрия'],
                 'Россия-Македония': ['Российская Федерация','Республика Македония'],
                 'Пуэрто-Рико-Германия': ['Пуэрто-Рико','Федеративная Республика Германия'],
                 'Россия-Индия': ['Российская Федерация','Республика Индия'],
                 'Венгрия-Россия': ['Венгрия','Российская Федерация'],
                 'Великобритания-Нидерланды': ['Соединенное Королевство Великобритании и Северной Ирландии','Королевство Нидерландов'],
                 'Нидерланды-Дания': ['Королевство Нидерландов','Королевство Дания'],
                 'Израиль-Венгрия': ['Государство Израиль','Венгрия'],
                 'США/Италия': ['Соединенные Штаты Америки','Итальянская Республика'],
                 'Пуэрто-Рико-Испания': ['Пуэрто-Рико','Королевство Испания'],
                 'Россия-Швейцария': ['Российская Федерация','Швейцарская Конфедерация'],
                 'Россия-Корея': ['Российская Федерация','Республика Корея'],
                 'Германия-Италия': ['Федеративная Республика Германия','Итальянская Республика'],

}

def search_country(country):
    try:
        return country_dict[country]
    except KeyError:
        return 'no_data'
