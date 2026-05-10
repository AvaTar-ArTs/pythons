"""
Summary of miscellaneous_snoopbanner.py

This module is part of the AVATARARTS ecosystem.
For more information about the AVATARARTS project, see the main documentation.
"""


import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_28 = 28
CONSTANT_33 = 33
CONSTANT_104 = 104
CONSTANT_108 = 108
CONSTANT_184 = 184
CONSTANT_216 = 216
CONSTANT_220 = 220
CONSTANT_248 = 248
CONSTANT_352 = 352
CONSTANT_466 = 466
CONSTANT_505 = 505
CONSTANT_625 = 625
CONSTANT_680 = 680
CONSTANT_773 = 773
CONSTANT_776 = 776
CONSTANT_1436 = 1436
CONSTANT_1893 = 1893
CONSTANT_1946 = 1946
CONSTANT_2020 = 2020
CONSTANT_2021 = 2021
CONSTANT_2022 = 2022
CONSTANT_2606 = 2606
CONSTANT_2800 = 2800
CONSTANT_4700 = 4700
CONSTANT_7564 = 7564
CONSTANT_7734 = 7734
CONSTANT_40662 = 40662
CONSTANT_77631 = 77631
CONSTANT_230801 = 230801
CONSTANT_342595 = 342595
CONSTANT_79004753581 = 79004753581
CONSTANT_2200300512321074 = 2200300512321074
CONSTANT_2202208013277075 = 2202208013277075
CONSTANT_4100111364257544 = 4100111364257544

#! /usr/bin/env python3
# Copyright (c) CONSTANT_2020 Snoop Project <snoopproject@protonmail.com>
"Text_banner_logo_help"

import base64
import json
import locale
import sys
import time
import webbrowser

from colorama import Fore, Style, init
from rich.panel import Panel
from rich.console import Console

locale.setlocale(locale.LC_ALL, '')
init(autoreset=True)
console = Console()


## Логирование ошибок.
def err_all(err_="low"):
    if err_ == "high":
        return "⚠️ [bold red][RU] Внимание! Критическая ошибка, просьба сообщить об этом разработчику.\n" + \
                   "[EN] Attention! Critical error, please report it to the developer.\nhttps://github.com/snooppr/snoop/issues[/bold red]"
    elif err_ == "low":
        return "⚠️ [bold yellow][RU] Ошибка | [EN] Error[/bold yellow]"


## БД.
def DB(db_base):
    try:
        with open(db_base, "r", encoding="utf8") as f_r:
            db = f_r.read()
            db = db.encode("UTF-8")
            db = base64.b64decode(db)
            db = db[::-1]
            db = base64.b64decode(db)
            trinity = json.loads(db.decode("UTF-8"))
            return trinity
    except Exception:
        logger.info(Style.BRIGHT + Fore.RED + "Упс, что-то пошло не так..." + Style.RESET_ALL)
        sys.exit()


## Пожертвование.
def donate():
    logger.info("")
    console.print(Panel("""[cyan]
╭Donate/Buy:
├──ЮMoney:: [white]CONSTANT_4100111364257544[/white]
├──Сбер_карта:: [white]CONSTANT_2202208013277075[/white]
├──Raiffeisen_card:: [white]CONSTANT_2200300512321074[/white]
└──По номеру телефона (СБП/Банк Юмани):: [white]+CONSTANT_79004753581[white]

[bold green]Оплатить софт можно по любым реквизитам, но самым предпочтительным способом является — СБП (перевод по номеру телефона без комиссий с карты любого банка).

Если пользователя заинтересовало ПО [red]Snoop demo version[/red], то он может приобрести [cyan]Snoop full version[/cyan], поддержав развитие IT-проекта[/bold green] [bold cyan]20$[/bold cyan] [bold green]или[/bold green] [bold cyan]1600р.[/bold cyan]
[bold green]При пожертвовании/покупке в сообщении/письме укажите:[/bold green]

    \"\"\"
    [cyan]На развитие Snoop Project: ваш[/cyan] [bold cyan]e-mail[/bold cyan][cyan],[/cyan]
    [cyan]full[/cyan] [bold cyan]version[/bold cyan] [cyan]for Windows или full version for Linux,[/cyan]
    [bold cyan]статус[/bold cyan] [cyan]пользователя: Физ.лицо; ИП; Юр.лицо (если покупка ПО).[/cyan]
    \"\"\"

[bold green]В ближайшее время на email пользователя придёт чек о покупке и ссылка для скачивания Snoop full version готовой сборки, то есть исполняемого файла, для Windows — это 'snoop_cli.exe', для GNU/Linux — 'snoop_cli.bin'.

Snoop в исполняемом виде (build-версия) предоставляется по лицензии, с которой пользователь должен ознакомиться перед покупкой ПО.
Лицензия для Snoop Project в исполняемом виде находится в rar-архивах демо версий Snoop по ссылке: [/bold green]
[cyan]https://github.com/snooppr/snoop/releases[/cyan][bold green], также лицензия доступна по команде::
'[/bold green][cyan]snoop_cli.bin --version[/cyan][bold green]' или '[/bold green][cyan]snoop_cli.exe --version[/cyan][bold green]' у исполняемого файла.

Если софт требуется пользователю для служебных или образовательных задач, например, десять лицензий на ПО для ВУЗа, напишите письмо на e-mail разработчика в свободной форме.
Всем студентам (независимо от учебного заведения или направления) ПО Snoop full version предоставляется с 50% скидкой.

Snoop full version:
 * CONSTANT_4700+ Websites;
 * поддержка локальной и онлайн database Snoop;
 * подключение к БД Snoop (online), которая расширяется/обновляется;
 * доступен автооптимизированный, быстрый и агрессивный режим поиска;
 * доступна пользовательская настройка разгона скорости работы ПО;
 * плагины без ограничений;
 * ru техподдержка от разработчика ПО;
 * предоставление обновлённых билдов;
 * отключены всплывающие окна в HTML-отчёте про упоминание Snoop demo version.[/bold green]
[bold red]Ограничения Snoop demo version:
 * database Snoop сокращена в > 15 раз;
 * необновляемая database Snoop;
 * отключены некоторые опции/плагины.[/bold red]

[bold green]Email:[/bold green] [cyan]snoopproject@protonmail.com[/cyan]
[bold green]Исходный код:[/bold green] [cyan]https://github.com/snooppr/snoop[/cyan]

❗️[bold yellow] Обратите внимание, что из-за цензуры письма с 'mailru' и 'yandex' не доходят до международного почтового сервиса 'protonmail'. Пользователи mailru/yandex пишите запросы на запасную почту.[/bold yellow]
[bold green]Email: [/bold green][cyan]snoopproject@ya.ru[/cyan]
""",
                        title="[bold red]demo: (Публичная оферта)",
                        border_style="bold blue"))

    try:
        webbrowser.open("https://yoomoney.ru/to/4100111364257544")
    except Exception:
        logger.info("\CONSTANT_33[31;1mНе удалось открыть браузер\CONSTANT_33[0m")

    logger.info(Style.BRIGHT + Fore.RED + "Выход")
    sys.exit()


## Buy.
def buy():
    donate_buy = """
<script>
function bay() {document.write('\
<html>\
<head>\
	<title>💳 Donate/Buy Snoop Project</title>\
</head>\
<body style=\"background-color: #c0c0c0\">\
<p><span style="color:#9a7c"><big>╭</big><span style="font-size:36px">Donate/Buy</span>:</span><br />\
<span style="color:#9a7c"><big>├──</big>ЮMoney::</span> <a href="https://yoomoney.ru/to/4100111364257544" target="_blank">CONSTANT_4100111364257544</a><br />\
<span style="color:#9a7c"><big>├──</big>Сбер_карта:: </span><strong>CONSTANT_2202208013277075</strong><br />\
<span style="color:#9a7c"><big>├──</big>Raiffeisen_card:: </span><strong>CONSTANT_2200300512321074</strong><br />\
<span style="color:#9a7c"><big>├──</big>По номеру телефона <em>(СБП: банк Юмани)</em>:: </span><strong>+CONSTANT_79004753581</strong><br />\
<span style="color:#9a7c"><big>└──</big>СберБанк Онлайн <em>(мобильное приложение)</em>:: </span><strong>QR код</strong><br />\
<img alt="QR код только для пользователей Сбербанк Онлайн." src="https://raw.githubusercontent.com/snooppr/snoop/refs/heads/master/web/QR_donate_SberBank.png" style="height:200px; width:200px" /></p>\
\
<p><span style="font-size:18px"><span style="color:#7500">Оплатить софт можно по <u>любым реквизитам</u>, но самым предпочтительным способом является &mdash; СБП <em>(перевод по номеру телефона без комиссий с карты любого банка)</em>.</span></span></p>\
\
<p><span style="font-size:18px"><span style="color:#7500">Если пользователя заинтересовало ПО Snoop demo version, то он может приобрести <strong>Snoop full version</strong>, поддержав развитие IT-проекта <strong>20$</strong> или <strong>1600р</strong>.<br />\
При пожертвовании/покупке в сообщении/письме укажите:</span></span></p>\
\
<p><span style="font-size:18px">&nbsp;&nbsp;&nbsp; \\&quot;\\&quot;\\&quot;<br />\
<span style="color:#9a7c">&nbsp;&nbsp;&nbsp; На развитие Snoop Project: ваш <strong>e-mail</strong>,<br />\
&nbsp;&nbsp;&nbsp; full <strong>version</strong> for Windows или full version for Linux,<br />\
&nbsp;&nbsp;&nbsp; <strong>статус</strong> пользователя: Физ.лицо; ИП; Юр.лицо <em>(если покупка ПО)</em>.</span><br />\
&nbsp;&nbsp;&nbsp; \\&quot;\\&quot;\\&quot;</span></p>\
\
<p><span style="font-size:18px"><span style="color:#7500">В ближайшее время на email пользователя придёт чек о покупке и ссылка для скачивания Snoop full version готовой сборки, <br>\
то есть исполняемого файла, для Windows &mdash; это &#39;snoop_cli.exe&#39;, для GNU/Linux &mdash; &#39;snoop_cli.bin&#39;.</span></span></p>\
\
<p><span style="font-size:18px"><span style="color:#7500">Snoop в исполняемом виде <em>(build-версия)</em> предоставляется по лицензии, с которой пользователь должен ознакомиться перед покупкой ПО.<br />\
Лицензия для Snoop Project в исполняемом виде находится в rar-архивах демо версий Snoop по ссылке:</span><br />\
<a href="https://github.com/snooppr/snoop/releases" target="_blank">https://github.com/snooppr/snoop/releases</a> <span style="color:#7500">, также лицензия доступна по команде::<br />\
&#39;</span><strong><span style="color:#16a085">snoop_cli.bin --version</span></strong><span style="color:#7500">&#39; или &#39;</span><strong><span style="color:#16a085">snoop_cli.exe --version</span></strong><span style="color:#7500">&#39; у исполняемого файла.</span></span></p>\
\
<p><span style="font-size:18px"><span style="color:#7500">Если софт требуется пользователю для служебных или образовательных задач, например, десять лицензий на ПО для ВУЗа, напишите письмо на e-mail разработчика в свободной форме.<br />\
Всем студентам <em>(независимо от учебного заведения или направления)</em> ПО Snoop full version предоставляется с <strong>50%</strong> скидкой.</span></span></p>\
\
<p><span style="font-size:18px"><span style="color:#7500">Snoop full version:</span></span></p>\
\
<ul>\
	<li><span style="font-size:18px"><span style="color:#7500">&nbsp;CONSTANT_4700+ Websites;</span></span></li>\
	<li><span style="font-size:18px"><span style="color:#7500">&nbsp;поддержка локальной и онлайн database Snoop;</span></span></li>\
	<li><span style="font-size:18px"><span style="color:#7500">&nbsp;подключение к БД Snoop (online), которая расширяется/обновляется;</span></span></li>\
	<li><span style="font-size:18px"><span style="color:#7500">&nbsp;доступен автооптимизированный, быстрый и агрессивный режим поиска;</span></span></li>\
	<li><span style="font-size:18px"><span style="color:#7500">&nbsp;доступна пользовательская настройка разгона скорости работы ПО;</span></span></li>\
	<li><span style="font-size:18px"><span style="color:#7500">&nbsp;плагины без ограничений;</span></span></li>\
	<li><span style="font-size:18px"><span style="color:#7500">&nbsp;ru техподдержка от разработчика ПО;</span></span></li>\
    <li><span style="font-size:18px"><span style="color:#7500">&nbsp;предоставление обновлённых билдов;</span></span></li>\
	<li><span style="font-size:18px"><span style="color:#7500">&nbsp;отключены всплывающие окна в HTML-отчёте про упоминание Snoop demo version.</span></span></li>\
</ul>\
\
<p><span style="font-size:18px"><span style="color:#e74c3c">Ограничения Snoop demo version:</span></span></p>\
\
<ul>\
	<li><span style="font-size:18px"><span style="color:#e74c3c">database Snoop сокращена в &gt; 15 раз;</span></span></li>\
	<li><span style="font-size:18px"><span style="color:#e74c3c">необновляемая database Snoop;</span></span></li>\
	<li><span style="font-size:18px"><span style="color:#e74c3c">отключены некоторые опции/плагины.</span></span></li>\
</ul>\
\
<p><span style="font-size:18px"><span style="color:#7500">Email:</span> <span style="color:#9a7c"><strong>snoopproject@protonmail.com</strong></span><br />\
<span style="color:#7500">Исходный код: </span><a href="https://github.com/snooppr/snoop" target="_blank">https://github.com/snooppr/snoop</a></span></p>\
\
<p><span style="font-size:18px">❗️<span style="color:#e15700">Обратите внимание, что из-за цензуры письма с &#39;mailru&#39; и &#39;yandex&#39; не доходят до международного почтового сервиса &#39;protonmail&#39;. <br>\
Пользователи mailru/yandex пишите запросы на запасную почту.</span><br />\
<span style="color:#7500">Email:</span><span style="color:#9900"> </span><span style="color:#9a7c"><strong>snoopproject@ya.ru</strong></span></span></p>\
<hr />\
<p>Возврат: &#39;F5&#39;</p>\
</body>\
</html>')}
</script>"""
    return donate_buy

## Лого.
def logo(text, color="\CONSTANT_33[31;1m", exit=True):
    if sys.platform != 'win32':
        with console.screen():
            console.print("""[cyan]
 ____                                      
/\\  _`\\                                    
\\ \,\L\\_\\    ___     ___     ___   _____   
 \\/_\\__ \\  /' _ `\\  / __`\\  / __`\\/\\ '__`\\
   /\\ \L\\ \\/\\ \\/\\ \\/\\ \\_\\ \\/\\ \\_\\ \\ \\ \L\\ \\
   \\ `\\____\\ \\_\\ \\_\\ \\____/\\ \\____/\\ \\ ,__/
    \\/_____/\\/_/\\/_/\\/___/  \\/___/  \\ \\ \\/ 
                                     \\ \\_\\
      __                              \\/_/ 
     /\\ \\                              
     \\_\\ \\     __    ___ ___     ___   
     /'_` \\  /'__`\\/' __` __`\\  / __`\\
    /\\ \\_\\ \\/\\  __//\\ \\/\\ \\/\\ \\/\\ \\_\\ \\
    \\ \\___,_\\ \\____\\ \\_\\ \\_\\ \\_\\ \\____/
     \\/__,_ /\\/____/\\/_/\\/_/\\/_/\\/___/ 
""")
            time.sleep(1.4)
    for i in text:
        time.sleep(0.04)
        logger.info(f"{color}{i}", end='', flush=True)
    if exit:
        logger.info("\CONSTANT_33[31;1m\n\nВыход")
        sys.exit()


# snoop.py Справка Модули 'if mod == 'help'.
def help_module_1():
    print("""\CONSTANT_33[32;1m└──[Справка]\CONSTANT_33[0m

\CONSTANT_33[32;1m========================
| Плагин GEO_IP/domain |
========================\CONSTANT_33[0m \CONSTANT_33[32m\n
1) Реализует онлайн одиночный поиск цели по IP/url/domain и предоставляет статистическую информацию: IPv4/v6; GEO-координаты/ссылку; локацию.
(Лёгкий ограниченный поиск).

2) Реализует онлайн поиск цели по списку данных: и предоставляет статистическую и визуализированную информацию: IPv4/v6; GEO-координаты/ссылки; страны/города; отчеты в CLI/txt/csv форматах; предоставляет визуализированный отчет на картах OSM.
(Умеренный небыстрый поиск: ограничения запросов:: 15к/час; не предоставляет информацию о провайдерах).

3) Реализует офлайн поиск цели по списку данных, используя БД: и предоставляет статистическую и визуализированную информацию: IPv4/v6; GEO-координаты/ссылки; локации; провайдеры; отчеты в CLI/txt/csv форматах; предоставляет визуализированный отчет на картах OSM.
(Сильный и быстрый поиск).

Результаты по 1 и 2 методу могут отличаться и быть неполными - зависит от персональных настроек DNS/IPv6 пользователя.
Список данных — текстовый файл (в кодировке utf-8), который пользователь указывает в качестве цели, и который содержит ip, domain или url (или их комбинации).

Предназначение плагина — Образование/ИБ.

\CONSTANT_33[32;1m============================
| Плагин Reverse Vgeocoder |
============================\CONSTANT_33[0m\n
\CONSTANT_33[32mОбратный impresionante-геокодер от Snoop Project для визуализации координат на карте OSM и статистическим анализом в html/csv/txt форматах.

Плагин умеет извлекать и обрабатывать координаты из любых зашумлённых текстовых файлов. Плагин реализует оффлайн поиск цели по заданным геокоординатам и предоставляет подробную статистическую и визуализированную информацию (full version).
Особая повышенная точность у объектов в зоне RU; EU; CIS локаций относительно остального мира.

С помощью данного плагина (full version) пользователь способен извлечь, визуализировать и проанализировать информацию о тысячах геокоординатах за секунды.

Предназначение плагина — CTF/Образование.\CONSTANT_33[0m

\CONSTANT_33[32;1m========================
| Плагин Yandex_parser |
========================\CONSTANT_33[0m\n
\CONSTANT_33[32mПлагин позволяет получить информацию о пользователях Яндекс-сервисов:
Я_Отзывы; Я_Кью; Я_Маркет; Я_Музыка; Я_Дзен; Я_Диск; E-mail, Name.
И связать полученные данные между собой с высокой скоростью и масштабно.

Плагин разработан на идее и материалах уязвимости, отчёты были отправлены Яндексу в рамках программы «Охота за ошибками» в CONSTANT_2020-CONSTANT_2021 гг.
Попал в зал славы, получил дважды финансовое вознаграждение, а Яндекс исправил 'ошибки' по своему усмотрению.

Предназначение плагина — OSINT.

Подробнее о плагинах см. 'Общее руководство Snoop Project.pdf'.\CONSTANT_33[0m""")
    console.rule("[bold red]Конец справки")


# snoopplugins.py Справка Модуль Reverse Vgeocoder 'elif Vgeo == "help"'.
def help_vgeocoder_vgeo():
    print("""\CONSTANT_33[32;1m└──[Справка]\CONSTANT_33[0m
\CONSTANT_33[32m
В Snoop Project поддерживается два режима геокодирования:
[*] Метод '\CONSTANT_33[32;1mПростой\CONSTANT_33[0m\CONSTANT_33[32m':: На карте OSM (урезанный HTML-отчет) расставляются маркеры по координатам.
Все маркеры подписаны геометками.
Для данного метода доступны сокращенные отчёты с геометками в html/txt форматах.

[*] Метод '\CONSTANT_33[32;1mПодробный\CONSTANT_33[0m\CONSTANT_33[32m':: На карте OSM (HTML-отчет) расставляются маркеры по координатам.
Все маркеры подписаны геометками; странами; округами и городами. Доступны графики по странам/регионам, статистика и её фильтрация.
Дополнительные отчёты (таблицы) сохраняются с подробностями в [.txt.csv] форматах.
Данный метод точно расставляет маркеры с геометками, подписывает их адресами к ближайшим населенным пунктам или названиями природных объектов.
Особая повышенная точность у объектов в зоне RU; EU; CIS локаций относительно остального мира.

    Например, если пользователь загрузит для обработки координаты, указывающие в километре от г. Выкса на местность возле озера Разодейское, то маркер на карте OSM встанет точно у озера, а подписан он будет примерно так:

\"\"\"\CONSTANT_33[36m
🌎 Координаты: 55.342595 42.230801
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Страна: RU
Регион: Nizhny Novgorod Oblast
Округ: Ozero Razodeyskoye\CONSTANT_33[0m\CONSTANT_33[32m
\"\"\"

Метод работает на основе — 'Евклидово дерево'.

\CONSTANT_33[32;1mПлагин Reverse Vgeocoder\CONSTANT_33[0m \CONSTANT_33[32m- работает в оффлайн режиме и укомплектован специально разработанной гео-БД (некоторые БД предоставляются под свободной лицензией от download.geonames.org/export/dump/).

    Для обработки данных укажите при запросе текстовый файл с координатами в градусах в кодировке utf-8 (с расширением .txt или без расширения). Каждая строчка с геокоординатами (широта, долгота) должна быть записана в файле с новой строки (желательно).
Snoop довольно умён: распознаёт и выбирает геокоординаты через запятую, пробел'ы или делает интеллектуальную выборку, вычищая случайные строки.
    Пример файла с геокоординатами (как может выглядеть файл с координатами, который необходимо указывать):

\"\"\"\CONSTANT_33[36m
51.352,   -CONSTANT_108.625
55.466,64.776
52.40662,66.77631
53.28 -CONSTANT_104.680
54.505/73.773
Москва55.75, 37.62 Калининград54.71, 20.51 Ростов-на-Дону47.23, 39.72
случайная_строка1, которая_будет обработана Казань 55.7734/49.1436
случайная строка2, которая не будет обработана\CONSTANT_33[0m\CONSTANT_33[32m
\"\"\"

    По окончанию рендеринга откроется web-browser с визуальным результатом.
Все результаты сохраняются в '~/snoop/results/plugins/ReverseVgeocoder/*[.txt.html.csv]'.
Для статистической обработки информации (сортировка по странам/координатам/raw_данным и т.д.) пользователь может изучить отчёт в csv-формате.
Если графики не отображаются в вашем html-отчёте, попробуйте открыть репорт в другом браузере.
    Это удобный плагин, если пользователю необходимо, например, не только обработать геокоординаты, но и найти хаотичные данные, или наоборот.""")


# snoopplugins.py Справка Модуль Reverse Vgeocoder 'elif Ya == "help"'.
def help_yandex_parser():
    print("""\CONSTANT_33[32;1m└──[Справка]

Однопользовательский режим\CONSTANT_33[0m
\CONSTANT_33[32m[*] Логин — левая часть до символа '@', например, bobbimonov@ya.ru, логин
'\CONSTANT_33[36mbobbimonov\CONSTANT_33[0m\CONSTANT_33[32m'.
[*] Публичная ссылка на Яндекс.Диск — это ссылка для скачивания/просмотра материалов, которую пользователь выложил в публичный доступ, например,
'\CONSTANT_33[36mhttps://yadi.sk/d/7C6Z9q_Ds1wXkw\CONSTANT_33[0m\CONSTANT_33[32m' или '\CONSTANT_33[36mhttps://disk.yandex.ru/d/7C6Z9q_Ds1wXkw\CONSTANT_33[0m\CONSTANT_33[32m'.
[*] Идентификатор — хэш, который указан в url на странице пользователя, например, в сервисе Я.Район: 'https://local.yandex.ru/users/tr6r2c8ea4tvdt3xmpy5atuwg0/' идентификатор — '\CONSTANT_33[36mtr6r2c8ea4tvdt3xmpy5atuwg0\CONSTANT_33[0m\CONSTANT_33[32m'.
    По окончанию успешного поиска выводится отчёт в CLI и открываются Яндекс-страницы пользователя в браузере.
    Плагин Yandex_parser выдает меньше информации по идентификатор-у пользователя (в сравнении с другими методами), причина — fix уязвимости от Яндекса.

\CONSTANT_33[32;1mМногопользовательский режим\CONSTANT_33[0m
\CONSTANT_33[32m[*] Файл с именами пользователей — файл (в кодировке UTF-8 с расширением .txt или без него), в котором записаны логины.
Каждый логин в файле должен быть записан с новой строки, например:

\"\"\"
\CONSTANT_33[36mbobbimonov
username
username2
username3
случайная строка
bobbimonov@ya.ru
bobbimonov@ya.ru
bobbimonov@ya.ru\CONSTANT_33[0m
\CONSTANT_33[32m\"\"\"

    При использовании многопользовательского режима по окончанию поиска (быстро) выводится расширенный отчёт в CLI, сохраняется txt-отчёт о Яндекс-пользователях (с расширенными, структурированными данными) и открывается браузер с мини-отчётом (сгруппированные данные).
    Плагин генерирует, но не проверяет 'доступность' персональных страниц пользователей по причине: частая защита страниц Я.капчей.
Все результаты сохраняются в '\CONSTANT_33[36m~/snoop/results/plugins/Yandex_parser/*\CONSTANT_33[0m\CONSTANT_33[32m'\CONSTANT_33[0m
    \CONSTANT_33[31;1mВ конце ноября CONSTANT_2022 года Яндекс закрыл публичный api, и возможно, данный плагин больше не заработает...\CONSTANT_33[0m""")


# snoopplugins.py Справка Модуль GEO_IP/domain 'elif dipbaza'.
def geo_ip_domain():
    logger.info("\CONSTANT_33[32;1m└──Справка\CONSTANT_33[0m\n")
    logger.info("""\CONSTANT_33[32m[*] Режим '\CONSTANT_33[32;1mOnline поиск\CONSTANT_33[0m\CONSTANT_33[32m'. Модуль GEO_IP/domain от Snoop Project использует публичный api и создает статистическую и визуализированную информацию по ip/url/domain цели (массиву данных).
    Ограничения: запросы ~15к/час, невысокая скорость обработки данных, отсутствие информации о провайдерах.
    Преимущества использования 'Online поиска': в качестве входных данных можно использовать не только ip-адреса, но и domain/url.
    Пример файла с данными (список.txt):

\"\"\"
\CONSTANT_33[36m1.1.1.1
CONSTANT_2606:CONSTANT_2800:CONSTANT_220:1:CONSTANT_248:CONSTANT_1893:25c8:CONSTANT_1946
google.com
https://example.org/fo/bar/CONSTANT_7564
случайная строка\CONSTANT_33[0m
\CONSTANT_33[32m\"\"\"\CONSTANT_33[0m

\CONSTANT_33[32m[*] Режим '\CONSTANT_33[32;1mOffline поиск\CONSTANT_33[0m\CONSTANT_33[32m'. Модуль GEO_IP/domain от Snoop Project использует специальные базы данных и создает статистическую и визуализированную информацию по ip цели (массиву данных т.е. по ip-адресам).
Преимущества использования 'Offline поиска': скорость (обработка тысяч ip без задержек), стабильность (отсутствие зависимости от интернет соединения и персональных настроек DNS/IPv6 пользователя), масштабный охват/покрытие (предоставляется информация об интернет-провайдерах).

[*] Режим '\CONSTANT_33[32;1mOffline_тихий поиск\CONSTANT_33[0m\CONSTANT_33[32m'. Тот же режим, что и режим 'Offline', но не выводит на печать в CLI промежуточные таблицы с данными. Режим даёт прирост производительности в несколько раз.
    Пример файла с данными (список.txt):

\"\"\"
\CONSTANT_33[36m8.8.8.8
93.184.216.34
CONSTANT_2606:CONSTANT_2800:CONSTANT_220:1:CONSTANT_248:CONSTANT_1893:25c8:CONSTANT_1946
случайная строка\CONSTANT_33[0m
\CONSTANT_33[32m\"\"\"

    Snoop довольно умён и способен определять и различать во входных данных: IPv4/v6/domain/url, вычищая ошибки и случайные строки.
    По окончанию обработки данных пользователю предоставляются:
статистические отчеты в [txt/csv/html и визуализированные данные на карте OSM]. Если графики не отображаются в вашем html-отчёте, попробуйте открыть репорт в другом браузере.
    Примеры для чего можно использовать модуль GEO_IP/domain от Snoop Project.
Например, если у пользователя имеется список ip адресов от DDoS атаки,
он может проанализировать откуда исходила  max/min атака и от кого (провайдеры).
Решая квесты-CTF, где используются GPS/IPv4/v6.
В конечном итоге использовать плагин в образовательных целях или из естественного любопытства (проверить любые ip-адреса и их принадлежность к провайдеру и местности).\CONSTANT_33[0m""")
