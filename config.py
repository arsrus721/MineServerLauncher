config_file = 'conf.data'

def read_config(key):
    with open(config_file, 'r', encoding='utf-8') as file:
        for line in file:
            if '=' in line:
                k, value = line.strip().split('=', 1)
                if k.strip().strip('"') == key:
                    return value.strip().strip('"')  # Возвращает значение для указанного ключа
    return None  # Возвращает None, если ключ не найден

def write_config(key, value):
    config = {}
    
    # Считываем существующие параметры
    try:
        with open(config_file, 'r', encoding='utf-8') as file:
            for line in file:
                if '=' in line:
                    k, v = line.strip().split('=', 1)
                    config[k.strip().strip('"')] = v.strip().strip('"')
    except FileNotFoundError:
        pass  # Если файл не найден, создадим новый

    # Обновляем или добавляем новый параметр
    config[key] = value

    # Записываем все параметры обратно в файл
    with open(config_file, 'w', encoding='utf-8') as file:
        for k, v in config.items():
            file.write(f'"{k}"="{v}"\n')

# Пример использования

# Запись параметра
#write_config('Имя', 'Значение')

# Получение параметра
#value = read_config(config_file, 'Имя')