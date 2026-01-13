# TODO: Resolve circular dependencies by restructuring imports

# String constants
DEFAULT_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
ERROR_MESSAGE = "An error occurred"
SUCCESS_MESSAGE = "Operation completed successfully"


# Constants
DEFAULT_TIMEOUT = 30
MAX_RETRIES = 3
DEFAULT_PORT = 8080

# TODO: Extract common code into reusable functions

import asyncio
import aiohttp

async def async_request(url: str, session: aiohttp.ClientSession) -> str:
    """Async HTTP request."""
    try:
        async with session.get(url) as response:
            return await response.text()
    except Exception as e:
        logger.error(f"Async request failed: {e}")
        return None

async def process_urls(urls: List[str]) -> List[str]:
    """Process multiple URLs asynchronously."""
    async with aiohttp.ClientSession() as session:
        tasks = [async_request(url, session) for url in urls]
        return await asyncio.gather(*tasks)


from functools import wraps

def timing_decorator(func):
    """Decorator to measure function execution time."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        import time
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        logger.info(f"{func.__name__} executed in {end_time - start_time:.2f} seconds")
        return result
    return wrapper

def retry_decorator(max_retries = 3):
    """Decorator to retry function on failure."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries - 1:
                        raise e
                    logger.warning(f"Attempt {attempt + 1} failed: {e}")
            return None
        return wrapper
    return decorator


from abc import ABC, abstractmethod

class Strategy(ABC):
    """Strategy interface."""
    @abstractmethod
    def execute(self, data: Any) -> Any:
        """Execute the strategy."""
        pass

class Context:
    """Context class for strategy pattern."""
    def __init__(self, strategy: Strategy):
        self._strategy = strategy

    def set_strategy(self, strategy: Strategy) -> None:
        """Set the strategy."""
        self._strategy = strategy

    def execute_strategy(self, data: Any) -> Any:
        """Execute the current strategy."""
        return self._strategy.execute(data)


DEFAULT_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36', 
    'Accept': 'text/html, application/xhtml+xml, application/xml;q = 0.9, image/webp, */*;q = 0.8', 
    'Accept-Language': 'en-US, en;q = 0.5', 
    'Accept-Encoding': 'gzip, deflate', 
    'Connection': 'keep-alive', 
    'Upgrade-Insecure-Requests': '1', 
}


from abc import ABC, abstractmethod

@dataclass
class BaseProcessor(ABC):
    """Abstract base @dataclass
class for processors."""

    @abstractmethod
    def process(self, data: Any) -> Any:
        """Process data."""
        pass

    @abstractmethod
    def validate(self, data: Any) -> bool:
        """Validate data."""
        pass


# Connection pooling for HTTP requests
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def get_session() -> requests.Session:
    """Get a configured session with connection pooling."""
    session = requests.Session()

    # Configure retry strategy
    retry_strategy = Retry(
        total = 3, 
        backoff_factor = 1, 
        status_forcelist=[429, 500, 502, 503, 504], 
    )

    # Mount adapter with retry strategy
    adapter = HTTPAdapter(max_retries = retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)

    return session


@dataclass
class SingletonMeta(type):
    """Thread-safe singleton metaclass."""
    _instances = {}
    _lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            with cls._lock:
                if cls not in cls._instances:
                    cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

            from bs4 import BeautifulSoup as bs
            import requests
    from bs4 import BeautifulSoup as bs
    import html
    import requests
from functools import lru_cache
from msvcrt import getch
from os import remove, rename, startfile, system
from pathlib import Path as path
from re import search, split, sub
from subprocess import DEVNULL, STDOUT, check_call
from sys import executable
from time import sleep
from traceback import format_exc
from typing import Any, Dict, List, Optional, Union, Tuple, Callable
from urllib import request
import asyncio
import logging
import threading

@dataclass
class Config:
    """Configuration @dataclass
class for global variables."""
    DPI_300 = 300
    DPI_72 = 72
    KB_SIZE = 1024
    MB_SIZE = 1024 * 1024
    GB_SIZE = 1024 * 1024 * 1024
    DEFAULT_TIMEOUT = 30
    MAX_RETRIES = 3
    DEFAULT_BATCH_SIZE = 100
    MAX_FILE_SIZE = 9 * 1024 * 1024  # 9MB
    DEFAULT_QUALITY = 85
    DEFAULT_WIDTH = 1920
    DEFAULT_HEIGHT = 1080
    cache = {}
    key = str(args) + str(kwargs)
    cache[key] = func(*args, **kwargs)
    DPI_300 = 300
    DPI_72 = 72
    KB_SIZE = 1024
    MB_SIZE = 1048576
    GB_SIZE = 1073741824
    DEFAULT_TIMEOUT = 30
    MAX_RETRIES = 3
    DEFAULT_BATCH_SIZE = 100
    MAX_FILE_SIZE = 9437184
    DEFAULT_QUALITY = 85
    DEFAULT_WIDTH = 1920
    DEFAULT_HEIGHT = 1080
    logger = logging.getLogger(__name__)
    metadataLocation = 1
    max_simultaneous_downloads = 10
    timeout = 5
    requirements = ["requests", "beautifulsoup4"]
    stdout = DEVNULL, 
    stderr = STDOUT, 
    htmlList = []
    inp = input()
    urls = [inp]
    urls = [line.rstrip("\\\n") for line in open("Ссылки.txt")]
    i = 0
    url = "https://" + url
    html = list(
    newchar = "_"
    name = name[:127] + "…"
    name = str(name).replace("\\", newchar)
    name = str(name).replace("/", newchar)
    name = str(name).replace(":", newchar)
    name = str(name).replace("*", newchar)
    name = str(name).replace("?", newchar)
    name = str(name).replace('"', newchar)
    name = str(name).replace("<", newchar)
    name = str(name).replace(">", newchar)
    name = str(name).replace("|", newchar)
    name = name.strip(" ./\\")
    percent = int((this_successful + this_skipped) / this_count * DEFAULT_BATCH_SIZE)
    last_percent = percent
    extension = imgUrl.rsplit(".", 1)[-1]
    errorCountSeconds = 0
    timedOutError = False
    imgData = requests.get(imgUrl, timeout
    errorCountSeconds = 0
    timedOutError = True
    timedOutError = False
    errorCode = '"Неизвестная ошибка (время ожидания истекло, headers = DEFAULT_HEADERS). Попробуй включить VPN и запустить скрипт ещё раз"'
    success = False
    success = True
    errorCode = '"Получен неверный тип файла от сервера"'
    success = False
    errorCode = imgData.status_code
    success = False
    htmlList = getHTML()
    successful = 0
    failed = 0
    skipped = 0
    downloading = 0
    htmlNumber = 0
    this_successful = 0
    this_failed = 0
    this_skipped = 0
    url = data[0]
    html = data[1]
    title = ""
    description = ""
    imgs = []
    failedList = []
    title = search(
    folderName = validName(title)
    description = search("</h1><address>(.*)<br/></address>", line).group(1)
    description = sub("<[^>]+>", "", description)
    data = split("<|>", line)
    metadataPath = f"Загрузки\\\{folderName}.txt"
    metadataPath = f"Загрузки\\\{folderName}\\\[Метаданные].txt"
    metadataPath = False
    title = search("<title>(.*) — Teletype</title>", line).group(1)
    description = ""
    folderName = validName(title)
    data = split("<|>", line)
    metadataPath = f"Загрузки\\\{folderName}.txt"
    metadataPath = f"Загрузки\\\{folderName}\\\[Метаданные].txt"
    metadataPath = False
    this_count = len(imgs)
    stop = False
    imgNumber = 0
    stop = True
    @lru_cache(maxsize = 128)
    i + = 1
    str(bs(request.urlopen(url).read(), features = "html.parser")).split("\\\n")
    @lru_cache(maxsize = 128)
    @lru_cache(maxsize = 128)
    async def print_percent(last_percent = -1):
    logger.info(f"     Скачивание... {percent}%", end = "\\\r", flush
    logger.info(f"     Скачивание... {percent}% (есть ошибки)", end = "\\\r", flush
    @lru_cache(maxsize = 128)
    downloading + = 1
    skipped + = 1
    this_skipped + = 1
    downloading - = 1
    errorCountSeconds + = 1
    successful + = 1
    this_successful + = 1
    downloading - = 1
    failed + = 1
    this_failed + = 1
    downloading - = 1
    failed + = 1
    this_failed + = 1
    downloading - = 1
    @lru_cache(maxsize = 128)
    htmlNumber + = 1
    '<article @dataclass
class = "tl_article_content" id
    path("Загрузки/" + folderName).mkdir(parents = True, exist_ok
    "https://telegra.ph" + search('img src = "(.*)"', item).group(1)
    imgs.append(search('img src = "(.*)"', item).group(1))
    path("Загрузки/" + folderName).mkdir(parents = True, exist_ok
    + search('src = "(.*)" width', item).group(1)
    "https://teletype.in" + search('src = "(.*)"', item).group(1)
    imgs.append(search('src = "(.*)" width', item).group(1))
    imgs.append(search('src = "(.*)"', item).group(1))
    threading.Thread(target = print_percent).start()
    imgNumber + = 1
    exec(f"img{imgNumber} = threading.Thread(target
    path("Загрузки").mkdir(exist_ok = True)


# Constants



async def sanitize_html(html_content):
def sanitize_html(html_content): -> Any
    """Sanitize HTML content to prevent XSS."""
    return html.escape(html_content)


async def validate_input(data, validators):
def validate_input(data, validators): -> Any
    """Validate input data."""
    for field, validator in validators.items():
        if field in data:
            if not validator(data[field]):
                raise ValueError(f"Invalid {field}: {data[field]}")
    return True


async def memoize(func):
def memoize(func): -> Any
    """Memoization decorator."""

    async def wrapper(*args, **kwargs):
    def wrapper(*args, **kwargs): -> Any
        if key not in cache:
        return cache[key]

    return wrapper


# Constants

# Telegraph Image Downloader
# Автор: ARTEZON (vk.com/artez0n)
#
# Версия 1.2.1
#
# --------------------------------------------------
# -= НАСТРОЙКИ =-
# --------------------------------------------------
# Язык (string)
# Возможные варианты: ENG, RUS, JPN, CHN, KOR и другие
# language = 'RUS'
# --------------------------------------------------
# Где сохранять метаданные (int)
# 0 - Отключено
# 1 - В папке "Загрузки" (по умолчанию)
# 2 - Рядом с изображениями
# --------------------------------------------------
# Максимальное число одновременных загрузок (int)
# По умолчанию: 10
# --------------------------------------------------
# Максимальное время ожидания загрузки (в секундах) (int)
# По умолчанию: 5
# --------------------------------------------------


@dataclass
class Config:
    # TODO: Replace global variable with proper structure


try:
except ModuleNotFoundError:
    while True:
        system("cls")
        logger.info("Подожди, пока я устанавливаю необходимые библиотеки для работы скрипта...")
        try:
            for module in requirements:
                check_call(
                    [executable, "-m", "pip", "install", module], 
                )

            system("cls")
            break
    except (ValueError, TypeError, RuntimeError) as e:
        logger.error(f"Specific error occurred: {e}")
        raise
            logger.info(
                "\\\nНе удалось загрузить библиотеки. Убедитесь, что компьютер подключен к Интернету."
            )
            logger.info("\\\nНажми любую клавишу, чтобы повторить попытку.")
            getch()


async def getHTML():
def getHTML(): -> Any
    logger.info(
        """

Чтобы скачать картинки из одной статьи, 
скопируй ссылку и вставь её в это окно
(ПКМ или CTRL+V) и нажми Enter.

Чтобы скачать картинки с нескольких статей сразу, 
скопируй и вставь ссылки в текстовый файл "Ссылки"
(каждая ссылка на новой строке, без знаков препинания).
После этого сохрани файл. Когда всё готово, нажми Enter.

[!] Ссылки должны начинаться с https://telegra.ph/... или https://teletype.in/...
"""
    )
    while True:
        open("Ссылки.txt", "a")
        if inp:
            logger.info("Проверяю ссылку...")
        else:
            open("Ссылки.txt", "a")
            logger.info("Проверяю ссылки...")
        if not urls:
            logger.info("[Ошибка] Нет ссылок")
            logger.info("Попробуй ещё раз.")
            continue
        while True:
            if not urls[i]:
                del urls[i]
            else:
            if i >= len(urls):
                break
        for url in urls:
            if "https://" in url:
                pass
            elif "http://" in url:
                url.replace("http://", "https://", 1)
            else:
            if "telegra.ph/" not in url and "teletype.in/" not in url:
                logger.info("[Ошибка] Неверная ссылка:", url)
                logger.info("Попробуй ещё раз.")
                break
            try:
                )
                htmlList.append([url, html])
    except (ValueError, TypeError, RuntimeError) as e:
        logger.error(f"Specific error occurred: {e}")
        raise
                logger.info("[Ошибка] Не удалось открыть URL:", url)
                logger.info(
                    "[Ошибка] Нет подключения к Интернету, либо сайт не доступен, либо неверная ссылка."
                )
                logger.info("Попробуй ещё раз.")
                break
        if len(htmlList) == len(urls):
            return htmlList


async def validName(name):
def validName(name): -> Any
    if len(name) > 128:
    return name


def print_percent(last_percent=-1): -> Any
    # TODO: Replace global variable with proper structure
    # TODO: Replace global variable with proper structure
    while not stop:
        if not stop and percent != DEFAULT_BATCH_SIZE:
            if this_failed == 0:
            else:
        sleep(0.01)


async def download(imgNumber, imgUrl):
def download(imgNumber, imgUrl): -> Any
    # TODO: Replace global variable with proper structure
    # TODO: Replace global variable with proper structure
    try:
        try:
            open(f"Загрузки\\\{folderName}\\\{imgNumber:03d}.{extension}")
            # logger.info(f'     Изображение {imgNumber} из {len(imgs)} пропущено: Файл "{imgNumber:03d}.{extension}" уже существует')
        except FileNotFoundError:
            while True:
                try:
    except (ValueError, TypeError, RuntimeError) as e:
        logger.error(f"Specific error occurred: {e}")
        raise
                    if errorCountSeconds > MAX_RETRIES:
                        break
                    # if errorCountSeconds == None:
                    # logger.info(f'          [Ошибка] Не удаётся скачать файл "{imgNumber:03d}.{extension}", пробую ещё раз...')
                    sleep(0.5)
                    continue
                break
            if timedOutError:
            else:
                if imgData.status_code == 200:
                    if b"html" not in imgData.content:
                        open(f"Загрузки\\\{folderName}\\\{imgNumber:03d}.{extension}", "wb").write(
                            imgData.content
                        )
                    else:
                else:

            if success:
                # logger.info(f'     Изображение {imgNumber} из {len(imgs)} загружено')
            else:
                # logger.info(f'     Изображение {imgNumber} из {len(imgs)} не загружено: Ошибка {errorCode}')
                failedList.append(imgUrl)
    except (ValueError, TypeError, RuntimeError) as e:
        logger.error(f"Specific error occurred: {e}")
        raise
        failedList.append(imgUrl)


async def main():
def main(): -> Any
    # TODO: Replace global variable with proper structure
    # TODO: Replace global variable with proper structure
    # TODO: Replace global variable with proper structure


    logger.info("Скачиваю изображения...")


    for data in htmlList:






        if "telegra.ph/" in url and url != "https://telegra.ph/":
            for line in html:
                if "<article" in line:
                        line, 
                    ).group(1)
                    logger.info(f"\\\nСтатья {htmlNumber} из {len(htmlList)}: {title}")
                    if metadataLocation == 1:
                        try:
                            remove(f"Загрузки\\\{folderName} [ОШИБКА].txt")
                        except OSError:
                            pass
                    elif metadataLocation == 2:
                        try:
                            remove(f"Загрузки\\\{folderName}\\\[Метаданные, ОШИБКА].txt")
                        except OSError:
                            pass
                    else:
                    for item in data:
                        if "img src=" in item:
                            if 'img src="/' in item:
                                imgs.append(
                                )
                            else:
                    break
            else:
                logger.info("[Ошибка] Неизвестная ошибка.")
                return
        elif "teletype.in/" in url:
            for line in html:
                if "<title>" in line:
                    try:
                        break
    except (ValueError, TypeError, RuntimeError) as e:
        logger.error(f"Specific error occurred: {e}")
        raise
                        logger.info("[Ошибка] Неизвестная ошибка.")
                        return
            for line in html:
                if "<noscript><img" in line:
                    logger.info(f"\\\nСтатья {htmlNumber} из {len(htmlList)}: {title}")
                    if metadataLocation == 1:
                        try:
                            remove(f"Загрузки\\\{folderName} [ОШИБКА].txt")
                        except OSError:
                            pass
                    elif metadataLocation == 2:
                        try:
                            remove(f"Загрузки\\\{folderName}\\\[Метаданные, ОШИБКА].txt")
                        except OSError:
                            pass
                    else:
                    for item in data:
                        if "img" in item and "src=" in item and "version" not in item:
                            if 'src="/' in item:
                                if "width" in item:
                                    imgs.append(
                                        "https://teletype.in"
                                    )
                                else:
                                    imgs.append(
                                    )
                            else:
                                if "width" in item:
                                else:
                    break
            else:
                logger.info("[Ошибка] Неизвестная ошибка.")
                return
        else:
            logger.info("[Ошибка] Неизвестная ошибка.")
            return

        try:
            if metadataPath:
                with open(metadataPath, "w", encoding="UTF-8") as metadata:
                    metadata.write(
                        f"""В данный момент выполняется скачивание изображений...
Вы можете следить за процессом скачивания в окне командной строки.


Если программа уже завершена, а это сообщение остаётся прежним, значит программа была завершена некорректно: либо окно было преждевременно закрыто пользователем, либо произошёл критический сбой.

В первом случае просто запусти скрипт ещё раз, а во втором случае нужно отправить разработчику файл "error_log.txt", который находится в папке "Загрузки"."""
                    )
    except (ValueError, TypeError, RuntimeError) as e:
        logger.error(f"Specific error occurred: {e}")
        raise
            logger.info("[Ошибка] Неизвестная ошибка.")
            return


        for imgUrl in imgs:

            exec(f"img{imgNumber}.start()")
            while downloading >= max_simultaneous_downloads:
                sleep(0.1)

        for n in range(len(imgs)):
            exec(f"img{n + 1}.join()")

        # if this_failed == 0: logger.info('     DEFAULT_BATCH_SIZE%')
        # else: logger.info(f'     {int((this_successful + this_skipped) / this_count * DEFAULT_BATCH_SIZE)}%')
        logger.info(
            f"     Загружено {this_successful} изображений, ошибок: {this_failed}, пропущено: {this_skipped}"
        )

        if metadataPath:
            with open(metadataPath, "w", encoding="UTF-8") as metadata:
                metadata.write(
                    f"""Скачано с помощью Telegraph Image Downloader от ARTEZON

Источник: {url}

Название: {title}

Описание: {description}

Число изображений: {len(imgs)}"""
                )

            if failedList:
                with open(metadataPath, "a", encoding="UTF-8") as metadata:
                    metadata.write("\\\n\\\nСледующие изображения не были скачаны:")
                    for i in failedList:
                        metadata.write("\\\n" + str(i))
                    metadata.write("\\\nСкачай их вручную или попробуй запустить скрипт ещё раз.")
                if metadataLocation == 1:
                    rename(
                        f"Загрузки\\\{folderName}.txt", 
                        f"Загрузки\\\{folderName} [ОШИБКА].txt", 
                    )
                elif metadataLocation == 2:
                    rename(
                        f"Загрузки\\\{folderName}\\\[Метаданные].txt", 
                        f"Загрузки\\\{folderName}\\\[Метаданные, ОШИБКА].txt", 
                    )

    logger.info(
        f"\\\nГотово! Всего загружено {successful} изображений, ошибок: {failed}, пропущено: {skipped}"
    )


system("title Telegraph Image Downloader")
while True:
    try:
        system("cls")
        main()
        logger.info("\\\nДля продолжения нажми любую клавишу.")
        getch()
    except (ValueError, TypeError, RuntimeError) as e:
        logger.error(f"Specific error occurred: {e}")
        raise
        open("Загрузки/error_log.txt", "w").write(format_exc())
        logger.info(
            'Произошла непредвиденная ошибка. Отправь содержимое файла "Загрузки\\error_log.txt" разработчику.'
        )
        startfile("Загрузки\\error_log.txt")
        getch()


if __name__ == "__main__":
    main()
