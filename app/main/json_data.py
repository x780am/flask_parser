def get_fields_name():
    fields_name = { "priority": 'Порядок выдачи; ', 
                    "text": 'Описание объявления; ',
                    "header": 'Заголовок объявления; ',
                    "price": 'Цена объявления; ',
                    "url": 'Ссылка на объявление; ',
                    "phone": 'Телефон; ',
                    "phone2": 'Защищенный номер; ',
                    "owner_name": 'Контактное лицо; ',
                    "sex": 'Пол продавца; ',
                    "address": 'Адрес; ',
                    "cat_text": 'Категория, подкатегория; ',
                    "operator": 'Оператор связи, регион оператора; ',
                    "date": 'Дата добавления; ',
                    "nom": 'Номер объявления; ',
                    "image_big": 'Ссылки на изображения; ',
                    "lat": 'Координаты объявления; ',
                    "dop": 'Тип объявления, параметры, категории одной строкой; ',
                    "owner_dop": 'Данные о продавце; ',
                    "commission": 'Комиссия,%; ',
                    "view_all": 'Кол-во просмотров сегодня и за все время; ',
                    "pay_usl": 'Платные услуги, доставка, уменьшение цены; ',
                    }
    return fields_name

def field_name_by_id(fields_id):
    # fields_name = field_name_by_id(fields_id='header,price,url,owner_dop')            
    fields_set = get_fields_name()
                
    fields = fields_id.split(',')
    return_str = ""
    for field in fields:
        if field in fields_set:
            return_str = return_str + fields_set[field]
        else:
            return_str = return_str + field + '; '
        
    return return_str

def get_dopfields_name():
    dopfields_name = {
                      "ads_dubli": 'Только уникальные объявления;',
                      "local_priority": 'Сначала в выбранном городе/радиусе;',
                      "only_new": 'Только новые объявления;',
                      "only_new_phone": 'Только новые телефоны;',
                      "only_with_phone": 'Только объявления с номерами телефонов;',
                      "phone_anonym": 'Не выгружать "защищенные" номера;',
                      "phone_dubli": 'Только уникальные телефоны;',
                      "param_in_col": 'Разбить параметры на столбцы;',
                      "save_tag": 'Сохранять html разметку в описании;',
                      "seller_dubli": 'Только уникальные продавцы;',
    }
    return dopfields_name

def get_order_header_none():
    return "Ваш заказ подготавливается к работе.<br>На данной странице скоро Вы увидите всю информацию по заказу. Обработка платежа занимает около 3 минут. <br>Обновите страницу позже."

def get_order_header_ban():
    return "Ваш аккаунт заблокирован. По всем вопросам обращайтесь в службу поддержки."

if __name__ == "__main__":
    field = 'param_in_col'
        
    