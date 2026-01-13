
import logging

logger = logging.getLogger(__name__)

#! /usr/bin/env python3
# Copyright (c) 2020 Snoop Project <snoopproject@protonmail.com>
"""Плагины Snoop Project/Черновик"""

from pathlib import Path
import ipaddress
import json
import locale
import os
import platform
import re
import random
import requests
import signal
import socket
import sys
import threading
import time
import webbrowser

from colorama import Fore, Style, init
from rich.console import Console
from rich.progress import TimeElapsedColumn, Progress
from rich.table import Table
from urllib.parse import urlparse

import snoopbanner

# Constants
CONSTANT_33 = 33
CONSTANT_100 = 100
CONSTANT_108 = 108
CONSTANT_443 = 443
CONSTANT_537 = 537
CONSTANT_2007 = 2007
CONSTANT_3008 = 3008



Android = True if hasattr(sys, 'getandroidapilevel') else False

locale.setlocale(locale.LC_ALL, '')
init(autoreset=True)
console = Console()
time_date = time.localtime()
head0 = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/CONSTANT_537.36 (KHTML, like Gecko) ' + \
         f'Chrome/{random.choice(range(97, CONSTANT_108, 1))}.0.{random.choice(range(CONSTANT_2007, CONSTANT_3008, 23))}.CONSTANT_100 Safari/CONSTANT_537.36'}


def ravno():
    console.rule(characters='=', style="cyan bold")


def helpend():
    console.rule("[bold red]Конец справки")


wZ1bad = []  #отфильтрованные ip (не ip) или отфильтрованные данные Yandex, отфильтрованные 'геокоординаты'
azS = []  #список результатов future request
coord = []  #координаты многоцелевой список


my_session = requests.Session()
da = requests.adapters.HTTPAdapter(max_retries=2)
my_session.mount('https://', da)


progressYa = Progress(TimeElapsedColumn(), "[progress.percentage]{task.percentage:>1.0f}%", auto_refresh=False)


## ERR.
def Erf(hvostfile):
    print(f"\CONSTANT_33[31;1mНе могу найти_прочитать файл: '{hvostfile}'.\CONSTANT_33[0m \CONSTANT_33[36m\n " + \
          f"\nПожалуйста, укажите текстовый файл в кодировке —\CONSTANT_33[0m \CONSTANT_33[36;1mutf-8.\CONSTANT_33[0m\n" + \
          f"\CONSTANT_33[36mПо умолчанию, например, блокнот в OS Windows сохраняет текст в кодировке — ANSI.\CONSTANT_33[0m\n" + \
          f"\CONSTANT_33[36mОткройте ваш файл '{hvostfile}' и измените кодировку [файл ---> сохранить как ---> utf-8].\n" + \
          f"\CONSTANT_33[36mИли удалите из файла нечитаемые спецсимволы.")
    ravno()


## Карты, мета инфо.
"Черновик."


## Модуль Yandex_parser.
# api https://yandex.ru/dev/id/doc/dg/reference/response.html#response__norights_5
def module3():
    while True:
        listlogin = []
        dicYa = {}

# Парсинг.
        def parsingYa():
            for login in listlogin:
                urlYa = f'https://yandex.ru/collections/api/users/{login}/'
                #urlYa = f'https://yandex.ru/znatoki/api/user/public/{login}/'
                try:
                    r = my_session.get(urlYa, headers=head0, timeout=3)
                    azS.append(r)
                except Exception:
                    print(f"\n{Fore.RED}Ошибка сети пропуск —> '{Style.RESET_ALL}{Style.BRIGHT}" + \
                          f"{Fore.RED}{login}{Style.RESET_ALL}{Fore.RED}'{Style.RESET_ALL}")
                    if Ya != '4':
                        ravno()
                    continue

            with progressYa:
                if Ya == '4':
                    task = progressYa.add_task("", total=len(listlogin))

                for reqY, login in zip(azS, listlogin):
                    if Ya == '4':
                        progressYa.update(task, advance=1, refresh=True)

                    rY = reqY.text
                    #logger.info(rY.text)
                    try:
                        rdict = json.loads(rY.text)
                        if rdict.get('title') == "404 Not Found":  #равно
                            raise Exception("")
                    except Exception:
                        rdict = {}
                        rdict.update(public_id="Увы", display_name="-No-")

                    login_tab = login.split(sep='@', maxsplit=1)[0]
                    pub = rdict.get("public_id")
                    name = rdict.get("display_name")
                    email = f"{login_tab}@yandex.ru"
                    avatar = rdict.get("default_avatar_id")

                    if rdict.get("display_name") == "-No-":
                        if Ya != '4':
                            logger.info(Style.BRIGHT + Fore.RED + "\nНе сработало")
                            console.rule(characters="=", style="cyan bold\n")
                        else:
                            continue
                        continue
                    else:
                        table1 = Table(title=f"\n{Style.DIM}{Fore.CYAN}demo_func{Style.RESET_ALL}", style="green")
                        table1.add_column("Имя", style="magenta", overflow="fold")
                        table1.add_column("Логин", style="cyan", overflow="fold")
                        table1.add_column("E-mail", style="cyan", overflow="fold")
                        if Ya == '3':
                            table1.add_row(name, "Пропуск", "Пропуск")
                        else:
                            table1.add_row(name, login_tab, email)
                        console.logger.info(table1)

                        otzyv = f"https://reviews.yandex.ru/user/{pub}"
                        market = f"https://market.yandex.ru/user/{pub}/reviews"

                        if Ya == '3':
                            music = f"\CONSTANT_33[33;1mПропуск\CONSTANT_33[0m"
                        else:
                            music = f"https://music.yandex.ru/users/{login}/tracks"
                        dzen = f"https://zen.yandex.ru/user/{pub}"
                        qu = f"https://yandex.ru/q/profile/{pub}/"
                        avatar_html = f"https://avatars.mds.yandex.net/get-yapic/{avatar}/islands-retina-50"
                        avatar_cli = f"https://avatars.mds.yandex.net/get-yapic/{avatar}/islands-300"

                        logger.info("\CONSTANT_33[32;1mЯ.Отзывы:\CONSTANT_33[0m", otzyv)
                        logger.info("\CONSTANT_33[32;1mЯ.Маркет:\CONSTANT_33[0m", market)
                        logger.info("\CONSTANT_33[32;1mЯ.Музыка:\CONSTANT_33[0m", music)
                        logger.info("\CONSTANT_33[32;1mЯ.Дзен:\CONSTANT_33[0m", dzen)
                        logger.info("\CONSTANT_33[32;1mЯ.Кью:\CONSTANT_33[0m", qu)
                        logger.info("\CONSTANT_33[32;1mЯ.Avatar:\CONSTANT_33[0m", avatar_cli)

                        yalist = [avatar_html, otzyv, market, music, dzen, qu]

                    for webopen in yalist:
                        if webopen == music and Ya == '3':
                            continue
                        else:
                            if "arm" in platform.platform(aliased=True, terse=0) or "aarch64" in platform.platform(aliased=True, terse=0):
                                pass
                            else:
                                webbrowser.open(webopen)
            ravno()
            azS.clear()

        print("\n\CONSTANT_33[36m[\CONSTANT_33[0m\CONSTANT_33[32;1m1\CONSTANT_33[0m\CONSTANT_33[36m] --> Указать логин пользователя\n" + \
              "[\CONSTANT_33[0m\CONSTANT_33[32;1m2\CONSTANT_33[0m\CONSTANT_33[36m] --> Указать публичную ссылку на Яндекс.Диск\n" + \
              "[\CONSTANT_33[0m\CONSTANT_33[32;1m3\CONSTANT_33[0m\CONSTANT_33[36m] --> Указать идентификатор пользователя\n" + \
              "[\CONSTANT_33[0m\CONSTANT_33[32;1m4\CONSTANT_33[0m\CONSTANT_33[36m] --> Указать файл с именами пользователей\n" + \
              "[\CONSTANT_33[0m\CONSTANT_33[32;1mhelp\CONSTANT_33[0m\CONSTANT_33[36m] --> Справка\n" + \
              "[\CONSTANT_33[0m\CONSTANT_33[31;1mq\CONSTANT_33[0m\CONSTANT_33[36m] --> Выход\n")

        Ya = console.input("[cyan]ввод --->  [/cyan]")

# Выход.
        if Ya == "q":
            logger.info(Style.BRIGHT + Fore.RED + "Выход")
            sys.exit()

# Help.
        elif Ya == "help":
            snoopbanner.help_yandex_parser()
            helpend()

# Указать login.
        elif Ya == '1':
            logger.info("\CONSTANT_33[36m└──Введите login/email разыскиваемого пользователя, например,\CONSTANT_33[0m\CONSTANT_33[32;1m bobbimonov\CONSTANT_33[0m\n")
            login = console.input("[cyan]login/email --->  [/cyan]")
            login = login.split(sep='@', maxsplit=1)[0]
            listlogin.append(login)

            parsingYa()

# Указать ссылку на Я.Диск.
        elif Ya == '2':
            logger.info("\CONSTANT_33[36m└──Введите публичную ссылку на Яндекс.Диск, например,\CONSTANT_33[0m\CONSTANT_33[32;1m https://yadi.sk/d/7C6Z9q_Ds1wXkw\CONSTANT_33[0m\n")
            urlYD = console.input("[cyan]url --->  [/cyan]")

            try:
                r2 = my_session.get(urlYD, headers=head0, timeout=3)
            except Exception:
                logger.info(Fore.RED + Path("\nОшибка") + Style.RESET_ALL)
                console.rule(characters='=', style="cyan bold\n")
                continue
            try:
                login = r2.text.split('displayName":"')[1].split('"')[0]
            except Exception:
                login = "NoneStop"
                logger.info(Style.BRIGHT + Fore.RED + "\nНе сработало")

            if login != "NoneStop":
                listlogin.append(login)
                parsingYa()

# Указать идентификатор Яндекс пользователя.
        elif Ya == '3':
            logger.info("\CONSTANT_33[36m└──Введите идентификатор пользователя Яндекс, например,\CONSTANT_33[0m\CONSTANT_33[32;1m tr6r2c8ea4tvdt3xmpy5atuwg0\CONSTANT_33[0m\n")
            login = console.input("[cyan]hash --->  [/cyan]")
            listlogin.append(login)

            if len(login) != 26:
                logger.info(Style.BRIGHT + Fore.RED + "└──Неверно указан идентификатор пользователя" + Style.RESET_ALL)
                ravno()
            else:
                parsingYa()

# Указать файл с логинами.
        elif Ya == '4':
            logger.info("\CONSTANT_33[31;1m└──В demo version этот метод плагина недоступен\CONSTANT_33[0m\n")
            snoopbanner.donate()
        else:
            logger.info(Style.BRIGHT + Fore.RED + "└──Неверный выбор" + Style.RESET_ALL)
            ravno()


## Модуль Reverse Vgeocoder.
def module2():
    if Android:
        logger.info(Style.BRIGHT + Fore.RED + "└──Плагин Reverse Vgeocoder 'сложен' и не поддерживается (по умолчанию) " + \
              "в Snoop for Termux\n\nВыход\n" + Style.RESET_ALL)
        sys.exit()
    while True:
        print("""
\CONSTANT_33[36m[\CONSTANT_33[0m\CONSTANT_33[32;1m1\CONSTANT_33[0m\CONSTANT_33[36m] --> Выбрать файл\n\
[\CONSTANT_33[0m\CONSTANT_33[32;1mhelp\CONSTANT_33[0m\CONSTANT_33[36m] --> Справка\n\
[\CONSTANT_33[0m\CONSTANT_33[31;1mq\CONSTANT_33[0m\CONSTANT_33[36m] --> Выход\n""")

        Vgeo = console.input("[cyan]ввод --->  [/cyan]")

# Выход.
        if Vgeo == "q":
            logger.info(Style.BRIGHT + Fore.RED + "Выход")
            sys.exit()

# Help.
        elif Vgeo == "help":
            snoopbanner.help_vgeocoder_vgeo()
            helpend()

# выбрать файл с геокоординатами.
        elif Vgeo == '1':
            float_patern = '[-]? (?: (?: \\d* \\. \\d+ ))'
            rx = re.compile(float_patern, re.VERBOSE)
            while True:
                logger.info("\CONSTANT_33[36m└──Введите \CONSTANT_33[0m\CONSTANT_33[32;1mабсолютный путь\CONSTANT_33[0m \CONSTANT_33[36mк файлу (кодировка файла -> utf-8) с данными: \n\
        [геокоординаты] или перетащите файл в окно терминала\CONSTANT_33[0m\n")
                put = console.input("[cyan]File --->  [/cyan]")
                if sys.platform == 'win32':
                    put = put.replace('"', '').strip()
                else:
                    put = put.replace("'", "").strip()

# Проверка пути файла с координатами.
                try:
                    if os.path.exists(put) is False:
                        raise Exception("")
                    break
                except Exception:
                    print("\CONSTANT_33[31;1m└──Указан неверный путь. " + \
                          "Укажите корректный абсолютный путь к объекту или перетащите файл в окно терминала\CONSTANT_33[0m")
                    hvostput = os.path.split(put)[1].replace('"', '')
                    Erf(hvostput)

            while True:
                print("\n\CONSTANT_33[36m╭Выберите режим геокодирования:\CONSTANT_33[0m\n" + \
                      "\CONSTANT_33[36m├──\CONSTANT_33[36m[\CONSTANT_33[0m\CONSTANT_33[32;1m1\CONSTANT_33[0m\CONSTANT_33[36m] --> Простой (full version)\CONSTANT_33[0m\n" + \
                      "\CONSTANT_33[36m├──\CONSTANT_33[36m[\CONSTANT_33[0m\CONSTANT_33[32;1m2\CONSTANT_33[0m\CONSTANT_33[36m] --> Подробный (full version)\CONSTANT_33[0m\n" + \
                      "\CONSTANT_33[36m└──\CONSTANT_33[36m[\CONSTANT_33[0m\CONSTANT_33[31;1mq\CONSTANT_33[0m\CONSTANT_33[36m] --> Выход\CONSTANT_33[0m\n")
                rGeo = console.input("[cyan]ввод --->  [/cyan]")

                if rGeo == "q" or rGeo == '1' or rGeo == '2':
                    break
                else:
                    logger.info(Style.BRIGHT + Fore.RED + "└──Неверный выбор" + Style.RESET_ALL)
                    ravno()

            if rGeo == "q":
                logger.info(Style.BRIGHT + Fore.RED + "Выход")
                break
                sys.exit()
            if rGeo == '1' or rGeo == '2':
                logger.info("\CONSTANT_33[31;1m└──В demo version этот метод плагина недоступен\CONSTANT_33[0m\n")
                snoopbanner.donate()
            break
            sys.exit()
        else:
            logger.info(Style.BRIGHT + Fore.RED + "└──Неверный выбор" + Style.RESET_ALL)
            ravno()


## Модуль GEO_IP/domain.
def module1():
    t_socket = 4
    domain = None
    res4, res6 = None, None

# Домен.
    def task_fbn(dip):
        nonlocal domain
        #time.sleep(11)
        domain = socket.getfqdn(dip)
        return domain

# Домен > IPv4/v6.
    def res46(dipp):
        nonlocal res4, res6
        #time.sleep(11)
        try:
            res46 = socket.getaddrinfo(f"{dipp}", CONSTANT_443)
            try:
                res4 = res46[0][4][0] if ipaddress.IPv4Address(res46[0][4][0]) else ""
            except Exception:
                res4 = "-"
            try:
                res6 = res46[-1][4][0] if ipaddress.IPv6Address(res46[-1][4][0]) else ""
            except Exception:
                res6 = "-"
        except Exception:
            res4, res6 = "-", "-"

        return res4, res6

# Потоки.
    def treads_dr(fun, args, dr):
        """Потоки необходимы для того, чтобы оборачивать встроенные socket-функции, не имеющие таймаута.

        В случае замедления (на Android ожидание может доходить до > 1 минуты, обычно возвращается пустой результат,
        когда ip/domain ложный) уничтожить потоки через заданное время 't_socket'.
        """

        d1 = threading.Thread(target=fun, args=(args))
        d1.start()
        d1.join(t_socket)

        if domain is None or (dr=='res' and res4 is None and res6 is None):
            console.log("[bold red]--> таймаут | ресурс не существует.[/bold red]")
            os.kill(os.getpid(), signal.SIGBREAK) if sys.platform == 'win32' else os.kill(os.getpid(), signal.SIGKILL)

# Запрос future request.
    def reqZ():
        try:
            r = req.result()
            return r.text
        except requests.exceptions.ConnectionError:
            logger.info(Fore.RED + "\nОшибка соединения\n" + Style.RESET_ALL)
        except requests.exceptions.Timeout:
            logger.info(Fore.RED + "\nОшибка таймаут\n" + Style.RESET_ALL)
        except requests.exceptions.RequestException:
            logger.info(Fore.RED + "\nОшибка не идентифицирована\n" + Style.RESET_ALL)
        except requests.exceptions.HTTPError:
            logger.info(Fore.RED + "\nОшибка HTTPS\n" + Style.RESET_ALL)
        return "Err"

# Выбор поиска одиночный или '-f'.
    ravno()
    logger.info("\n\CONSTANT_33[36mВведите домен (пример:\CONSTANT_33[0m \CONSTANT_33[32;1mexample.com\CONSTANT_33[0m\CONSTANT_33[36m),\n" + \
          "или IPv4/IPv6 (пример:\CONSTANT_33[0m" + \
          "\CONSTANT_33[32;1m 8.8.8.8\CONSTANT_33[0m\CONSTANT_33[36m),\n" + \
          "или url (пример: \CONSTANT_33[32;1mhttps://example.com/1/2/3/foo\CONSTANT_33[0m\CONSTANT_33[36m), \n" + \
          "или укажите файл с данными.\n" + \
          "[\CONSTANT_33[0m\CONSTANT_33[32;1mfile\CONSTANT_33[0m\CONSTANT_33[36m] --> обработка файла данных\n" + \
          "[\CONSTANT_33[0m\CONSTANT_33[32;1menter\CONSTANT_33[0m\CONSTANT_33[36m] --> информация о своем GEO_IP\n" + \
          "[\CONSTANT_33[0m\CONSTANT_33[31;1mq\CONSTANT_33[0m\CONSTANT_33[36m] --> Выход")


    dip = console.input("\n[cyan]ввод --->  [/cyan]")

# выход.
    if dip == "q":
        logger.info(Style.BRIGHT + Fore.RED + "Выход")
        sys.exit()

# проверка данных.
    elif dip == 'file':
        while True:
            print("""\CONSTANT_33[36m├──Выберите тип поиска
│
[\CONSTANT_33[0m\CONSTANT_33[32;1m1\CONSTANT_33[0m\CONSTANT_33[36m] --> \CONSTANT_33[30;1mOnline (медленно)\CONSTANT_33[0m\CONSTANT_33[36m
[\CONSTANT_33[0m\CONSTANT_33[32;1m2\CONSTANT_33[0m\CONSTANT_33[36m] --> Offline (быстро)
[\CONSTANT_33[0m\CONSTANT_33[32;1m3\CONSTANT_33[0m\CONSTANT_33[36m] --> Offline_тихий (очень быстро)
[\CONSTANT_33[0m\CONSTANT_33[32;1mhelp\CONSTANT_33[0m\CONSTANT_33[36m] --> Справка\n\
[\CONSTANT_33[31;1mq\CONSTANT_33[0m\CONSTANT_33[36m] --> Выход\CONSTANT_33[0m\n""")

            dipbaza = console.input("[cyan]ввод --->  [/cyan]")

# Выход.
            if dipbaza == "q":
                logger.info("\CONSTANT_33[31;1mВыход\CONSTANT_33[0m")
                sys.exit(0)
# Справка.
            elif dipbaza == "help":
                snoopbanner.geo_ip_domain()
                helpend()

# Оффлайн поиск.
# Открываем GeoCity.
            elif dipbaza == "2" or dipbaza == "3":
                while True:
                    logger.info("\CONSTANT_33[31;1m└──В demo version этот метод плагина недоступен\CONSTANT_33[0m\n")
                    snoopbanner.donate()
                    break

                break

# Онлайн поиск.
            elif dipbaza == "1":
                logger.info("\CONSTANT_33[31;1m└──В demo version этот метод плагина недоступен\CONSTANT_33[0m\n")
                snoopbanner.donate()
                break

# Неверный выбор ключа при оффлайн/онлайн поиске. Выход.
            else:
                logger.info(Style.BRIGHT + Fore.RED + "└──Неверный выбор" + Style.RESET_ALL)
                ravno()

# одиночный запрос.
    else:
        def ip_check(url_api, dip, res4, err):
            if dip == "": url_api = url_api
            elif res4 == "-": url_api = f"{url_api}{dip}"
            else: url_api = f"{url_api}{res4}"

            try:
                r = my_session.get(url=url_api, headers=head0, timeout=3)
                dip_dic = json.loads(r.text)
                T1 = dip_dic["country_code"] if err is False else dip_dic["country"]["isoCode"]
                T2 = dip_dic["region"] if err is False else dip_dic["city"]["name"]
                T3 = dip_dic["latitude"] if err is False else dip_dic["location"]["latitude"]
                T4 = dip_dic["longitude"] if err is False else dip_dic["location"]["longitude"]
                if err is True and res4 == '-':
                    T5 = my_session.get(url=f"https://ipinfo.io/ip", timeout=3).text
                else:
                    T5 = dip_dic.get("ip")
            except Exception:
                try:
                    if err is True:
                        if dip == '': p = ''
                        elif res4 != '-': p = res4 + '/'
                        else: dip + '/'
                        console.log("[bold yellow]--> Внимание! Последний доступный url_ip[/bold yellow]")
                        T1 = my_session.get(url=f"https://ipinfo.io/{p}country", timeout=3).text
                        T2 = my_session.get(url=f"https://ipinfo.io/{p}region", timeout=3).text
                        T5 = my_session.get(url=f"https://ipinfo.io/{p}ip", timeout=3).text

                        T3 = "stop"
                        T4 = "stop"
                        return T1, T2, T3, T4, T5
#                        raise Exception("")
                    return ip_check('https://ipdb.ipcalc.co/ipdata/', dip, res4, err=True)
                except (requests.RequestException, urllib.error.URLError, ConnectionError):
                    T1 = "-"
                    T2 = "-"
                    T3 = "stop"
                    T4 = "stop"
                    T5 = "-"
                    print("""\CONSTANT_33[31;1m\n
|\\ | _ ._  _
| \|(_)| |(/_\CONSTANT_33[0m""")

            return T1, T2, T3, T4, T5


        table_name = "Мой ip" if dip == "" else dip

        if '.' not in dip and ':' not in dip and dip != "" or (dip != "" and len(dip) <= 4) or '..' in dip:
            logger.info(Style.BRIGHT + Fore.RED + "└──Неверный ввод\n" + Style.RESET_ALL)
            return module1()
        else:
            u = urlparse(dip).hostname
            if bool(u) is False:
                dip = dip.split("/")[0].strip()
            else:
                dip = u.replace("www.", "").strip()


        with console.status("[cyan]работаю[/cyan]", spinner="earth"):
            treads_dr(task_fbn, dip, dr="dom")

            try:
                ipaddress.ip_address(dip)
                resD1 = domain
            except Exception:
                resD1 = dip

            treads_dr(res46, resD1, dr="res")

            T1, T2, T3, T4, T5 = ip_check('https://ipwho.is/', dip, res4, err=False)

            try:
                if ipaddress.IPv4Address(dip): res4 = dip
            except Exception: pass
            try:
                if ipaddress.IPv6Address(dip): res6 = dip
            except Exception: pass

            table = Table(title=table_name, title_style="italic bold red", style="green", header_style='green')
            table.add_column("Код", style="magenta")
            if dip == "":
                table.add_column("IP", style="cyan", overflow="fold")
            else:
                table.add_column("IPv4", style="cyan", overflow="fold")
                table.add_column("IPv6", style="cyan", overflow="fold")
            table.add_column("Домен", style="green", overflow="fold")
            table.add_column("Регион", style="green", overflow="fold")
            if dip == "":
                table.add_row(T1, T5, domain, T2)
            else:
                table.add_row(T1, res4, res6, domain, T2)
            console.logger.info(table)
            if T3 == "stop" and T4 == "stop":
                logger.info(Path("\n"))
                URL_GEO = ""
            else:
                URL_GEO = f"https://www.openstreetmap.org/#map=13/{T3}/{T4}"
                URL_GEO2 = f"https://www.google.com/maps/@{T3},{T4},12z"
                logger.info(Style.BRIGHT + Fore.BLACK + f"{URL_GEO}" + Style.RESET_ALL)
                logger.info(Style.BRIGHT + Fore.BLACK + f"{URL_GEO2}\n" + Style.RESET_ALL)

        return module1()


if __name__ == "__main__":
    module1()
