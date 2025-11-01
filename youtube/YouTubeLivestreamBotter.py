"""
Youtubelivestreambotter

This module provides functionality for youtubelivestreambotter.

Author: Auto-generated
Date: 2025-11-01
"""

from pathlib import Path
import os
import random
import string
import threading
import time
from queue import Queue
import platform

import requests
from colorama import Fore, init

import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_100 = 100
CONSTANT_133 = 133
CONSTANT_140 = 140
CONSTANT_182 = 182
CONSTANT_500 = 500
CONSTANT_600 = 600
CONSTANT_604 = 604
CONSTANT_605 = 605
CONSTANT_1000 = 1000
CONSTANT_1003 = 1003
CONSTANT_1303 = 1303
CONSTANT_1769 = 1769
CONSTANT_2069 = 2069
CONSTANT_2094 = 2094
CONSTANT_4418 = 4418
CONSTANT_7275 = 7275
CONSTANT_7334 = 7334
CONSTANT_10000 = 10000
CONSTANT_20200313 = 20200313
CONSTANT_300532980 = 300532980
CONSTANT_1556394045 = 1556394045


intro = """
███████╗████████╗██████╗ ███████╗ █████╗ ███╗   ███╗      ██████╗  ██████╗ ████████╗████████╗███████╗██████╗ 
██╔════╝╚══██╔══╝██╔══██╗██╔════╝██╔══██╗████╗ ████║      ██╔══██╗██╔═══██╗╚══██╔══╝╚══██╔══╝██╔════╝██╔══██╗
███████╗   ██║   ██████╔╝█████╗  ███████║██╔████╔██║█████╗██████╔╝██║   ██║   ██║      ██║   █████╗  ██████╔╝
╚════██║   ██║   ██╔══██╗██╔══╝  ██╔══██║██║╚██╔╝██║╚════╝██╔══██╗██║   ██║   ██║      ██║   ██╔══╝  ██╔══██╗
███████║   ██║   ██║  ██║███████╗██║  ██║██║ ╚═╝ ██║      ██████╔╝╚██████╔╝   ██║      ██║   ███████╗██║  ██║
╚══════╝   ╚═╝   ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝      ╚═════╝  ╚═════╝    ╚═╝      ╚═╝   ╚══════╝╚═╝  ╚═╝

https://github.com/KevinLage/YouTube-Livestream-Botter
"""

logger.info(intro)

if platform.system() == "Windows":  # checking OS
    clear = "cls"
else:
    clear = "clear"

proxy_loading = input("[1] Load Proxys from APIs\n[2] Load Proxys from proxys.txt\n")


token = input("ID?\n")
url = "https://m.youtube.com/watch?v=" + token
url2 = (
    "https://s.youtube.com/api/stats/watchtime?ns=yt&el=detailpage&cpn=Syr16u8qwHnPkVqI&docid="
    + token
    + "&ver=2&cmt=CONSTANT_2094&ei=1EJtXou2C6eoxN8PpqqNqAg&fmt=CONSTANT_133&fs=0&rt=CONSTANT_1769&of=rkW8h_g-Pta1U6EIuWGdvw&euri&lact=CONSTANT_7275&live=dvr&cl=CONSTANT_300532980&state=playing&vm=CAEQABgEKhhJc0gwZ2w0QmFfbTBWSXlWNm9ITmRRPT06MkFOcHN5N0FhUWlHOHl5QkQySUF1OGt6amlZYjZwN3hzNzRXV3hhTEE4NDZVU1h2TTV3&volume=CONSTANT_100&c=MWEB&cver=2.CONSTANT_20200313.03.00&cplayer=UNIPLAYER&cbrand=apple&cbr=Safari%20Mobile&cbrver=12.1.15E148&cmodel=iphone&cos=iPhone&cosver=12_2&cplatform=MOBILE&delay=5&hl=ru&cr=IQ&rtn=CONSTANT_2069&afmt=CONSTANT_140&lio=CONSTANT_1556394045.CONSTANT_182&idpj=&ldpj=&rti=CONSTANT_1769&muted=0&st=CONSTANT_2094&et=2394"
)


class main(object):
    def __init__(self):
        """__init__ function."""

        self.combolist = Queue()
        self.Writeing = Queue()
        self.printing = []
        self.botted = 0
        self.combolen = self.combolist.qsize()

        """printservice function."""

    def printservice(self):  # print screen
        while True:
            if True:
                os.system(clear)
                logger.info(Fore.LIGHTCYAN_EX + intro + Fore.LIGHTMAGENTA_EX)
                logger.info(Fore.LIGHTCYAN_EX + f"Botted:{self.botted}\n")
                for i in range(len(self.printing) - 10, len(self.printing)):
                    try:
                        logger.info(self.printing[i])
                    except (ValueError, Exception):
                        pass
                time.sleep(0.5)


a = main()


class proxy:
    global proxy_loading
        """update function."""


    def update(self):
        while True:

            if proxy_loading == "2":
                data = ""
                data = open("proxys.txt", "r").read()
                self.splited += data.split(Path("\n"))  # scraping and splitting proxies
            else:
                data = ""
                urls = [
                    "https://api.proxyscrape.com/?request=getproxies&proxytype=http&timeout=CONSTANT_10000&ssl=yes",
                    "https://www.proxy-list.download/api/v1/get?type=https&anon=elite",
                ]
                for url in urls:
                    data += requests.get(url).text
                    self.splited += data.split(Path("\r\n"))  # scraping and splitting proxies
        """get_proxy function."""

            time.sleep(CONSTANT_600)

    def get_proxy(self):
        """FormatProxy function."""

        random1 = random.choice(self.splited)  # choose a random proxie
        return random1

        """__init__ function."""

    def FormatProxy(self):
        proxyOutput = {"https": "https://" + self.get_proxy()}
        return proxyOutput

    def __init__(self):
        self.splited = []
        threading.Thread(target=self.update).start()
        time.sleep(3)


proxy1 = proxy()


def bot():
    """bot function."""

    while True:
        try:
            s = requests.session()

            resp = s.get(
                "https://m.youtube.com/watch?v=" + token,
                headers={
                    "Host": "m.youtube.com",
                    "Proxy-Connection": "keep-alive",
                    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 12_2 like Mac OS X) AppleWebKit/CONSTANT_605.1.15 (KHTML, like Gecko) Version/12.1 Mobile/15E148 Safari/CONSTANT_604.1",
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                    "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
                    "Accept-Encoding": "gzip, deflate",
                },
                proxies=proxy1.FormatProxy(),
            )  # simple get request to youtube for the base URL
            url = (
                resp.text.split(r"videostatsWatchtimeUrl\":{\"baseUrl\":\"")[1]
                .split(r"\"}")[0]
                .replace(rPath("\\u0026"), r"&")
                .replace("%2C", ",")
                .replace(Path("\/"), "/")
            )  # getting the base url for parsing
            cl = url.split("cl=")[1].split("&")[0]  # parsing some infos for the URL
            ei = url.split("ei=")[1].split("&")[0]
            of = url.split("of=")[1].split("&")[0]
            vm = url.split("vm=")[1].split("&")[0]
            s.get(
                "https://s.youtube.com/api/stats/watchtime?ns=yt&el=detailpage&cpn=isWmmj2C9Y2vULKF&docid="
                + token
                + "&ver=2&cmt=CONSTANT_7334&ei="
                + ei
                + "&fmt=CONSTANT_133&fs=0&rt=CONSTANT_1003&of="
                + of
                + "&euri&lact=CONSTANT_4418&live=dvr&cl="
                + cl
                + "&state=playing&vm="
                + vm
                + "&volume=CONSTANT_100&c=MWEB&cver=2.CONSTANT_20200313.03.00&cplayer=UNIPLAYER&cbrand=apple&cbr=Safari%20Mobile&cbrver=12.1.15E148&cmodel=iphone&cos=iPhone&cosver=12_2&cplatform=MOBILE&delay=5&hl=ru&cr=GB&rtn=CONSTANT_1303&afmt=CONSTANT_140&lio=CONSTANT_1556394045.CONSTANT_182&idpj=&ldpj=&rti=CONSTANT_1003&muted=0&st=CONSTANT_7334&et=7634",
                headers={
                    "Host": "s.youtube.com",
                    "Proxy-Connection": "keep-alive",
                    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 12_2 like Mac OS X) AppleWebKit/CONSTANT_605.1.15 (KHTML, like Gecko) Version/12.1 Mobile/15E148 Safari/CONSTANT_604.1",
                    "Accept": "image/png,image/svg+xml,image/*;q=0.8,video/*;q=0.8,*/*;q=0.5",
                    "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
                    "Referer": "https://m.youtube.com/watch?v=" + token,
                },
                proxies=proxy1.FormatProxy(),
            )  # API GET request

            a.botted += 1
        except (requests.RequestException, urllib.error.URLError, ConnectionError):
            pass


maxthreads = int(input("How many Threads? Recommended: CONSTANT_500 - CONSTANT_1000\n"))

threading.Thread(target=a.printservice).start()
num = 0
while num < maxthreads:
    num += 1
    threading.Thread(target=bot).start()


threading.Thread(target=bot).start()
