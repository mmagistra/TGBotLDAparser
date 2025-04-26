import os
import shutil
from bs4 import BeautifulSoup
import requests
import re


# Проверка на ссылку и на доступ
def _is_url(url: str):  # return (bool, 'massage')
    try:
        page = requests.get(url)
        status = page.status_code
        if status == requests.codes.ok:
            return 'done'
        raise Exception(f'status_code = {status}')
    except Exception as expt:
        return str(expt)


# Проверка, что сайт - wiki/cyberleninka
def _is_web(url: str) -> str:
    for domain in ['wikipedia', 'cyberleninka.ru']:
        if domain in url:
            return 'done'
    return 'Wrong site. I was expecting "wikipedia" or "cyberleninka.ru"'


# Парсинг
def _parsing(url: str) -> BeautifulSoup:
    page = requests.get(url)
    return BeautifulSoup(page.text, 'lxml')


# Запись текста в файл
def _writing(url: str, soup: BeautifulSoup, path: str) -> str:  # return path
    try:
        if 'wiki' in url:
            soups = soup.find('div', class_='mw-content-ltr mw-parser-output').find_all('p')
        else:
            soups = soup.find('div', class_='ocr').find_all('p')
    except:
        return 'the parser was unable to find the text'

    try:
        with open(path, 'w', encoding='utf-8') as f:
            for paragraph in soups:
                f.write(paragraph.text)
    except Exception as expt:
        return str(expt)
    return 'done'


# main функция
def _parser(url, file_name) -> tuple:  # return (status, path/massage)
    # Проверка на передачу ссылки
    if not url:
        return 'error', 'nothing was handed over'

    # Очистка ссылки от лишних пробелов и добавление http://
    url = url.strip().strip('/')
    if not url.startswith('http'):
        url = 'http://' + url

    # Проверка на подходящий сайт wiki/cyberleninka
    status_web = _is_web(url)
    if status_web != 'done':
        return 'error', status_web

    # Проверка на ссылку и на доступ к сайту
    status_url = _is_url(url)
    if status_url != 'done':
        return 'error', status_url

    # Парсинг
    soup = _parsing(url)

    # Добавить к названию файла .txt
    if not file_name.endswith('.txt'):
        file_name += '.txt'

    # Создание директории
    folder_name = url.split('/')[-1]  # Название статьи
    path = os.path.join('texts', folder_name)
    os.makedirs(path, exist_ok=True)  # Создание директории
    file_path = os.path.join(path, file_name)  # Добавление имя файла к пути

    # Запись в файл
    status_writing = _writing(url, soup, file_path)

    # Проверка статуса записи
    if status_writing != 'done':
        shutil.rmtree(path)  # Удаление папки с файлом
        return 'error', status_writing

    return 'done', file_path


def parser(url: str = '', file_name: str = 'default.txt') -> tuple:
    """
        Загружает и сохраняет все текста с указанного веб-сайта.

        Функция выполняет парсинг веб-страницы по переданной ссылке (`url`), извлекает
        весь текс и сохраняет его локально. Возвращает статус выполнения и сообщение.

        :param url: URL веб-страницы, с которой необходимо загрузить изображения.
        :param file_name: Имя текстового файла, в который необходимо сохранить текст. По умолчанию default.txt

        :return: Кортеж (status, path/message), где:
            - status (str):
                * 'done' — парсинг и сохранение изображений выполнены успешно.
                * 'error' — возникла критическая ошибка, загрузка не удалась.
            - path (str):
                * Путь к файлу — куда был сохранен текст страницы.
            - message (str):
                * Текст ошибки — если возникла ошибка.
        """
    return _parser(url, file_name)


# Все сохраняется по пути texts/[НАЗВАНИЕ_САЙТА]/file.txt
if __name__ == '__main__':
    # Пример с ожидаемой успешной работой функции
    address = 'https://ru.wikipedia.org/wiki/Буква'
    print(parser(address))
    # output: ('done', 'texts\\Буква\\default.txt')

    # # Пример с передачей желаемого имени файла
    # address = 'https://cyberleninka.ru/article/n/ugolovnyy-kodeks-finlyandii-1889-g-kak-zakonodatelnyy-istochnik-evropeyskoy-integratsii/'
    # print(parser(address, 'file_1'))
    # # output: ('done', 'texts\\ugolovnyy-kodeks-finlyandii-1889-g-kak-zakonodatelnyy-istochnik-evropeyskoy-integratsii\\file_1.txt')

    # # Пример ошибки_1 (если сайт не wikipedia и не cyberleninka)
    # address = 'https://NONAME_SITE'
    # print(parser(address))
    # # output: ('error', 'Wrong site. I was expecting "wikipedia" or "cyberleninka.ru"')

    # # Пример ошибки_2 (нет доступа к сайту)
    # address = 'https://ru.wikipedia.org/wik404/Буква'
    # print(parser(address))
    # # output: ('error', 'status_code = 404')
