import os
import colorlog
import sys
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler


def set_logger(logger, config):
    """
    Задает настройки логирования
    """    
    # ************************** форматирование ************************************************************
    FORMATTER_EMAIL = logging.Formatter("[%(asctime)s] %(name)s(%(funcName)s)"
                                        "[LINE:%(lineno)d]: %(levelname)-8s:  %(message)s",
                                        datefmt='%d/%m/%Y %H:%M:%S')
    # для выделения цветом сообщений в консоле
    FORMATTER_CONSOLE = colorlog.ColoredFormatter('%(log_color)s%(name)s(%(funcName)s)[LINE:%(lineno)d]: %(levelname)-8s:  '
                                                '%(message)s',
                                                datefmt='%d/%m/%Y %H:%M:%S',
                                                log_colors={'DEBUG': 'white', 'INFO': 'green',
                                                            'WARNING': 'bold_yellow', 'ERROR': 'bold_red',
                                                            'CRITICAL': 'bold_red'})
    
    # переопределили класс, чтобы убрать пробелы и перевод строки из сообщения
    class CustomFormatter(logging.Formatter):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def format(self, record):
            record.msg = record.msg.strip().replace('\n', ', ')
            return super().format(record)

    # форматирование для записи в файл
    FORMATTER_FILE = CustomFormatter("[%(asctime)s] %(name)s(%(funcName)s)[LINE:%(lineno)d]: "
                                "%(levelname)-8s:  %(message)s",
                                datefmt='%d/%m/%Y %H:%M:%S')
    
    # ***************************** handlers *********************************************************
    def console_handler():
        """
        Запись в консоль
        Сообщения с уровня DEBUG и выше пишем в консоль
        """
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(FORMATTER_CONSOLE)
        console_handler.setLevel(logging.DEBUG)  # здесь можно изменить с какого уровня ошибки выводить в консоль
        return console_handler
    
    def info_file_handler():
        """
        Запись логов в файл
        Сообщения с уровня INFO и выше пишем в файл info.log
        DEBUG игнорируем
        """
        if not os.path.exists('logs'):
            os.mkdir('logs')
            
        file_handler = RotatingFileHandler('logs/info.log', 
                                           maxBytes=10485760, # 10485760 = 10мб
                                           backupCount=10,  # храним 10 файлов с историей
                                           encoding="utf8" # кодировка логов utf8
                                           )            
        file_handler.setFormatter(FORMATTER_FILE)
        file_handler.setLevel(logging.INFO)  # здесь можно изменить с какого уровня ошибки выводить в файл
        return file_handler
    
    def error_file_handler():
        """
        Запись логов в файл
        Сообщения с уровня ERROR и выше пишем в файл errors.log
        DEBUG, INFO, WARNING игнорируем
        """
        
        if not os.path.exists('logs'):
            os.mkdir('logs')
            
        file_handler = RotatingFileHandler('logs/errors.log', 
                                           maxBytes=10485760, # 10485760 = 10мб
                                           backupCount=10,  # храним 10 файлов с историей
                                           encoding="utf8" # кодировка логов utf8
                                           )            
        file_handler.setFormatter(FORMATTER_FILE)
        file_handler.setLevel(logging.ERROR)  # здесь можно изменить с какого уровня ошибки выводить в файл
        return file_handler

    def email_handler():
            """
            Запись логов в файл
            Сообщения с уровня ERROR и выше пишем в файл errors.log
            DEBUG, INFO, WARNING игнорируем
            """            
            # Отправка сообщения на почту админу
            if config['MAIL_SERVER']:
                # отправка писем админам
                auth = None
                if config['MAIL_USERNAME'] or config['MAIL_PASSWORD']:
                    auth = (config['MAIL_USERNAME'], config['MAIL_PASSWORD'])
                
                mail_handler = SMTPHandler(mailhost=config['MAIL_SERVER'], 
                                        fromaddr=config['ADMIN'], # от кого
                                        toaddrs=config['ADMIN'], # кому
                                        subject='Ошибка в Flask_parser', # Заголовок 
                                        credentials=auth, 
                                        secure=())
                mail_handler.setFormatter(FORMATTER_EMAIL)
                mail_handler.setLevel(logging.CRITICAL)
                return mail_handler
            
    # ********************* установка Handler с настройками ***********************************
    logger.setLevel(logging.DEBUG)
    
    logger.addHandler(console_handler())
    logger.addHandler(info_file_handler())    
    logger.addHandler(error_file_handler())      
    logger.addHandler(email_handler())  
    
    return None