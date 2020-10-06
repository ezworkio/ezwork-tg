import configparser


def get_config():
    # Считываем учетные данные
    config = configparser.ConfigParser()
    config.read("config.ini")

    # Присваиваем значения внутренним переменным
    api_id = config['Telegram']['api_id']
    api_hash = config['Telegram']['api_hash']

    return api_id, api_hash
