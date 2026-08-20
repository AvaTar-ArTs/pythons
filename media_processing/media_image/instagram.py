# TODO: Resolve circular dependencies by restructuring imports

# String constants
DEFAULT_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
ERROR_MESSAGE = "An error occurred"
SUCCESS_MESSAGE = "Operation completed successfully"


# Constants
DEFAULT_TIMEOUT = 30
MAX_RETRIES = 3
DEFAULT_PORT = 8080


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


@dataclass
class DependencyContainer:
    """Simple dependency injection container."""
    _services = {}

    @classmethod
    def register(cls, name: str, service: Any) -> None:
        """Register a service."""
        cls._services[name] = service

    @classmethod
    def get(cls, name: str) -> Any:
        """Get a service."""
        if name not in cls._services:
            raise ValueError(f"Service not found: {name}")
        return cls._services[name]


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

from functools import lru_cache

@dataclass
class SingletonMeta(type):
    """Thread-safe singleton metaclass."""
    _instances = {}
    _lock = threading.Lock()

@lru_cache(maxsize = 128)
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            with cls._lock:
                if cls not in cls._instances:
                    cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

    import html
from builtins import print
from colorama import init
from datetime import datetime
from functools import lru_cache
from random import randint
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from termcolor import colored
from time import sleep
from typing import Any, Dict, List, Optional, Union, Tuple, Callable
import asyncio
import getpass
import json
import logging
import os
import requests
import threading
import urllib.request

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
    DPI_300 = DPI_300
    DPI_72 = 72
    KB_SIZE = KB_SIZE
    MB_SIZE = 1048576
    GB_SIZE = 1073741824
    DEFAULT_TIMEOUT = DEFAULT_TIMEOUT
    MAX_RETRIES = MAX_RETRIES
    DEFAULT_BATCH_SIZE = DEFAULT_BATCH_SIZE
    MAX_FILE_SIZE = 9437184
    DEFAULT_QUALITY = DEFAULT_QUALITY
    DEFAULT_WIDTH = DEFAULT_WIDTH
    DEFAULT_HEIGHT = DEFAULT_HEIGHT
    logger = logging.getLogger(__name__)
    menu = self.configGetir("languages.{dil}.menu".format(dil
    base_warnings = self.BASE_UYARI(metod
    base_inputs = self.BASE_UYARI(metod
    secim = input(self.configGetir(base_inputs + "input1")).strip()
    secim = int(secim)
    base_warnings = self.BASE_UYARI(metod
    secimler = self.configGetir(
    base_warnings = self.BASE_UYARI(metod
    base_inputs = self.BASE_UYARI(metod
    kullanici = input(self.configGetir(base_inputs + "input1")).strip()
    ilkGonderi = self.driver.find_elements_by_css_selector("article div.v1Nh3")[0]
    base_warnings = self.BASE_UYARI(metod
    base_sleep = self.BASE_SLEEP(metod
    gonderiSayisi = self.gonderiSayisi()
    gonderiSayisi = int(self.metindenKarakterSil(gonderiSayisi, ", "))
    tempIndex = self.index
    kullanici = kullanici, hata
    base_warnings = self.BASE_UYARI(metod
    base_sleep = self.BASE_SLEEP(metod
    gonderiSayisi = self.gonderiSayisi()
    gonderiSayisi = int(self.metindenKarakterSil(gonderiSayisi, ", "))
    btn_begen = self.begenButon()
    begeniDurum = self.begenButonuDurumGetir(btn_begen)
    index = str(self.index), url
    url = self.driver.current_url
    index = str(self.index), url
    url = self.driver.current_url
    kullanici = kullanici
    kullanici = kullanici
    kullanici = kullanici, hata
    kullanici = kullanici, hata
    base_warnings = self.BASE_UYARI(metod
    base_sleep = self.BASE_SLEEP(metod
    btn_takipEdilenler = self.takipEdilenlerButon()
    takipEdilenSayisi = btn_takipEdilenler.find_element_by_css_selector("span.g47SY").text
    takipEdilenSayisi = int(self.metindenKarakterSil(takipEdilenSayisi, ", "))
    devamEtsinMi = True
    dialog_popup = self.driver.find_element_by_css_selector("div.pbNvD")
    takipListe = dialog_popup.find_elements_by_css_selector("div.PZuss > li")
    btn_takip = takip.find_element_by_css_selector("button.sqdOP")
    btn_onay = self.driver.find_element_by_css_selector(
    kullanici = takipEdilenKullanıcıAdi, hata
    index = self.index, kullanici
    devamEtsinMi = False
    sleep3 = self.configGetir("{base}sleep3".format(base
    hata = str(error)
    base_warnings = self.BASE_UYARI(metod
    base_inputs = self.BASE_UYARI(metod
    base_sleep = self.BASE_SLEEP(metod
    sleep1 = self.configGetir(base_sleep + "sleep1")
    url = input(self.configGetir(base_inputs + "input1")).strip()
    yorumSayisi = input(self.configGetir(base_inputs + "input2")).strip()
    yorumSayisi = int(yorumSayisi)
    yorumSayisi = 50
    secilenIslem = str(input(self.configGetir(base_inputs + "input3")).strip())
    yorum = self.rastgeleYorumGetir()
    yorum = self.yorumUzunlukBelirle(yorum)
    dosya = self.dosyaSec()
    yorumlar = self.dosyaIceriginiAl(dosya)
    yorum = self.yorumUzunlukBelirle(yorum)
    index = index + 1
    url = url, yorumSayisi
    base_warnings = self.BASE_UYARI(metod
    takipciler = self.takipcileriGetir()
    base_warnings = self.BASE_UYARI(metod
    base_sleep = self.BASE_SLEEP(metod
    devamEtsinMi = True
    silinenMesajlar = set()
    mesajListesi = self.driver.find_elements_by_css_selector("div.N9abW  a.rOtsg")
    kullaniciAdi = mesaj.find_element_by_css_selector(
    index = self.index, kullanici
    index = self.index, kullanici
    sleep1 = self.configGetir(base_sleep + "sleep1")
    base_warnings = self.BASE_UYARI(metod
    base_inputs = self.BASE_UYARI(metod
    base_sleep = self.BASE_SLEEP(metod
    url = input(self.configGetir(base_inputs + "input1")).strip()
    btn_oynat = self.driver.find_element_by_css_selector("button._42FBe")
    kullanici = self.driver.find_element_by_css_selector("a.FPmhX").get_attribute("title")
    base_warnings = self.BASE_UYARI(metod
    base_sleep = self.BASE_SLEEP(metod
    kullanici = kullanici
    kullanici = kullanici
    base_warnings = self.BASE_UYARI(metod
    base_inputs = self.BASE_UYARI(metod
    url = input(self.configGetir(base_inputs + "input1")).strip()
    kullanici = self.gonderiKullaniciAdi()
    base_warnings = self.BASE_UYARI(metod
    base_inputs = self.BASE_UYARI(metod
    base_sleep = self.BASE_SLEEP(metod
    hedefTakipciSayisi = None
    secilenIslem = str(input(self.configGetir(base_inputs + "input1")).strip())
    hedefTakipciSayisi = input(self.configGetir(base_inputs + "input2")).strip()
    hedefTakipciSayisi = int(hedefTakipciSayisi)
    kullanici = kullanici, secim
    kullanici = kullanici, secim
    devamEtsinMi = True
    takipciSayisi = self.driver.find_elements_by_css_selector(
    takipciSayisi = int(self.metindenKarakterSil(takipciSayisi, ", "))
    kaynakTakipciSayisi = self.driver.find_element_by_css_selector(
    kaynakTakipciSayisi = int(self.metindenKarakterSil(kaynakTakipciSayisi, ", "))
    takipciSayisi = self.hedefKaynaktanBuyukMu(
    btn_takipciler = self.takipcilerButon()
    kontrolEdilenKullanicilar = set()
    dialog_popup = self.driver.find_element_by_css_selector("div._1XyCr")
    takipciListe = dialog_popup.find_elements_by_css_selector("div.PZuss > li")
    takipciKullaniciAdi = takipci.find_element_by_css_selector(
    takipciKullaniciAdi = takipciKullaniciAdi.replace(
    btn_takip = takipci.find_element_by_css_selector("button.sqdOP")
    index = self.index, kullanici
    devamEtsinMi = False
    sleep2 = self.configGetir("{base}sleep2".format(base
    devamEtsinMi = False
    devamEtsinMi = False
    kullanici = kullanici, hata
    dosya = self.dosyaSec()
    kullanicilar = self.dosyaIceriginiAl(dosya)
    base_warnings = self.BASE_UYARI(metod
    base_inputs = self.BASE_UYARI(metod
    base_sleep = self.BASE_SLEEP(metod
    url = input(self.configGetir(base_inputs + "input1")).strip()
    hedefBegenenSayisi = None
    secilenIslem = str(input(self.configGetir(base_inputs + "input2")).strip())
    hedefBegenenSayisi = input(self.configGetir(base_inputs + "input3")).strip()
    hedefBegenenSayisi = int(hedefBegenenSayisi)
    devamEtsinMi = True
    begenenSayisi = self.driver.find_element_by_css_selector(
    begenenSayisi = int(self.metindenKarakterSil(begenenSayisi, ", "))
    kaynakBegenenSayisi = self.driver.find_element_by_css_selector(
    kaynakBegenenSayisi = int(
    begenenSayisi = int(
    btn_begenenler = self.driver.find_element_by_css_selector(
    kontrolEdilenKullanicilar = set()
    dialog_popup = self.driver.find_element_by_css_selector("div.pbNvD")
    begenenlerKullanicilar = dialog_popup.find_elements_by_css_selector(
    begenenKullaniciAdi = begenenKullanici.find_element_by_css_selector(
    begenenKullaniciAdi = begenenKullaniciAdi.replace(
    btn_takip = begenenKullanici.find_element_by_css_selector(
    index = self.index, kullanici
    devamEtsinMi = False
    sleep2 = self.configGetir("{base}sleep2".format(base
    devamEtsinMi = False
    devamEtsinMi = False
    secici = 'div[role
    base_warnings = self.BASE_UYARI(metod
    base_sleep = self.BASE_SLEEP(metod
    etiket = self.etiketGetir()
    limit = self.etiketeGoreIslemLimitiGetir(2)
    kaynakGonderiSayisi = int(
    limit = self.hedefKaynaktanBuyukMu(limit, kaynakGonderiSayisi)
    kullaniciAdi = self.driver.find_element_by_css_selector("div.e1e1d a.sqdOP").text
    btn_takip = self.driver.find_element_by_css_selector("div.bY2yH >button.sqdOP")
    index = self.index, kullanici
    sleep3 = self.configGetir("{base}sleep3".format(base
    kullanici = kullaniciAdi
    base_warnings = self.BASE_UYARI(metod
    base_sleep = self.BASE_SLEEP(metod
    etiket = self.etiketGetir()
    limit = self.etiketeGoreIslemLimitiGetir(1)
    kaynakGonderiSayisi = int(
    limit = self.hedefKaynaktanBuyukMu(limit, kaynakGonderiSayisi)
    btn_begen = self.begenButon()
    begeniDurum = self.begenButonuDurumGetir(btn_begen)
    index = self.index, url
    sleep3 = self.configGetir("{base}sleep3".format(base
    url = self.driver.current_url
    base_warnings = self.BASE_UYARI(metod
    base_inputs = self.BASE_UYARI(metod
    url = input(self.configGetir(base_inputs + "input1")).strip()
    url = input(self.configGetir(base_inputs + "input2")).strip()
    btn_begen = self.begenButon()
    begeniDurum = self.begenButonuDurumGetir(btn_begen)
    url = self.driver.current_url
    url = self.driver.current_url
    url = self.driver.current_url
    url = self.driver.current_url
    base_warnings = self.BASE_UYARI(metod
    base_inputs = self.BASE_UYARI(metod
    url = input(self.configGetir(base_inputs + "input1")).strip()
    yorum = input(self.configGetir(base_inputs + "input2")).strip()
    yorum = yorum[0:250]
    base_warnings = self.BASE_UYARI(metod
    kullanici = kullanici, hata
    kullanici = kullanici, hata
    base_warnings = self.BASE_UYARI(metod
    btnText = str(
    kullanici = kullanici
    kullanici = kullanici
    btnText = str(
    kullanici = kullanici
    kullanici = kullanici
    kullanici = kullanici, hata
    kullanici = kullanici, hata
    base_warnings = self.BASE_UYARI(metod
    base_inputs = self.BASE_UYARI(metod
    ayarlar = self.configGetir(
    secilenIslem = input(self.configGetir(base_inputs + "input1"))
    base_warnings = self.BASE_UYARI(metod
    base_warnings = self.BASE_UYARI(metod
    deger = self.config
    deger = deger[key]
    base_warnings = self.BASE_UYARI(metod
    base_inputs = self.BASE_UYARI(metod
    ayarlar = self.configGetir(
    secilenIslem = input(self.configGetir(base_inputs + "input1"))
    base_warnings = self.BASE_UYARI(metod
    base_inputs = self.BASE_UYARI(metod
    ayarlar = self.configGetir(
    secilenIslem = input(self.configGetir(base_inputs + "input1"))
    headless = self.configGetir("headless")
    durum = None
    durum = "Açık"
    durum = "Open"
    durum = "Kapalı"
    durum = "Close"
    base_warnings = self.BASE_UYARI(metod
    base_inputs = self.BASE_UYARI(metod
    ayarlar = self.configGetir(
    secilenIslem = input(self.configGetir(base_inputs + "input1"))
    base_warnings = self.BASE_UYARI(metod
    dil = "tr"
    dil = "en"
    veri = json.load(dosya)
    t1 = threading.Thread(target
    base_warnings = self.BASE_UYARI(metod
    firefox_options = Options()
    headless = self.configGetir("headless")
    firefox_profile = self.tarayiciDilDegistir(), 
    options = firefox_options, 
    executable_path = self.tarayiciPathGetir(), 
    profile = webdriver.FirefoxProfile()
    base_warnings = self.BASE_UYARI(metod
    base_inputs = self.BASE_UYARI(metod
    ayarlar = self.configGetir(
    secilenIslem = input(self.configGetir(base_inputs + "input1"))
    base_warnings = self.BASE_UYARI(metod
    base_inputs = self.BASE_UYARI(metod
    path = input(self.configGetir(base_inputs + "input1"))
    veri = json.load(dosya)
    base_warnings = self.BASE_UYARI(metod
    base_inputs = self.BASE_UYARI(metod
    ayarlar = self.configGetir(
    base = self.BASE_AYARLAR()
    secilenIslem = input(self.configGetir(base_inputs + "input1"))
    base_warnings = self.BASE_UYARI(metod
    headless = "true"
    headless = "false"
    veri = json.load(dosya)
    base_warnings = self.BASE_UYARI(metod
    base_sleep = self.BASE_SLEEP(metod
    takipciSayisi = self.takipciSayisiGetir()
    btn_takipciler = self.takipcilerButon()
    takipciler = set()
    devamEtsinMi = True
    dialog_popup = self.driver.find_element_by_css_selector("div.pbNvD")
    takipcilerPopup = dialog_popup.find_elements_by_css_selector("div.PZuss > li")
    takipciKullaniciAdi = takipci.find_element_by_css_selector(
    takipciKullaniciAdi = self.metindenKarakterSil(
    index = self.index, kullanici
    devamEtsinMi = False
    hata = str(error)
    btn_close_dialog = self.driver.find_element_by_css_selector("div.WaOAr >button.wpO6b")
    base_warnings = self.BASE_UYARI(metod
    base_sleep = self.BASE_SLEEP(metod
    takipEdilenSayisi = self.takipEdilenSayisiGetir()
    btn_takipEdilenler = self.takipEdilenlerButon()
    islemIndex = 0
    devamEtsinMi = True
    dialog_popup = self.driver.find_element_by_css_selector("div.pbNvD")
    takipListe = dialog_popup.find_elements_by_css_selector("div.PZuss > li")
    btn_takip = takip.find_element_by_css_selector("button.sqdOP")
    btn_onay = self.driver.find_element_by_css_selector(
    kullanici = takipEdilenKullanıcıAdi, 
    hata = str(error), 
    index = self.index, kullanici
    devamEtsinMi = False
    sleep3 = self.configGetir("{base}sleep3".format(base
    islemIndex = islemIndex + 1
    devamEtsinMi = False
    hata = str(error)
    takipEdilenSayisi = self.driver.find_elements_by_css_selector(
    takipciSayisi = self.driver.find_elements_by_css_selector(
    base_warnings = self.BASE_UYARI(metod
    base_inputs = self.BASE_UYARI(metod
    base_sleep = self.BASE_SLEEP(metod
    username = input(self.configGetir(base_inputs + "input1"))
    password = getpass.getpass(prompt
    username = input(self.configGetir(base_inputs + "input1"))
    password = getpass.getpass(prompt
    usernameInput = self.driver.find_elements_by_css_selector("form input")[0]
    passwordInput = self.driver.find_elements_by_css_selector("form input")[1]
    base_warnings = self.BASE_UYARI(metod
    base_warnings = self.BASE_UYARI(metod
    base_inputs = self.BASE_UYARI(metod
    base_sleep = self.BASE_SLEEP(metod
    kod = input(self.configGetir(base_inputs + "input1")).strip()
    kodInput = self.driver.find_elements_by_css_selector("form input")[0]
    base_warnings = self.BASE_UYARI(metod
    base_inputs = self.BASE_UYARI(metod
    etiket = input(self.configGetir(base_inputs + "input1")).strip()
    url = "{BASE_URL}explore/tags/{etiket}".format(
    BASE_URL = self.BASE_URL, etiket
    base_warnings = self.BASE_UYARI(metod
    base_inputs = self.BASE_UYARI(metod
    limit = input(self.configGetir(base_inputs + "input1")).strip()
    limit = input(self.configGetir(base_inputs + "input2")).strip()
    durum = self.driver.find_element_by_css_selector("div.RR-M-").get_attribute(
    base_warnings = self.BASE_UYARI(metod
    hikayeSayisi = self.driver.find_elements_by_css_selector("div.w9Vr-  > div._7zQEa")
    base_warnings = self.BASE_UYARI(metod
    base_sleep = self.BASE_SLEEP(metod
    url = self.driver.find_element_by_css_selector(
    foto_srcset = str(
    url = (foto_srcset.split(", ")[-1]).split(" ")[0]
    btn_ileri = self.driver.find_element_by_css_selector("button.ow3u_")
    base_warnings = self.BASE_UYARI(metod
    textarea = self.driver.find_element_by_class_name("Ypffh")
    textarea = self.driver.find_element_by_class_name("Ypffh")
    base_warnings = self.BASE_UYARI(metod
    base_warnings = self.BASE_UYARI(metod
    base = self.BASE_SLEEP(metod
    sleep1 = self.configGetir(base + "sleep1")
    base_sleep = self.BASE_SLEEP(metod
    base_warnings = self.BASE_UYARI(metod
    base_sleep = self.BASE_SLEEP(metod
    btn_takip = self.driver.find_element_by_css_selector("div.BY3EC >button")
    btn_text = str(btn_takip.text).lower()
    kullanici = kullanici
    kullanici = kullanici
    kullanici = kullanici
    kullanici = kullanici
    kullanici = kullanici
    btn_takip = self.driver.find_element_by_css_selector("span.vBF20 > button._5f5mN")
    btn_text = str(btn_takip.text).lower()
    kullanici = kullanici
    kullanici = kullanici
    ariaLabel = btn_takip.find_element_by_tag_name("span").get_attribute(
    kullanici = kullanici
    ariaLabel = btn_takip.find_element_by_tag_name("span").get_attribute(
    kullanici = kullanici
    kullanici = kullanici
    kullanici = kullanici
    base_sleep = self.BASE_SLEEP(metod
    sleep2 = self.configGetir("{base}sleep2".format(base
    base_warnings = self.BASE_UYARI(metod
    veriTuru = None
    url = self.driver.find_element_by_css_selector("video.tWeCl").get_attribute("src")
    veriTuru = 2
    url = self.driver.find_element_by_css_selector(
    veriTuru = 1
    base_warnings = self.BASE_UYARI(metod
    base_sleep = self.BASE_SLEEP(metod
    album = set()
    ul = self.driver.find_element_by_css_selector("article ul.vi798")
    liste = ul.find_elements_by_css_selector("li.Ckrof")
    btn_ileri = self.driver.find_element_by_css_selector(
    base_warnings = self.BASE_UYARI(metod
    url = str(self.driver.current_url), hata
    veriTuru = None
    url = element.find_element_by_css_selector("video.tWeCl").get_attribute("src")
    veriTuru = 2
    url = element.find_element_by_css_selector("img.FFVAD").get_attribute("src")
    veriTuru = 1
    base_warnings = self.BASE_UYARI(metod
    kullanici = self.driver.find_elements_by_css_selector("div._01UL2 >a.-qQT3")[
    base_warnings = self.BASE_UYARI(metod
    base_warnings = self.BASE_UYARI(metod
    base_warnings = self.BASE_UYARI(metod
    dil = self.dil, metod
    dil = self.dil, metod
    dil = self.dil, metod
    base_warnings = self.BASE_UYARI(metod
    t1 = threading.Thread(target
    base_sleep = self.BASE_SLEEP(metod
    btn = self.driver.find_element_by_xpath("//button[contains(text(), 'Not Now')]")
    secici = secici
    base_sleep = self.BASE_SLEEP(metod
    base_warnings = self.BASE_UYARI(metod
    sleep1 = self.configGetir("{base}sleep1".format(base
    base = self.BASE_SLEEP(metod
    base_warnings = self.BASE_UYARI(metod
    base_warnings = self.BASE_UYARI(metod
    response = requests.get(url, headers = DEFAULT_HEADERS)
    base = self.BASE_SLEEP(metod
    uyari = colored(mesaj, "green")
    uyari = colored(mesaj, "red")
    uyari = colored(mesaj, "blue")
    dt = str(datetime.now()).replace(":", "_").replace(" ", "")
    isim = "{index}_{tarih}.jpg".format(index
    isim = "{index}_{tarih}.mp4".format(index
    base_warnings = self.BASE_UYARI(metod
    dosyaAdi = self.dosyaAdiOlustur(veriTuru)
    base_warnings = self.BASE_UYARI(metod
    base_inputs = self.BASE_UYARI(metod
    dosyaAdi = input(self.configGetir(base_inputs + "input1")).strip()
    icerik = set()
    base_warnings = self.BASE_UYARI(metod
    base_warnings = self.BASE_UYARI(metod
    hedef = kaynak
    instagram = Instagram()
    self._lazy_loaded = {}
    init(convert = True)
    self.config = None
    self.dil = None
    self.girisYapildimi = False
    self.tarayiciAcildimi = False
    self.aktifKullanici = ""
    self.index = 1
    self.BASE_URL = "https://www.instagram.com/"
    self.kullaniciListesiTakipEt(secim = secim)
    "languages.{dil}.warnings.secilenIslemiGoster.secimler".format(dil = self.dil)
    logger.info(str(self.configGetir(base_warnings + "warning1")).format(kullanici = kullanici))
    str(self.configGetir(base_warnings + "warning2")).format(kullanici = kullanici), 
    logger.info(str(self.configGetir(base_warnings + "warning1")).format(kullanici = kullanici))
    sleep(self.configGetir("{base}sleep1".format(base = base_sleep)))
    self.index = tempIndex + 1
    [url, veriTuru] = self.gonderiUrlGetir()
    sleep(self.configGetir("{base}sleep2".format(base = base_sleep)))
    logger.info(str(self.configGetir(base_warnings + "warning2")).format(kullanici = kullanici))
    str(self.configGetir(base_warnings + "warning3")).format(kullanici = kullanici), 
    async def gonderileriBegen(self, kullanici, secim, durum = True):
    logger.info(str(self.configGetir(base_warnings + "warning1")).format(kullanici = kullanici))
    sleep(self.configGetir("{base}sleep1".format(base = base_sleep)))
    sleep(self.configGetir("{base}sleep2".format(base = base_sleep)))
    sleep(self.configGetir("{base}sleep3".format(base = base_sleep)))
    logger.info(str(self.configGetir(base_warnings + "warning6")).format(kullanici = kullanici))
    sleep(self.configGetir("{base}sleep1".format(base = base_sleep)))
    takipEdilenKullanıcıAdi = self.takipEdilenKullaniciAdiGetir(element
    sleep(self.configGetir("{base}sleep2".format(base = base_sleep)))
    self.popupAsagiKaydir(secici = 'div[role
    sleep(self.configGetir("{base}sleep4".format(base = base_sleep)))
    str(self.configGetir(base_warnings + "warning6")).format(hata = str(error)), 
    async def topluYorumYapma(self, url = None, yorumSayisi
    self.urlGirildiMi(url = url, metod
    self.urlGecerliMi(url = url, metod
    logger.info(str(self.configGetir(base_warnings + "warning1")).format(url = url))
    str(self.configGetir(base_warnings + "warning2")).format(url = url), 
    str(self.configGetir(base_warnings + "warning3")).format(url = url), 
    self.topluYorumYapma(url = url, yorumSayisi
    logger.info(str(self.configGetir(base_warnings + "warning8")).format(url = url))
    str(self.configGetir(base_warnings + "warning9")).format(index = i + 1), 
    logger.info(str(self.configGetir(base_warnings + "warning11")).format(url = url))
    self.topluYorumYapma(url = url, yorumSayisi
    logger.info(str(self.configGetir(base_warnings + "warning14")).format(url = url))
    str(self.configGetir(base_warnings + "warning15")).format(url = url, hata
    self.takipEdilenleriGetir(takipciler = takipciler)
    str(self.configGetir(base_warnings + "warning5")).format(hata = str(error)), 
    str(self.configGetir(base_warnings + "warning6")).format(hata = str(error)), 
    self.urlGirildiMi(url = url, metod
    self.urlGecerliMi(url = url, metod
    logger.info(str(self.configGetir(base_warnings + "warning1")).format(url = url))
    logger.info(str(self.configGetir(base_warnings + "warning3")).format(url = url))
    sleep(self.configGetir("{base}sleep1".format(base = base_sleep)))
    logger.info(str(self.configGetir(base_warnings + "warning4")).format(url = url))
    str(self.configGetir(base_warnings + "warning5")).format(hata = str(error)), 
    sleep(self.configGetir("{base}sleep1".format(base = base_sleep)))
    str(self.configGetir(base_warnings + "warning4")).format(kullanici = kullanici), 
    str(self.configGetir(base_warnings + "warning5")).format(hata = str(error)), 
    self.urlGirildiMi(url = url, metod
    self.urlGecerliMi(url = url, metod
    logger.info(str(self.configGetir(base_warnings + "warning1")).format(url = url))
    logger.info(str(self.configGetir(base_warnings + "warning2")).format(url = url))
    [url, veriTuru] = self.gonderiUrlGetir()
    logger.info(str(self.configGetir(base_warnings + "warning3")).format(url = url))
    str(self.configGetir(base_warnings + "warning4")).format(url = url), 2
    str(self.configGetir(base_warnings + "warning5")).format(hata = error), 
    async def kullaniciTakipcileriniTakipEt(self, kullanici, secim, secilenIslem = None):
    logger.info(str(self.configGetir(base_warnings + "warning6")).format(kullanici = kullanici))
    sleep(self.configGetir("{base}sleep1".format(base = base_sleep)))
    self.popupAsagiKaydir(secici = 'div[role
    sleep(self.configGetir("{base}sleep3".format(base = base_sleep)))
    logger.info(str(self.configGetir(base_warnings + "warning8")).format(kullanici = kullanici))
    str(self.configGetir(base_warnings + "warning9")).format(kullanici = kullanici), 
    async def gonderiBegenenleriTakipEt(self, url = None, secilenIslem
    self.urlGirildiMi(url = url, metod
    self.urlGecerliMi(url = url, metod
    logger.info(str(self.configGetir(base_warnings + "warning1")).format(url = url))
    self.gonderiBegenenleriTakipEt(url = url, secilenIslem
    self.gonderiBegenenleriTakipEt(url = url, secilenIslem
    logger.info(str(self.configGetir(base_warnings + "warning7")).format(url = url))
    sleep(self.configGetir("{base}sleep1".format(base = base_sleep)))
    sleep(self.configGetir("{base}sleep3".format(base = base_sleep)))
    logger.info(str(self.configGetir(base_warnings + "warning10")).format(url = url))
    str(self.configGetir(base_warnings + "warning11")).format(url = url), 
    str(self.configGetir(base_warnings + "warning12")).format(hata = str(error)), 
    sleep(self.configGetir("{base}sleep1".format(base = base_sleep)))
    logger.info(str(self.configGetir(base_warnings + "warning1")).format(etiket = etiket))
    sleep(self.configGetir("{base}sleep2".format(base = base_sleep)))
    sleep(self.configGetir("{base}sleep4".format(base = base_sleep)))
    logger.info(str(self.configGetir(base_warnings + "warning4")).format(etiket = etiket))
    str(self.configGetir(base_warnings + "warning5")).format(hata = str(error)), 
    sleep(self.configGetir("{base}sleep1".format(base = base_sleep)))
    logger.info(str(self.configGetir(base_warnings + "warning1")).format(etiket = etiket))
    sleep(self.configGetir("{base}sleep2".format(base = base_sleep)))
    sleep(self.configGetir("{base}sleep4".format(base = base_sleep)))
    logger.info(str(self.configGetir(base_warnings + "warning4")).format(etiket = etiket))
    str(self.configGetir(base_warnings + "warning5")).format(hata = str(error)), 
    async def gonderiBegen(self, durum = True):
    self.urlGirildiMi(url = url, metod
    self.urlGecerliMi(url = url, metod
    logger.info(str(self.configGetir(base_warnings + "warning1")).format(url = url))
    logger.info(str(self.configGetir(base_warnings + "warning2")).format(url = url))
    logger.info(str(self.configGetir(base_warnings + "warning3")).format(url = url))
    logger.info(str(self.configGetir(base_warnings + "warning8")).format(url = url))
    logger.info(str(self.configGetir(base_warnings + "warning9")).format(url = url))
    str(self.configGetir(base_warnings + "warning10")).format(url = url), 
    str(self.configGetir(base_warnings + "warning11")).format(url = url), 
    str(self.configGetir(base_warnings + "warning12")).format(hata = error), 
    str(self.configGetir(base_warnings + "warning13")).format(hata = error), 
    async def gonderiYorumYapma(self, url = None, yorum
    self.urlGirildiMi(url = url, metod
    self.urlGecerliMi(url = url, metod
    self.gonderiYorumYapma(url = url, yorum
    logger.info(str(self.configGetir(base_warnings + "warning2")).format(url = url))
    logger.info(str(self.configGetir(base_warnings + "warning4")).format(url = url))
    logger.info(str(self.configGetir(base_warnings + "warning5")).format(url = url))
    str(self.configGetir(base_warnings + "warning6")).format(url = url), 2
    str(self.configGetir(base_warnings + "warning7")).format(url = url, hata
    async def kullaniciTakipEt(self, kullanici, secim, durum = True):
    logger.info(str(self.configGetir(base_warnings + "warning1")).format(kullanici = kullanici))
    logger.info(str(self.configGetir(base_warnings + "warning2")).format(kullanici = kullanici))
    self.kullaniciTakipDurumDegistir(kullanici = kullanici, durum
    logger.info(str(self.configGetir(base_warnings + "warning3")).format(kullanici = kullanici))
    logger.info(str(self.configGetir(base_warnings + "warning4")).format(kullanici = kullanici))
    async def kullaniciEngelle(self, kullanici, secim, durum = True):
    logger.info(str(self.configGetir(base_warnings + "warning1")).format(kullanici = kullanici))
    logger.info(str(self.configGetir(base_warnings + "warning2")).format(kullanici = kullanici))
    logger.info(str(self.configGetir(base_warnings + "warning7")).format(kullanici = kullanici))
    logger.info(str(self.configGetir(base_warnings + "warning8")).format(kullanici = kullanici))
    async def ayarlar(self, durum = True):
    "{base}ana_ekran.secenekler".format(base = self.BASE_AYARLAR())
    self.ayarlar(durum = False)
    str(self.configGetir(base_warnings + "warning2")).format(hata = str(error)), 
    self.girisYapildimi = False
    str(self.configGetir(base_warnings + "warning3")).format(hata = str(error)), 
    str(self.configGetir(base_warnings + "warning3")).format(hata = str(error)), 
    self.config = json.load(dosya)
    self.dil = self.configGetir("language")
    async def dilAyarlari(self, durum = True):
    "{base}dil_ayarlari.secenekler".format(base = self.BASE_AYARLAR())
    self.uyariOlustur(str(secenek).format(dil = self.dilGetir()), MAX_RETRIES)
    self.dilAyarlari(durum = False)
    str(self.configGetir(base_warnings + "warning2")).format(hata = str(error)), 
    async def tarayiciAyarlari(self, durum = True):
    "{base}tarayici_ayarlari.secenekler".format(base = self.BASE_AYARLAR())
    self.uyariOlustur(str(secenek).format(path = self.tarayiciPathGetir()), MAX_RETRIES)
    str(secenek).format(durum = self.tarayiciHeadlessGetir()), MAX_RETRIES
    self.tarayiciAyarlari(durum = False)
    str(self.configGetir(base_warnings + "warning2")).format(hata = str(error)), 
    async def dilSec(self, durum = True):
    "{base}dil_ayarlari.dil_degistir.secenekler".format(base = self.BASE_AYARLAR())
    self.uygulamaDilDegistir(dilNo = secilenIslem)
    self.dilSec(durum = False)
    str(self.configGetir(base_warnings + "warning2")).format(hata = str(error)), 
    veri["language"] = dil
    json.dump(veri, dosya, indent = 4, ensure_ascii
    str(self.configGetir(base_warnings + "warning2")).format(hata = str(error)), 
    t1.daemon = True
    self.driver = webdriver.Firefox(
    str(self.configGetir(base_warnings + "warning2")).format(hata = str(error)), 
    async def tarayiciPathAyarlari(self, durum = True):
    self.tarayiciPathAyarlari(durum = False)
    str(self.configGetir(base_warnings + "warning2")).format(hata = str(error)), 
    veri["driver_path"] = path
    json.dump(veri, dosya, indent = 4, ensure_ascii
    str(self.configGetir(base_warnings + "warning3")).format(hata = str(error)), 
    async def tarayiciGorunmeDurumuAyarlari(self, durum = True):
    self.tarayiciGorunmeDurumDegistir(durum = secilenIslem)
    self.tarayiciGorunmeDurumuAyarlari(durum = False)
    str(self.configGetir(base_warnings + "warning2")).format(hata = str(error)), 
    veri["headless"] = headless
    json.dump(veri, dosya, indent = 4, ensure_ascii
    str(self.configGetir(base_warnings + "warning2")).format(hata = str(error)), 
    sleep(self.configGetir("{base}sleep1".format(base = base_sleep)))
    self.popupAsagiKaydir(secici = 'div[role
    sleep(self.configGetir("{base}sleep2".format(base = base_sleep)))
    str(self.configGetir(base_warnings + "warning4")).format(hata = str(error)), 
    sleep(self.configGetir("{base}sleep1".format(base = base_sleep)))
    takipEdilenKullanıcıAdi = self.takipEdilenKullaniciAdiGetir(element
    sleep(self.configGetir("{base}sleep2".format(base = base_sleep)))
    self.popupAsagiKaydir(secici = 'div[role
    sleep(self.configGetir("{base}sleep4".format(base = base_sleep)))
    str(self.configGetir(base_warnings + "warning4")).format(hata = str(error)), 
    takipEdilenKullanıcıAdi = element.find_element_by_css_selector("a.FPmhX").get_attribute(
    async def girisYap(self, username = False, password
    sleep(self.configGetir("{base}sleep1".format(base = base_sleep)))
    sleep(self.configGetir("{base}sleep2".format(base = base_sleep)))
    str(self.configGetir(base_warnings + "warning6")).format(hata = str(error)), 
    self.girisYapildimi = True
    async def girisDogrulama(self, durum = True):
    sleep(self.configGetir("{base}sleep1".format(base = base_sleep)))
    sleep(self.configGetir("{base}sleep2".format(base = base_sleep)))
    self.girisYapildimi = True
    logger.info(str(self.configGetir(base_warnings + "warning1")).format(url = url))
    str(self.configGetir(base_warnings + "warning2")).format(etiket = etiket), 
    str(self.configGetir(base_warnings + "warning4")).format(hata = str(error)), 
    return self.etiketeGoreIslemLimitiGetir(islemNo = islemNo)
    str(self.configGetir(base_warnings + "warning2")).format(hata = str(error)), 
    str(self.configGetir(base_warnings + "warning1")).format(hata = str(error)), 
    str(self.configGetir(base_warnings + "warning1")).format(hata = str(error)), 
    sleep(self.configGetir("{base}sleep1".format(base = base_sleep)))
    str(self.configGetir(base_warnings + "warning1")).format(hata = str(error)), 
    str(self.configGetir(base_warnings + "warning1")).format(hata = str(error)), 
    str(self.configGetir(base_warnings + "warning1")).format(hata = str(error)), 
    sleep(self.configGetir("{base}sleep1".format(base = base_sleep)))
    sleep(self.configGetir("{base}sleep2".format(base = base_sleep)))
    sleep(self.configGetir("{base}sleep1".format(base = base_sleep)))
    sleep(self.configGetir("{base}sleep1".format(base = base_sleep)))
    sleep(self.configGetir("{base}sleep1".format(base = base_sleep)))
    str(self.configGetir(base_warnings + "warning1")).format(kullanici = kullanici), 
    async def gonderiTipiVideoMu(self, element = None):
    str(self.configGetir(base_warnings + "warning1")).format(hata = str(error)), 
    [url, veriTuru] = self.albumIcerikUrlGetir(li)
    sleep(self.configGetir("{base}sleep1".format(base = base_sleep)))
    str(self.configGetir(base_warnings + "warning1")).format(hata = str(error)), 
    self.aktifKullanici = str(kullanici).replace(self.BASE_URL, "")
    str(self.configGetir(base_warnings + "warning1")).format(hata = str(error)), 
    return "languages.{dil}.ayarlar.".format(dil = self.dil)
    str(self.configGetir(base_warnings + "warning1")).format(hata = str(error)), 
    return "time.{metod}.".format(metod = metod.__name__)
    str(self.configGetir(base_warnings + "warning1")).format(hata = str(error)), 
    async def BASE_UYARI(self, metod, warnings = None, inputs
    str(self.configGetir(base_warnings + "warning1")).format(hata = str(error))
    t1.daemon = True
    sleep(self.configGetir("{base}sleep1".format(base = base_sleep)))
    var fDialog = document.querySelector('{secici}');
    fDialog.scrollTop = fDialog.scrollHeight
    self.kullaniciTakipEt(kullanici = kullanici.strip(), secim
    sleep(self.configGetir("{base}sleep1".format(base = base)))
    async def urlGirildiMi(self, url, metod, metodDeger = None):
    metod(yorum = metodDeger)
    async def urlGecerliMi(self, url, metod, metodDeger = None):
    metod(yorum = metodDeger)
    sleep(self.configGetir("{base}sleep1".format(base = base)))
    self.uyariOlustur(str(self.configGetir(base_warnings + "warning1")).format(url = url), 1)
    str(self.configGetir(base_warnings + "warning2")).format(hata = str(error)), 
    str(self.configGetir(base_warnings + "warning2")).format(hata = str(error)), 
    str(self.configGetir(base_warnings + "warning1")).format(hata = str(error)), 
    str(self.configGetir(base_warnings + "warning1")).format(klasor = klasor), 
    logger.info(str(self.configGetir(base_warnings + "warning2")).format(klasor = klasor))
    logger.info(str(self.configGetir(base_warnings + "warning3")).format(klasor = klasor))
    self.index = 1
    self.index = self.index + 1


# Constants



async def sanitize_html(html_content):
@lru_cache(maxsize = 128)
def sanitize_html(html_content): -> Any
    """Sanitize HTML content to prevent XSS."""
    return html.escape(html_content)


async def safe_sql_query(query, params):
@lru_cache(maxsize = 128)
def safe_sql_query(query, params): -> Any
    """Execute SQL query safely with parameterized queries."""
    # Use parameterized queries to prevent SQL injection
    return execute_query(query, params)


async def validate_input(data, validators):
@lru_cache(maxsize = 128)
def validate_input(data, validators): -> Any
    """Validate input data."""
    for field, validator in validators.items():
        if field in data:
            if not validator(data[field]):
                raise ValueError(f"Invalid {field}: {data[field]}")
    return True


async def memoize(func):
@lru_cache(maxsize = 128)
def memoize(func): -> Any
    """Memoization decorator."""

    async def wrapper(*args, **kwargs):
@lru_cache(maxsize = 128)
    def wrapper(*args, **kwargs): -> Any
        if key not in cache:
        return cache[key]

    return wrapper


# Constants



@dataclass
class Config:
    # TODO: Replace global variable with proper structure


# Constants


@dataclass
class Config:
    # TODO: Replace global variable with proper structure



@dataclass
class Instagram:
async def __init__(self):
def __init__(self): -> Any
self.ayarlarYukle()
self.dilYukle()
self.script()
self.tarayiciThreadOlustur()
self.girisYap()

async def script(self):
def script(self): -> Any
logger.info("")
self.uyariOlustur(
"  _____           _                                    ____        _   ", 1
)
self.uyariOlustur(
" |_   _|         | |                                  |  _ \\\\\\\\      | |  ", 1
)
self.uyariOlustur(
"   | |  _ __  ___| |_ __ _  __ _ _ __ __ _ _ __ ___   | |_) | ___ | |_ ", 1
)
self.uyariOlustur(
"   | | | '_ \\\\/ __| __/ _` |/ _` | '__/ _` | '_ ` _ \\\\\\\\  |  _ < / _ \\\\\\\\\| __|", 1
)
self.uyariOlustur(
"  _| |_| | | \\\\\\\\__ \\\\\\\\ || (_| | (_| | | | (_| c | | | | | | |_) | (_) | |_ ", 1
)
self.uyariOlustur(
" |_____|_| |_|___/\\\\\\\\__\\\\\\\\__, _|\\\\\\\\__, |_|  \\\\\\\\__, _|_| |_| |_| |____/ \\\\\\\\___/ \\\\\\\\__|", 1
)
self.uyariOlustur(
"                            __/ |                                      ", 1
)
self.uyariOlustur(
"                           |___/                                       ", 1
)
self.uyariOlustur(
1, 
)
self.uyariOlustur("# author       :Mustafa Dalga", 1)
self.uyariOlustur("# linkedin     :https://www.linkedin.com/in/mustafadalga", 1)
self.uyariOlustur("# github       :https://github.com/mustafadalga", 1)
self.uyariOlustur("# email        :mustafadalgaa < at > gmail[.]com", 1)
self.uyariOlustur("# date         :08.08.2020", 1)
self.uyariOlustur("# version      :2.0", 1)
self.uyariOlustur("# python_version:MAX_RETRIES.8.1", 1)
self.uyariOlustur(
1, 
)
logger.info("")

async def menu(self):
def menu(self): -> Any
for secenek in menu:
self.uyariOlustur(secenek, MAX_RETRIES)
self.islemSec()

async def islemSec(self):
def islemSec(self): -> Any
if secim:
try:
if 0 < secim < 27:
self.secilenIslemiGoster(secim)
if secim in [1, 2, MAX_RETRIES, 9, 12, 20, 21, 22, 23]:
self.profilSec(secim)
elif secim == 4:
self.topluTakiptenCik()
elif secim == 5:
self.topluYorumYapma()
elif secim == 6:
self.takipEtmeyenleriTakiptenCik()
elif secim == 7:
self.topluMesajSilme()
elif secim == 8:
self.oneCikanHikayeIndir()
elif secim in [10, 11]:
self.gonderiIndir()
elif secim == 13:
elif secim == 14:
self.gonderiBegenenleriTakipEt()
elif secim == 15:
self.etiketeGoreTakipEtme()
elif secim == 16:
self.etiketeGoreBegenme()
elif secim == 17:
self.gonderiBegen()
elif secim == 18:
self.gonderiBegen(False)
elif secim == 19:
self.gonderiYorumYapma()
elif secim == 24:
self.ayarlar()
elif secim == 25:
self.oturumKapat()
elif secim == 26:
self.quit()
else:
self.uyariOlustur(self.configGetir(base_warnings + "warning1"), 2)
self.islemSec()
    except (ValueError, TypeError, RuntimeError) as e:
        logger.error(f"Specific error occurred: {e}")
        raise
self.uyariOlustur(self.configGetir(base_warnings + "warning2"), 2)
self.islemSec()
else:
self.islemSec()

async def secilenIslemiGoster(self, secim):
def secilenIslemiGoster(self, secim): -> Any
)
logger.info("")
self.uyariOlustur(secimler.get(str(secim), self.configGetir(base_warnings + "warning1")), 1)
if secim < 24:
self.uyariOlustur(self.configGetir(base_warnings + "warning2"), MAX_RETRIES)
logger.info("")

async def profilSec(self, secim):
def profilSec(self, secim): -> Any


if not kullanici:
self.profilSec(secim)

self.anaMenuyeDonsunMu(kullanici)

if self.kullaniciKontrol(kullanici):
if secim == 1:
self.gonderileriIndir(kullanici, secim)
elif secim == 2:
self.gonderileriBegen(kullanici, secim)
elif secim == MAX_RETRIES:
self.gonderileriBegen(kullanici, secim, False)
elif secim == 9:
self.hikayeIndir(kullanici, secim)
elif secim == 12:
self.kullaniciTakipcileriniTakipEt(kullanici, secim)
elif secim == 20:
self.kullaniciTakipEt(kullanici, secim)
elif secim == 21:
self.kullaniciTakipEt(kullanici, secim, False)
elif secim == 22:
self.kullaniciEngelle(kullanici, secim)
elif secim == 23:
self.kullaniciEngelle(kullanici, secim, False)
else:
self.uyariOlustur(
2, 
)
self.profilSec(secim)

async def ilkGonderiTikla(self):
def ilkGonderiTikla(self): -> Any
ilkGonderi.click()

async def gonderileriIndir(self, kullanici, secim):
def gonderileriIndir(self, kullanici, secim): -> Any

try:
self.kullaniciProfilineYonlendir(kullanici)
if not self.hesapGizliMi():
self.gonderiVarMi(kullanici, gonderiSayisi, secim)
self.ilkGonderiTikla()
self.klasorOlustur(kullanici)
self.indexSifirla()
for index in range(gonderiSayisi):
if self.gonderiAlbumMu():
self.klasorOlustur(str(self.index) + "_album")
self.indexSifirla()
self.albumUrlGetir()
self.klasorDegistir("../")
else:
if url is not None:
self.dosyaIndir(url, veriTuru)
else:
    continue
self.gonderiIlerlet()
self.klasorDegistir("../")
else:
self.uyariOlustur(
2, 
)

self.profilSec(secim)
    except (ValueError, TypeError, RuntimeError) as e:
        logger.error(f"Specific error occurred: {e}")
        raise
self.uyariOlustur(
str(self.configGetir(base_warnings + "warning4")).format(
), 
2, 
)
self.profilSec(secim)

def gonderileriBegen(self, kullanici, secim, durum = True): -> Any
try:
self.kullaniciProfilineYonlendir(kullanici)
if not self.hesapGizliMi():
self.gonderiVarMi(kullanici, gonderiSayisi, secim)
self.ilkGonderiTikla()
self.indexSifirla()
for index in range(gonderiSayisi):
if durum:
if begeniDurum == "like":
self.uyariOlustur(
str(self.configGetir(base_warnings + "warning2")).format(
), 
1, 
)
self.gonderiBegenDurumDegistir(btn_begen)
else:
logger.info(
str(self.configGetir(base_warnings + "warning3")).format(
)
)
self.gonderiIlerlet()
else:
if begeniDurum == "unlike":
self.uyariOlustur(
str(self.configGetir(base_warnings + "warning4")).format(
), 
1, 
)
self.gonderiBegenDurumDegistir(btn_begen)
else:
logger.info(
str(self.configGetir(base_warnings + "warning5")).format(
)
)
self.gonderiIlerlet()
self.profilSec(secim)
else:
if durum:
self.uyariOlustur(
str(self.configGetir(base_warnings + "warning7")).format(
), 
2, 
)
else:
self.uyariOlustur(
str(self.configGetir(base_warnings + "warning8")).format(
), 
2, 
)
self.profilSec(secim)
    except (ValueError, TypeError, RuntimeError) as e:
        logger.error(f"Specific error occurred: {e}")
        raise
if durum:
self.uyariOlustur(
str(self.configGetir(base_warnings + "warning9")).format(
), 
2, 
)
else:
self.uyariOlustur(
str(self.configGetir(base_warnings + "warning10")).format(
), 
2, 
)
self.profilSec(secim)

async def topluTakiptenCik(self):
def topluTakiptenCik(self): -> Any
try:
logger.info(self.configGetir(base_warnings + "warning1"))
self.kullaniciProfilineYonlendir(self.aktifKullanici)
btn_takipEdilenler.click()
self.indexSifirla()
while devamEtsinMi:
for takip in takipListe:
if btn_takip.text == "Following":
btn_takip.click()
try:
"div.mt3GC > button.aOOlW"
)
btn_onay.click()
    except (ValueError, TypeError, RuntimeError) as e:
        logger.error(f"Specific error occurred: {e}")
        raise
self.uyariOlustur(
str(self.configGetir(base_warnings + "warning2")).format(
), 
2, 
)
    continue
self.uyariOlustur(
str(self.configGetir(base_warnings + "warning3")).format(
), 
1, 
)
self.indexArtir()
if (self.index - 1) >= takipEdilenSayisi:
    break
sleep(self.beklemeSuresiGetir(sleep3[0], sleep3[1]))
if devamEtsinMi:
try:
    except (ValueError, TypeError, RuntimeError) as e:
        logger.error(f"Specific error occurred: {e}")
        raise
self.uyariOlustur(
str(self.configGetir(base_warnings + "warning4")).format(
), 
2, 
)
    pass
logger.info(self.configGetir(base_warnings + "warning5"))
self.menu()
    except (ValueError, TypeError, RuntimeError) as e:
        logger.error(f"Specific error occurred: {e}")
        raise
self.uyariOlustur(
2, 
)
self.menu()

def topluYorumYapma(self, url = None, yorumSayisi = None, secilenIslem = None): -> Any
try:
if url is None:
self.anaMenuyeDonsunMu(url)


self.urlYonlendir(url)

if not self.sayfaMevcutMu():
self.uyariOlustur(
2, 
)
self.topluYorumYapma()

if self.hesapGizliMi():
self.uyariOlustur(
2, 
)
self.topluYorumYapma()

if not yorumSayisi:
self.anaMenuyeDonsunMu(yorumSayisi)
if yorumSayisi.isnumeric() and int(yorumSayisi) > 0:
if self.yorumLimitiAsildiMi(yorumSayisi):
logger.info(self.configGetir(base_warnings + "warning4"))
else:
self.uyariOlustur(self.configGetir(base_warnings + "warning5"), 2)

if not secilenIslem:
for secenek in self.configGetir(base_warnings + "warning6"):
self.uyariOlustur(secenek, MAX_RETRIES)
self.anaMenuyeDonsunMu(secilenIslem)

if secilenIslem == "1":
self.uyariOlustur(self.configGetir(base_warnings + "warning7"), 1)
for i in range(yorumSayisi):
self.yorumYap(yorum)
self.uyariOlustur(
1, 
)

sleep(self.beklemeSuresiGetir(sleep1[0], sleep1[1]))
elif secilenIslem == "2":
self.uyariOlustur(self.configGetir(base_warnings + "warning10"), 1)
if self.dosyaIcerigiAlindiMi(yorumlar):
for index, yorum in enumerate(yorumlar):
self.yorumYap(yorum)
self.uyariOlustur(
str(self.configGetir(base_warnings + "warning12")).format(
), 
1, 
)
if (index + 1) == yorumSayisi:
    break
sleep(self.beklemeSuresiGetir(sleep1[0], sleep1[1]))
else:
self.topluYorumYapma(
)
else:
self.uyariOlustur(self.configGetir(base_warnings + "warning13"), 2)
logger.info("")

self.topluYorumYapma()
    except (ValueError, TypeError, RuntimeError) as e:
        logger.error(f"Specific error occurred: {e}")
        raise
self.uyariOlustur(
2, 
)
self.topluYorumYapma()

async def takipEtmeyenleriTakiptenCik(self):
def takipEtmeyenleriTakiptenCik(self): -> Any
try:
logger.info(self.configGetir(base_warnings + "warning1"))
logger.info(self.configGetir(base_warnings + "warning2"))
logger.info(self.configGetir(base_warnings + "warning3"))
logger.info(self.configGetir(base_warnings + "warning4"))
self.menu()
    except (ValueError, TypeError, RuntimeError) as e:
        logger.error(f"Specific error occurred: {e}")
        raise
self.uyariOlustur(
2, 
)
self.menu()

async def topluMesajSilme(self):
def topluMesajSilme(self): -> Any
try:

logger.info(self.configGetir(base_warnings + "warning1"))
self.kullaniciProfilineYonlendir("direct/inbox/")
self.indexSifirla()
while devamEtsinMi:
if len(mesajListesi) == 0:
logger.info(self.configGetir(base_warnings + "warning2"))
    break
for mesaj in mesajListesi:
if mesaj not in silinenMesajlar:
silinenMesajlar.add(mesaj)
"._7UhW9.xLCgt.MMzan.KV-D4.fDxYl"
).text
logger.info(
str(self.configGetir(base_warnings + "warning3")).format(
)
)
self.mesajSil(mesaj)
self.uyariOlustur(
str(self.configGetir(base_warnings + "warning4")).format(
), 
1, 
)
self.indexArtir()
sleep(self.beklemeSuresiGetir(sleep1[0], sleep1[1]))
    break

logger.info(self.configGetir(base_warnings + "warning5"))
self.menu()
    except (ValueError, TypeError, RuntimeError) as e:
        logger.error(f"Specific error occurred: {e}")
        raise
self.uyariOlustur(
2, 
)
self.menu()

async def oneCikanHikayeIndir(self):
def oneCikanHikayeIndir(self): -> Any

try:
self.anaMenuyeDonsunMu(url)

self.urlYonlendir(url)

if not self.sayfaMevcutMu():
self.uyariOlustur(self.configGetir(base_warnings + "warning2"), 2)
self.oneCikanHikayeIndir()

btn_oynat.click()
self.klasorOlustur(kullanici)
self.indexSifirla()
self.hikayeleriGetir()
self.klasorDegistir("../")
self.oneCikanHikayeIndir()
    except (ValueError, TypeError, RuntimeError) as e:
        logger.error(f"Specific error occurred: {e}")
        raise
self.uyariOlustur(
2, 
)
self.oneCikanHikayeIndir()

async def hikayeIndir(self, kullanici, secim):
def hikayeIndir(self, kullanici, secim): -> Any

try:
self.kullaniciProfilineYonlendir(kullanici)
if not self.hesapGizliMi():
if self.hikayeVarMi():
self.driver.find_element_by_css_selector("div.RR-M-").click()
logger.info(
str(self.configGetir(base_warnings + "warning1")).format(
)
)
self.klasorOlustur(kullanici)
self.indexSifirla()
self.hikayeleriGetir()
self.klasorDegistir("../")
logger.info(
str(self.configGetir(base_warnings + "warning2")).format(
)
)
else:
self.uyariOlustur(self.configGetir(base_warnings + "warning3"), 2)
else:
self.uyariOlustur(
2, 
)
self.profilSec(secim)
    except (ValueError, TypeError, RuntimeError) as e:
        logger.error(f"Specific error occurred: {e}")
        raise
self.uyariOlustur(
2, 
)
self.profilSec(secim)

async def gonderiKullaniciAdi(self):
def gonderiKullaniciAdi(self): -> Any
    return self.driver.find_element_by_css_selector("a.sqdOP").text

async def gonderiIndir(self):
def gonderiIndir(self): -> Any
try:
self.anaMenuyeDonsunMu(url)

self.urlYonlendir(url)
if not self.hesapGizliMi():
self.klasorOlustur(kullanici)
if self.gonderiAlbumMu():
self.indexSifirla()
self.klasorOlustur(str(self.index) + "_album")
self.albumUrlGetir()
self.klasorDegistir("../")
else:
if url is not None:
self.dosyaIndir(url, veriTuru)
self.klasorDegistir("../")
else:
self.uyariOlustur(
)
self.gonderiIndir()
    except (ValueError, TypeError, RuntimeError) as e:
        logger.error(f"Specific error occurred: {e}")
        raise
logger.info(
self.uyariOlustur(
2, 
)
)
self.gonderiIndir()

def kullaniciTakipcileriniTakipEt(self, kullanici, secim, secilenIslem = None): -> Any

try:
self.kullaniciProfilineYonlendir(kullanici)

if secilenIslem is None:
for secenek in self.configGetir(base_warnings + "warning1"):
self.uyariOlustur(secenek, MAX_RETRIES)
self.anaMenuyeDonsunMu(secilenIslem)

if secilenIslem == "1":
self.uyariOlustur(self.configGetir(base_warnings + "warning2"), 1)
elif secilenIslem == "2":
self.uyariOlustur(self.configGetir(base_warnings + "warning3"), 1)
self.anaMenuyeDonsunMu(hedefTakipciSayisi)
if hedefTakipciSayisi.isnumeric():
else:
self.uyariOlustur(self.configGetir(base_warnings + "warning4"), 2)
logger.info("")
self.kullaniciTakipcileriniTakipEt(
)
else:
self.uyariOlustur(self.configGetir(base_warnings + "warning5"), 2)
logger.info("")
self.kullaniciTakipcileriniTakipEt(
)

if not self.hesapGizliMi():
self.indexSifirla()

if hedefTakipciSayisi is None:
"a.-nal3 > span.g47SY"
)[0].get_attribute("title")
else:
"a.-nal3 > span.g47SY"
).get_attribute("title")
hedefTakipciSayisi, kaynakTakipciSayisi
)

btn_takipciler.click()
while devamEtsinMi:
for takipci in takipciListe:
"a.FPmhX"
).get_attribute("href")
self.BASE_URL, ""
).replace("/", "")
try:
if btn_takip.text == "Follow":
logger.info(
str(self.configGetir(base_warnings + "warning7")).format(
)
)
btn_takip.click()
self.indexArtir()
if self.index - 1 >= takipciSayisi:
    break
sleep(self.beklemeSuresiGetir(sleep2[0], sleep2[1]))
    except (ValueError, TypeError, RuntimeError) as e:
        logger.error(f"Specific error occurred: {e}")
        raise
    pass
kontrolEdilenKullanicilar.add(takipciKullaniciAdi)
if hedefTakipciSayisi:
if len(kontrolEdilenKullanicilar) >= kaynakTakipciSayisi:
else:
if len(kontrolEdilenKullanicilar) >= takipciSayisi:

if devamEtsinMi:
else:
self.uyariOlustur(
2, 
)
self.profilSec(secim)
    except (ValueError, TypeError, RuntimeError) as e:
        logger.error(f"Specific error occurred: {e}")
        raise
self.uyariOlustur(
str(self.configGetir(base_warnings + "warning10")).format(
), 
2, 
)
self.profilSec(secim)

async def kullaniciListesiTakipEt(self, secim):
def kullaniciListesiTakipEt(self, secim): -> Any
if self.dosyaIcerigiAlindiMi(kullanicilar):
self.kullanicilariTakipEt(kullanicilar, secim)
else:
self.kullaniciListesiTakipEt(secim)
self.kullaniciListesiTakipEt(secim)

def gonderiBegenenleriTakipEt(self, url = None, secilenIslem = None): -> Any
try:
if url is None:
self.anaMenuyeDonsunMu(url)
self.urlYonlendir(url)


if secilenIslem is None:
for secenek in self.configGetir(base_warnings + "warning2"):
self.uyariOlustur(secenek, MAX_RETRIES)
self.anaMenuyeDonsunMu(secilenIslem)

if secilenIslem == "1":
self.uyariOlustur(self.configGetir(base_warnings + "warning3"), 1)
elif secilenIslem == "2":
self.uyariOlustur(self.configGetir(base_warnings + "warning4"), 1)
self.anaMenuyeDonsunMu(hedefBegenenSayisi)
if hedefBegenenSayisi.isnumeric():
else:
self.uyariOlustur(self.configGetir(base_warnings + "warning5"), 2)
logger.info("")
else:
self.uyariOlustur(self.configGetir(base_warnings + "warning6"), 2)
logger.info("")

if not self.hesapGizliMi():
if not self.gonderiTipiVideoMu():
self.indexSifirla()

if hedefBegenenSayisi is None:
"div.Nm9Fw > button.sqdOP > span"
).text
else:
"div.Nm9Fw > button.sqdOP > span"
).text
self.metindenKarakterSil(kaynakBegenenSayisi, ", ")
)
self.hedefKaynaktanBuyukMu(hedefBegenenSayisi, kaynakBegenenSayisi)
)

"div.Nm9Fw > button.sqdOP"
)
btn_begenenler.click()
while devamEtsinMi:
"div.HVWg4"
)
for begenenKullanici in begenenlerKullanicilar:
"div.Igw0E > div.Igw0E > div._7UhW9  a"
).get_attribute("href")
self.BASE_URL, ""
).replace("/", "")
"div.Igw0E > button.sqdOP"
)
if btn_takip.text == "Follow":
logger.info(
str(self.configGetir(base_warnings + "warning8")).format(
)
)
btn_takip.click()
self.indexArtir()
if self.index - 1 >= begenenSayisi:
    break
sleep(self.beklemeSuresiGetir(sleep2[0], sleep2[1]))

kontrolEdilenKullanicilar.add(begenenKullaniciAdi)

if hedefBegenenSayisi:
if len(kontrolEdilenKullanicilar) >= kaynakBegenenSayisi:
    break
else:
if len(kontrolEdilenKullanicilar) >= begenenSayisi:
    break
if devamEtsinMi:
self.popupAsagiKaydir(
)
else:
logger.info(self.configGetir(base_warnings + "warning9"))
else:
else:
self.uyariOlustur(
2, 
)
self.gonderiBegenenleriTakipEt()
    except (ValueError, TypeError, RuntimeError) as e:
        logger.error(f"Specific error occurred: {e}")
        raise
self.uyariOlustur(
2, 
)
self.gonderiBegenenleriTakipEt()

async def etiketeGoreTakipEtme(self):
def etiketeGoreTakipEtme(self): -> Any
try:


self.metindenKarakterSil(
self.driver.find_element_by_css_selector("span.g47SY").text, ", "
)
)
self.ilkGonderiTikla()
self.indexSifirla()

while True:
if btn_takip.text != "Following":
btn_takip.click()
self.uyariOlustur(
str(self.configGetir(base_warnings + "warning2")).format(
), 
1, 
)
self.indexArtir()
if self.index - 1 >= limit:
    break
self.gonderiIlerlet()
sleep(self.beklemeSuresiGetir(sleep3[0], sleep3[1]))
else:
logger.info(
str(self.configGetir(base_warnings + "warning3")).format(
)
)
self.gonderiIlerlet()
self.etiketeGoreTakipEtme()
    except (ValueError, TypeError, RuntimeError) as e:
        logger.error(f"Specific error occurred: {e}")
        raise
self.uyariOlustur(
2, 
)
self.etiketeGoreTakipEtme()

async def etiketeGoreBegenme(self):
def etiketeGoreBegenme(self): -> Any
try:
self.metindenKarakterSil(
self.driver.find_element_by_css_selector("span.g47SY").text, ", "
)
)
self.ilkGonderiTikla()
self.indexSifirla()

while True:
if begeniDurum != "unlike":
btn_begen.click()
self.uyariOlustur(
str(self.configGetir(base_warnings + "warning2")).format(
), 
1, 
)
self.indexArtir()
if self.index - 1 >= limit:
    break
self.gonderiIlerlet()
sleep(self.beklemeSuresiGetir(sleep3[0], sleep3[1]))
else:
logger.info(
str(self.configGetir(base_warnings + "warning3")).format(
)
)
self.gonderiIlerlet()
self.etiketeGoreBegenme()
    except (ValueError, TypeError, RuntimeError) as e:
        logger.error(f"Specific error occurred: {e}")
        raise
self.uyariOlustur(
2, 
)
self.etiketeGoreBegenme()

def gonderiBegen(self, durum = True): -> Any

try:
if durum:
else:

self.anaMenuyeDonsunMu(url)
self.urlYonlendir(url)
if not self.hesapGizliMi():
if durum:
else:
if durum:
if begeniDurum == "like":
btn_begen.click()
logger.info(
self.uyariOlustur(
str(self.configGetir(base_warnings + "warning4")).format(
), 
1, 
)
)
else:
logger.info(
str(self.configGetir(base_warnings + "warning5")).format(
)
)
else:
if begeniDurum == "unlike":
btn_begen.click()
self.uyariOlustur(
str(self.configGetir(base_warnings + "warning6")).format(
), 
1, 
)
else:
logger.info(
str(self.configGetir(base_warnings + "warning7")).format(
)
)
if durum:
else:
else:
if durum:
self.uyariOlustur(
2, 
)
else:
self.uyariOlustur(
2, 
)
self.gonderiBegen(durum)
    except (ValueError, TypeError, RuntimeError) as e:
        logger.error(f"Specific error occurred: {e}")
        raise
if durum:
self.uyariOlustur(
2, 
)
else:
self.uyariOlustur(
2, 
)
self.gonderiBegen(durum)

def gonderiYorumYapma(self, url = None, yorum = None): -> Any
try:

if url is None:
self.anaMenuyeDonsunMu(url)
if not yorum:
self.anaMenuyeDonsunMu(yorum)


if not self.degerVarMi(yorum):
self.uyariOlustur(self.configGetir(base_warnings + "warning1"), 2)

self.urlYonlendir(url)

if not self.sayfaMevcutMu():
self.uyariOlustur(self.configGetir(base_warnings + "warning3"), 2)
self.gonderiYorumYapma()

if not self.hesapGizliMi():
self.yorumYap(yorum)
else:
self.uyariOlustur(
)
self.gonderiYorumYapma()
    except (ValueError, TypeError, RuntimeError) as e:
        logger.error(f"Specific error occurred: {e}")
        raise
self.uyariOlustur(
2, 
)
self.gonderiYorumYapma()

def kullaniciTakipEt(self, kullanici, secim, durum = True): -> Any
try:
self.kullaniciProfilineYonlendir(kullanici)
if durum:
else:

if durum:
else:
if secim != 13:
self.profilSec(secim)
    except (ValueError, TypeError, RuntimeError) as e:
        logger.error(f"Specific error occurred: {e}")
        raise
if durum:
self.uyariOlustur(
str(self.configGetir(base_warnings + "warning5")).format(
), 
2, 
)
else:
self.uyariOlustur(
str(self.configGetir(base_warnings + "warning6")).format(
), 
2, 
)
if secim != 13:
self.profilSec(secim)

def kullaniciEngelle(self, kullanici, secim, durum = True): -> Any
try:
self.kullaniciProfilineYonlendir(kullanici)
if durum:
else:

if self.hesapGizliMi():
self.driver.find_element_by_css_selector("div.BY3EC >button").text
).lower()
if durum:
if btnText != "unblock":
self.kullaniciEngelDurumDegistir()
else:
self.uyariOlustur(
str(self.configGetir(base_warnings + "warning3")).format(
), 
2, 
)
else:
if btnText == "unblock":
self.kullaniciEngelDurumDegistir()
else:
self.uyariOlustur(
str(self.configGetir(base_warnings + "warning4")).format(
), 
2, 
)
else:
self.driver.find_element_by_css_selector("span.vBF20 > button._5f5mN").text
).lower()
if durum:
if btnText != "unblock":
self.kullaniciEngelDurumDegistir()
else:
self.uyariOlustur(
str(self.configGetir(base_warnings + "warning5")).format(
), 
2, 
)
else:
if btnText == "unblock":
self.kullaniciEngelDurumDegistir()
else:
self.uyariOlustur(
str(self.configGetir(base_warnings + "warning6")).format(
), 
2, 
)

if durum:
else:
self.profilSec(secim)
    except (ValueError, TypeError, RuntimeError) as e:
        logger.error(f"Specific error occurred: {e}")
        raise
if durum:
self.uyariOlustur(
str(self.configGetir(base_warnings + "warning9")).format(
), 
2, 
)
else:
self.uyariOlustur(
str(self.configGetir(base_warnings + "warning10")).format(
), 
2, 
)
self.profilSec(secim)

def ayarlar(self, durum = True): -> Any
try:
if durum:
)
for secenek in ayarlar:
self.uyariOlustur(secenek, MAX_RETRIES)

if secilenIslem == "1":
self.dilAyarlari()
elif secilenIslem == "2":
self.tarayiciAyarlari()
elif secilenIslem == "MAX_RETRIES":
self.menu()
else:
self.uyariOlustur(self.configGetir(base_warnings + "warning1"), 2)
    except (ValueError, TypeError, RuntimeError) as e:
        logger.error(f"Specific error occurred: {e}")
        raise
self.uyariOlustur(
2, 
)

async def oturumKapat(self):
def oturumKapat(self): -> Any
logger.info(self.configGetir(base_warnings + "warning1"))
try:
self.driver.find_elements_by_css_selector("div._47KiJ > div.Fifk5")[-1].click()
sleep(0.10)
self.driver.find_elements_by_css_selector("div.-qQT3")[-1].click()
self.uyariOlustur(self.configGetir(base_warnings + "warning2"), 1)
self.driver.get(self.BASE_URL + "accounts/login/")
self.girisYap()
    except (ValueError, TypeError, RuntimeError) as e:
        logger.error(f"Specific error occurred: {e}")
        raise
self.uyariOlustur(
2, 
)
self.menu()

async def quit(self):
def quit(self): -> Any
try:
logger.info(self.configGetir(base_warnings + "warning1"))
self.driver.quit()
self.uyariOlustur(self.configGetir(base_warnings + "warning2"), 1)
exit()
    except (ValueError, TypeError, RuntimeError) as e:
        logger.error(f"Specific error occurred: {e}")
        raise
self.uyariOlustur(
2, 
)
self.driver.quit()
exit()

async def ayarlarYukle(self):
def ayarlarYukle(self): -> Any
if self.dosyaMevcutMu("config.json"):
with open("config.json", "r+", encoding="utf-8") as dosya:
else:
self.uyariOlustur("Config file is missing - Config dosyası eksik !", 2)
exit()

async def configGetir(self, anahtar):
def configGetir(self, anahtar): -> Any
for key in anahtar.split("."):
    return deger

async def dilYukle(self):
def dilYukle(self): -> Any

async def dilGetir(self):
def dilGetir(self): -> Any
if self.dil == "tr":
    return "Türkçe"
else:
    return "English"

def dilAyarlari(self, durum = True): -> Any
try:
if durum:
)
for secenek in ayarlar:
if "{dil}" in secenek:
else:
self.uyariOlustur(secenek, MAX_RETRIES)

if secilenIslem == "1":
self.dilSec()
elif secilenIslem == "2":
self.ayarlar()
elif secilenIslem == "MAX_RETRIES":
self.menu()
else:
self.uyariOlustur(self.configGetir(base_warnings + "warning1"), 2)
    except (ValueError, TypeError, RuntimeError) as e:
        logger.error(f"Specific error occurred: {e}")
        raise
self.uyariOlustur(
2, 
)

def tarayiciAyarlari(self, durum = True): -> Any
try:
if durum:
)
for secenek in ayarlar:
if "{path}" in secenek:
elif "{durum}" in secenek:
self.uyariOlustur(
)
else:
self.uyariOlustur(secenek, MAX_RETRIES)

if secilenIslem == "1":
self.tarayiciGorunmeDurumuAyarlari()
elif secilenIslem == "2":
self.tarayiciPathAyarlari()
elif secilenIslem == "MAX_RETRIES":
self.ayarlar()
elif secilenIslem == "4":
self.menu()
else:
self.uyariOlustur(self.configGetir(base_warnings + "warning1"), 2)
    except (ValueError, TypeError, RuntimeError) as e:
        logger.error(f"Specific error occurred: {e}")
        raise
self.uyariOlustur(
2, 
)

async def tarayiciHeadlessGetir(self):
def tarayiciHeadlessGetir(self): -> Any
if headless == "true":
if self.dil == "tr":
elif self.dil == "en":
else:
if self.dil == "tr":
elif self.dil == "en":
    return durum

def dilSec(self, durum = True): -> Any
try:
if durum:
)
for secenek in ayarlar:
self.uyariOlustur(secenek, MAX_RETRIES)

if secilenIslem in ["1", "2"]:
self.ayarlar()
elif secilenIslem == "MAX_RETRIES":
self.dilAyarlari()
elif secilenIslem == "4":
self.ayarlar()
elif secilenIslem == "5":
self.menu()
else:
self.uyariOlustur(self.configGetir(base_warnings + "warning1"), 2)
    except (ValueError, TypeError, RuntimeError) as e:
        logger.error(f"Specific error occurred: {e}")
        raise
self.uyariOlustur(
2, 
)

async def uygulamaDilDegistir(self, dilNo):
def uygulamaDilDegistir(self, dilNo): -> Any
try:
if dilNo == "1":
elif dilNo == "2":
with open("config.json", "r+", encoding="utf-8") as dosya:
dosya.seek(0)
dosya.truncate()
self.uyariOlustur(self.configGetir(base_warnings + "warning1"), 1)
    except (ValueError, TypeError, RuntimeError) as e:
        logger.error(f"Specific error occurred: {e}")
        raise
self.uyariOlustur(
2, 
)

async def tarayiciThreadOlustur(self):
def tarayiciThreadOlustur(self): -> Any
t1.start()

async def tarayiciBaslat(self):
def tarayiciBaslat(self): -> Any
try:
logger.info(self.configGetir(base_warnings + "warning1"))
if headless == "false":
firefox_options.add_argument("--headless")
)
self.driver.get(self.BASE_URL + "accounts/login/")
    except (ValueError, TypeError, RuntimeError) as e:
        logger.error(f"Specific error occurred: {e}")
        raise
self.uyariOlustur(
2, 
)
exit()

async def tarayiciPathGetir(self):
def tarayiciPathGetir(self): -> Any
    return self.configGetir("driver_path")

async def tarayiciDilDegistir(self):
def tarayiciDilDegistir(self): -> Any
profile.set_preference("intl.accept_languages", "en-US, en")
    return profile

def tarayiciPathAyarlari(self, durum = True): -> Any
try:
if durum:
self.BASE_AYARLAR() + "tarayici_ayarlari.path_degistir.secenekler"
)
for secenek in ayarlar:
self.uyariOlustur(secenek, MAX_RETRIES)
if secilenIslem == "1":
self.tarayiciPathDegistir()
self.ayarlar()
elif secilenIslem == "2":
self.tarayiciAyarlari()
elif secilenIslem == "MAX_RETRIES":
self.ayarlar()
elif secilenIslem == "4":
self.menu()
else:
self.uyariOlustur(self.configGetir(base_warnings + "warning1"), 2)
    except (ValueError, TypeError, RuntimeError) as e:
        logger.error(f"Specific error occurred: {e}")
        raise
self.uyariOlustur(
2, 
)

async def tarayiciPathDegistir(self):
def tarayiciPathDegistir(self): -> Any
try:
if self.dosyaMevcutMu(path):
with open("config.json", "r+", encoding="utf-8") as dosya:
dosya.seek(0)
dosya.truncate()
self.uyariOlustur(self.configGetir(base_warnings + "warning1"), 1)
else:
self.uyariOlustur(self.configGetir(base_warnings + "warning2"), 2)
self.tarayiciPathAyarlari()
    except (ValueError, TypeError, RuntimeError) as e:
        logger.error(f"Specific error occurred: {e}")
        raise
self.uyariOlustur(
2, 
)

def tarayiciGorunmeDurumuAyarlari(self, durum = True): -> Any
try:
if durum:
"{base}tarayici_ayarlari.gorunme_durumu_degistir.secenekler".format(
)
)
for secenek in ayarlar:
self.uyariOlustur(secenek, MAX_RETRIES)
if secilenIslem in ["1", "2"]:
self.ayarlar()
elif secilenIslem == "MAX_RETRIES":
self.tarayiciAyarlari()
elif secilenIslem == "4":
self.ayarlar()
elif secilenIslem == "5":
self.menu()
else:
self.uyariOlustur(self.configGetir(base_warnings + "warning1"), 2)
    except (ValueError, TypeError, RuntimeError) as e:
        logger.error(f"Specific error occurred: {e}")
        raise
self.uyariOlustur(
2, 
)

async def tarayiciGorunmeDurumDegistir(self, durum):
def tarayiciGorunmeDurumDegistir(self, durum): -> Any
try:
if durum == "1":
elif durum == "2":
with open("config.json", "r+", encoding="utf-8") as dosya:
dosya.seek(0)
dosya.truncate()
self.uyariOlustur(self.configGetir(base_warnings + "warning1"), 1)
    except (ValueError, TypeError, RuntimeError) as e:
        logger.error(f"Specific error occurred: {e}")
        raise
self.uyariOlustur(
2, 
)

async def takipcilerButon(self):
def takipcilerButon(self): -> Any
    return self.driver.find_elements_by_css_selector("ul.k9GMp >li.Y8-fY")[1]

async def takipEdilenlerButon(self):
def takipEdilenlerButon(self): -> Any
    return self.driver.find_elements_by_css_selector("ul.k9GMp >li.Y8-fY")[2]

async def takipcileriGetir(self):
def takipcileriGetir(self): -> Any
try:
logger.info(self.configGetir(base_warnings + "warning1"))
self.kullaniciProfilineYonlendir(self.aktifKullanici)

btn_takipciler.click()
self.indexSifirla()
while devamEtsinMi:
for takipci in takipcilerPopup:
"a.FPmhX"
).get_attribute("href")
self.metindenKarakterSil(takipciKullaniciAdi, self.BASE_URL), 
"/", 
)
if takipciKullaniciAdi not in takipciler:
logger.info(
str(self.configGetir(base_warnings + "warning2")).format(
)
)
takipciler.add(takipciKullaniciAdi)
self.indexArtir()
if (self.index - 1) >= takipciSayisi:
    break
if devamEtsinMi:
try:
    except (ValueError, TypeError, RuntimeError) as e:
        logger.error(f"Specific error occurred: {e}")
        raise
self.uyariOlustur(
str(self.configGetir(base_warnings + "warning3")).format(
), 
2, 
)
    pass
btn_close_dialog.click()
    return takipciler
    except (ValueError, TypeError, RuntimeError) as e:
        logger.error(f"Specific error occurred: {e}")
        raise
self.uyariOlustur(
2, 
)
self.menu()

async def takipEdilenleriGetir(self, takipciler):
def takipEdilenleriGetir(self, takipciler): -> Any
try:
btn_takipEdilenler.click()
self.indexSifirla()
while devamEtsinMi:
for takip in takipListe:

if takipEdilenKullanıcıAdi not in takipciler:
if btn_takip.text == "Following":
btn_takip.click()
try:
"div.mt3GC > button.aOOlW"
)
btn_onay.click()
    except (ValueError, TypeError, RuntimeError) as e:
        logger.error(f"Specific error occurred: {e}")
        raise
self.uyariOlustur(
str(self.configGetir(base_warnings + "warning1")).format(
), 
2, 
)
    continue
self.uyariOlustur(
str(self.configGetir(base_warnings + "warning2")).format(
), 
1, 
)
self.indexArtir()
if self.index - 1 >= takipEdilenSayisi:
    break
sleep(self.beklemeSuresiGetir(sleep3[0], sleep3[1]))
if islemIndex >= takipEdilenSayisi:
    break
if devamEtsinMi:
try:
    except (ValueError, TypeError, RuntimeError) as e:
        logger.error(f"Specific error occurred: {e}")
        raise
self.uyariOlustur(
str(self.configGetir(base_warnings + "warning3")).format(
), 
2, 
)
    pass

    except (ValueError, TypeError, RuntimeError) as e:
        logger.error(f"Specific error occurred: {e}")
        raise
self.uyariOlustur(
2, 
)
self.menu()

async def takipEdilenSayisiGetir(self):
def takipEdilenSayisiGetir(self): -> Any
"ul.k9GMp li.Y8-fY >a.-nal3 >span.g47SY"
)[-1].text
    return int(self.metindenKarakterSil(takipEdilenSayisi, ", "))

async def takipciSayisiGetir(self):
def takipciSayisiGetir(self): -> Any
"ul.k9GMp li.Y8-fY >a.-nal3 >span.g47SY"
)[0].get_attribute("title")
    return int(self.metindenKarakterSil(takipciSayisi, ", "))

async def takipEdilenKullaniciAdiGetir(self, element):
def takipEdilenKullaniciAdiGetir(self, element): -> Any
"href"
)
    return self.metindenKarakterSil(
self.metindenKarakterSil(takipEdilenKullanıcıAdi, self.BASE_URL), "/"
)

def girisYap(self, username = False, password = False): -> Any

try:
if not username and not password:
logger.info(" ")
logger.info(" ")
self.uyariOlustur(self.configGetir(base_warnings + "warning1"), 1)
elif not username:
elif not password:

if not username and not password:
self.uyariOlustur(self.configGetir(base_warnings + "warning2"), 2)
self.girisYap()
elif not username:
self.uyariOlustur(self.configGetir(base_warnings + "warning3"), 2)
self.girisYap(False, password)
elif not password:
self.uyariOlustur(self.configGetir(base_warnings + "warning4"), 2)
self.girisYap(username, False)

logger.info(self.configGetir(base_warnings + "warning5"))
usernameInput.send_keys(username.strip())
    passwordInput.send_keys(password.strip())
    passwordInput.send_keys(Keys.ENTER)
self.girisKontrol()
if self.girisYapildimi:
self.bildirimThreadOlustur()
self.menu()
else:
self.inputTemizle(usernameInput)
self.inputTemizle(passwordInput)
self.girisYap()
    except (ValueError, TypeError, RuntimeError) as e:
        logger.error(f"Specific error occurred: {e}")
        raise
self.uyariOlustur(
2, 
)

async def girisKontrol(self):
def girisKontrol(self): -> Any
if (
    "The username you entered doesn't belong to an account. Please check your username and try again."
    in self.driver.page_source
    ):
    self.uyariOlustur(self.configGetir(base_warnings + "warning1"), 2)
    elif (
        "Sorry, your password was incorrect. Please double-check your password."
        in self.driver.page_source
        ):
        self.uyariOlustur(self.configGetir(base_warnings + "warning2"), 2)
        elif self.BASE_URL + "accounts/login/two_factor" in self.driver.current_url:
        self.girisDogrulama()
        elif self.driver.current_url != self.BASE_URL + "accounts/login/":
        self.uyariOlustur(self.configGetir(base_warnings + "warning3"), 1)
    else:
    self.uyariOlustur(self.configGetir(base_warnings + "warning4"), 2)

    def girisDogrulama(self, durum = True): -> Any

    if not kod:
    self.girisYap(durum)

    if durum:
    kodInput.send_keys(kod)
    kodInput.send_keys(Keys.ENTER)
    if "A security code is required." in self.driver.page_source:
    self.uyariOlustur(self.configGetir(base_warnings + "warning1"), 2)
    self.inputTemizle(kodInput)
    self.girisDogrulama(False)
    elif "Please check the security code and try again." in self.driver.page_source:
    self.uyariOlustur(self.configGetir(base_warnings + "warning2"), 2)
    self.inputTemizle(kodInput)
    self.girisDogrulama(False)
    elif self.BASE_URL + "accounts/login/two_factor" not in self.driver.current_url:
    self.uyariOlustur(self.configGetir(base_warnings + "warning3"), 1)
else:
self.uyariOlustur(self.configGetir(base_warnings + "warning4"), 2)

async def etiketGetir(self):
def etiketGetir(self): -> Any
try:
self.anaMenuyeDonsunMu(etiket)

if self.degerVarMi(etiket):
)
self.urlYonlendir(url)
if not self.sayfaMevcutMu():
self.uyariOlustur(
2, 
)
    return self.etiketGetir()
    return etiket
else:
self.uyariOlustur(self.configGetir(base_warnings + "warning3"), 2)
    return self.etiketGetir()
    except (ValueError, TypeError, RuntimeError) as e:
        logger.error(f"Specific error occurred: {e}")
        raise
self.uyariOlustur(
2, 
)

async def etiketeGoreIslemLimitiGetir(self, islemNo):
def etiketeGoreIslemLimitiGetir(self, islemNo): -> Any
try:
if islemNo == 1:
elif islemNo == 2:

self.anaMenuyeDonsunMu(limit)
if limit.isnumeric() and int(limit) > 0:
    return int(limit)
else:
self.uyariOlustur(self.configGetir(base_warnings + "warning1"), 2)
    except (ValueError, TypeError, RuntimeError) as e:
        logger.error(f"Specific error occurred: {e}")
        raise
self.uyariOlustur(
2, 
)
if islemNo == 1:
self.etiketeGoreBegenme()
elif islemNo == 2:
self.etiketeGoreTakipEtme()

async def hikayeVarMi(self):
def hikayeVarMi(self): -> Any
try:
"aria-disabled"
)
if durum == "false":
    return True
else:
    return False
    except (ValueError, TypeError, RuntimeError) as e:
        logger.error(f"Specific error occurred: {e}")
        raise
self.uyariOlustur(
2, 
)

async def hikayeVideoMu(self):
def hikayeVideoMu(self): -> Any
try:
self.driver.find_element_by_css_selector("div.qbCDp > video.y-yJ5")
    return True
    except (ValueError, TypeError, RuntimeError) as e:
        logger.error(f"Specific error occurred: {e}")
        raise
    return False

async def hikayeSayisiGetir(self):
def hikayeSayisiGetir(self): -> Any
try:
    return len(hikayeSayisi)
    except (ValueError, TypeError, RuntimeError) as e:
        logger.error(f"Specific error occurred: {e}")
        raise
self.uyariOlustur(
2, 
)

async def hikayeleriGetir(self):
def hikayeleriGetir(self): -> Any

try:
for i in range(self.hikayeSayisiGetir()):
if self.hikayeVideoMu():
"div.qbCDp > video.y-yJ5 > source"
).get_attribute("src")
self.dosyaIndir(url, 2)
else:
self.driver.find_element_by_css_selector(
"div.qbCDp >  img.y-yJ5"
).get_attribute("srcset")
)
self.dosyaIndir(url, 1)
btn_ileri.click()
    except (ValueError, TypeError, RuntimeError) as e:
        logger.error(f"Specific error occurred: {e}")
        raise
self.uyariOlustur(
2, 
)

async def yorumUzunlukBelirle(self, yorum):
def yorumUzunlukBelirle(self, yorum): -> Any
    return yorum[0 : randint(5, DEFAULT_BATCH_SIZE)]

async def yorumYap(self, yorum):
def yorumYap(self, yorum): -> Any
try:

self.inputTemizle(textarea)
textarea.click()

textarea.send_keys(yorum)
textarea.send_keys(Keys.ENTER)
    except (ValueError, TypeError, RuntimeError) as e:
        logger.error(f"Specific error occurred: {e}")
        raise
self.uyariOlustur(
2, 
)

async def rastgeleYorumGetir(self):
def rastgeleYorumGetir(self): -> Any
try:
    return requests.get("http://metaphorpsum.com/paragraphs/1/1", headers = DEFAULT_HEADERS).text
    except (ValueError, TypeError, RuntimeError) as e:
        logger.error(f"Specific error occurred: {e}")
        raise
self.uyariOlustur(
2, 
)

async def yorumLimitiAsildiMi(self, yorumSayisi):
def yorumLimitiAsildiMi(self, yorumSayisi): -> Any
if yorumSayisi > 50:
    return True
else:
    return False

async def mesajSil(self, mesaj):
def mesajSil(self, mesaj): -> Any
mesaj.click()
sleep(self.beklemeSuresiGetir(sleep1[0], sleep1[1]))
self.driver.find_element_by_css_selector("div.PjuAP button.wpO6b").click()
sleep(self.configGetir(base + "sleep2"))
self.driver.find_elements_by_css_selector("div._9XapR >div._7zBYT button.sqdOP")[0].click()
sleep(self.configGetir(base + "sleep3"))
self.driver.find_elements_by_css_selector("div.mt3GC >button.aOOlW")[0].click()

async def kullaniciEngelDurumDegistir(self):
def kullaniciEngelDurumDegistir(self): -> Any
self.driver.find_element_by_css_selector("button.wpO6b").click()
self.driver.find_elements_by_css_selector("div.mt3GC > button.aOOlW")[0].click()
self.driver.find_elements_by_css_selector("div.mt3GC > button.aOOlW")[0].click()

async def kullaniciTakipDurumDegistir(self, kullanici, durum):
def kullaniciTakipDurumDegistir(self, kullanici, durum): -> Any

if self.hesapGizliMi():
if durum:
if btn_text in ["follow", "follow back"]:
btn_takip.click()
self.uyariOlustur(
str(self.configGetir(base_warnings + "warning1")).format(
), 
1, 
)
elif btn_text == "requested":
logger.info(
str(self.configGetir(base_warnings + "warning2")).format(
)
)
elif btn_text == "unblock":
self.uyariOlustur(
str(self.configGetir(base_warnings + "warning3")).format(
), 
2, 
)
else:
if btn_text == "requested":
btn_takip.click()
self.driver.find_elements_by_css_selector("div.mt3GC >button.aOOlW")[0].click()
self.uyariOlustur(
str(self.configGetir(base_warnings + "warning8")).format(
), 
1, 
)
else:
logger.info(
str(self.configGetir(base_warnings + "warning4")).format(
)
)

else:
if durum:
if btn_text in ["follow", "follow back"]:
btn_takip.click()
self.uyariOlustur(
str(self.configGetir(base_warnings + "warning5")).format(
), 
1, 
)
elif btn_text == "unblock":
self.uyariOlustur(
str(self.configGetir(base_warnings + "warning6")).format(
), 
2, 
)
else:
"aria-label"
)
if ariaLabel == "Following":
logger.info(
str(self.configGetir(base_warnings + "warning7")).format(
)
)
else:
try:
"aria-label"
)
if ariaLabel == "Following":
btn_takip.click()
self.driver.find_elements_by_css_selector("div.mt3GC >button.aOOlW")[
0
].click()
self.uyariOlustur(
str(self.configGetir(base_warnings + "warning8")).format(
), 
1, 
)
else:
logger.info(
str(self.configGetir(base_warnings + "warning4")).format(
)
)
    except (ValueError, TypeError, RuntimeError) as e:
        logger.error(f"Specific error occurred: {e}")
        raise
logger.info(
str(self.configGetir(base_warnings + "warning4")).format(
)
)

async def gonderiIlerlet(self):
def gonderiIlerlet(self): -> Any
try:
self.driver.find_element_by_css_selector("a._65Bje").click()
    except (ValueError, TypeError, RuntimeError) as e:
        logger.error(f"Specific error occurred: {e}")
        raise
    pass

async def gonderiBegenDurumDegistir(self, btn):
def gonderiBegenDurumDegistir(self, btn): -> Any
btn.click()
self.indexArtir()
self.gonderiIlerlet()
sleep(self.beklemeSuresiGetir(sleep2[0], sleep2[1]))

async def begenButon(self):
def begenButon(self): -> Any
    return self.driver.find_element_by_css_selector(
"article.M9sTE section.ltpMr >span.fr66n >button"
)

async def begenButonuDurumGetir(self, buton):
def begenButonuDurumGetir(self, buton): -> Any
    return str(buton.find_element_by_tag_name("svg").get_attribute("aria-label")).lower()

async def gonderiVarMi(self, kullanici, gonderiSayisi, secim):
def gonderiVarMi(self, kullanici, gonderiSayisi, secim): -> Any
if gonderiSayisi < 1:
self.uyariOlustur(
2, 
)
self.profilSec(secim)

async def gonderiSayisi(self):
def gonderiSayisi(self): -> Any
    return self.driver.find_element_by_css_selector("ul.k9GMp >li.Y8-fY >span >span.g47SY").text

def gonderiTipiVideoMu(self, element = None): -> Any
try:
if element:
element.find_element_by_css_selector("video.tWeCl")
else:
self.driver.find_element_by_css_selector("video.tWeCl")
    return True
    except (ValueError, TypeError, RuntimeError) as e:
        logger.error(f"Specific error occurred: {e}")
        raise
    return False

async def gonderiUrlGetir(self):
def gonderiUrlGetir(self): -> Any
try:
if self.gonderiTipiVideoMu():
else:
"article.M9sTE div.KL4Bh > img.FFVAD"
).get_attribute("src")
    return url, veriTuru
    except (ValueError, TypeError, RuntimeError) as e:
        logger.error(f"Specific error occurred: {e}")
        raise
self.uyariOlustur(
2, 
)
    return None, None

async def gonderiAlbumMu(self):
def gonderiAlbumMu(self): -> Any
try:
self.driver.find_element_by_css_selector("div.Yi5aA")
    return True
    except (ValueError, TypeError, RuntimeError) as e:
        logger.error(f"Specific error occurred: {e}")
        raise
    return False

async def albumUrlGetir(self):
def albumUrlGetir(self): -> Any

try:
for i in range(self.albumIcerikSayisiGetir()):
for li in liste:
if url not in album and url is not None:
album.add(url)
self.dosyaIndir(url, veriTuru)
"button._6CZji div.coreSpriteRightChevron"
)
btn_ileri.click()
    except (ValueError, TypeError, RuntimeError) as e:
        logger.error(f"Specific error occurred: {e}")
        raise
    pass

async def albumIcerikSayisiGetir(self):
def albumIcerikSayisiGetir(self): -> Any
try:
    return len(self.driver.find_elements_by_css_selector("div.Yi5aA"))
    except (ValueError, TypeError, RuntimeError) as e:
        logger.error(f"Specific error occurred: {e}")
        raise
self.uyariOlustur(
str(self.configGetir(base_warnings + "warning1")).format(
), 
2, 
)
    return None

async def albumIcerikUrlGetir(self, element):
def albumIcerikUrlGetir(self, element): -> Any
try:
if self.gonderiTipiVideoMu(element):
else:
    return url, veriTuru
    except (ValueError, TypeError, RuntimeError) as e:
        logger.error(f"Specific error occurred: {e}")
        raise
self.uyariOlustur(
2, 
)
    return None, None

async def aktifKullaniciGetir(self):
def aktifKullaniciGetir(self): -> Any
try:
self.driver.find_elements_by_css_selector("div._47KiJ > div.Fifk5")[-1].click()
0
].get_attribute("href")
    except (ValueError, TypeError, RuntimeError) as e:
        logger.error(f"Specific error occurred: {e}")
        raise
self.uyariOlustur(
2, 
)
self.aktifKullaniciGetir()

async def anaMenuyeDonsunMu(self, deger):
def anaMenuyeDonsunMu(self, deger): -> Any
if deger == "menu":
self.menu()

async def BASE_AYARLAR(self):
def BASE_AYARLAR(self): -> Any
try:
    except (ValueError, TypeError, RuntimeError) as e:
        logger.error(f"Specific error occurred: {e}")
        raise
self.uyariOlustur(
2, 
)

async def BASE_SLEEP(self, metod):
def BASE_SLEEP(self, metod): -> Any
try:
    except (ValueError, TypeError, RuntimeError) as e:
        logger.error(f"Specific error occurred: {e}")
        raise
self.uyariOlustur(
2, 
)

def BASE_UYARI(self, metod, warnings = None, inputs = None): -> Any
try:
if warnings:
    return "languages.{dil}.warnings.{metod}.warnings.".format(
)
elif inputs:
    return "languages.{dil}.warnings.{metod}.inputs.".format(
)
else:
    return "languages.{dil}.warnings.{metod}.".format(
)
    except (ValueError, TypeError, RuntimeError) as e:
        logger.error(f"Specific error occurred: {e}")
        raise
self.uyariOlustur(
)

async def beklemeSuresiGetir(self, baslangic, bitis):
def beklemeSuresiGetir(self, baslangic, bitis): -> Any
    return randint(baslangic, bitis)

async def bildirimThreadOlustur(self):
def bildirimThreadOlustur(self): -> Any
t1.start()

async def bildirimPopupKapat(self):
def bildirimPopupKapat(self): -> Any
try:
for i in range(2):
if btn:
self.driver.execute_script("arguments[0].click();", btn)
self.aktifKullaniciGetir()
self.aktifKullaniciGetir()

    except (ValueError, TypeError, RuntimeError) as e:
        logger.error(f"Specific error occurred: {e}")
        raise
    pass

async def popupAsagiKaydir(self, secici):
def popupAsagiKaydir(self, secici): -> Any
self.driver.execute_script(
"""
""".format(
)
)

async def hesapGizliMi(self):
def hesapGizliMi(self): -> Any
if "This Account is Private" in self.driver.page_source:
    return True
else:
    return False

async def sayfaMevcutMu(self):
def sayfaMevcutMu(self): -> Any
if "Sorry, this page isn't available." not in self.driver.page_source:
    return True
else:
    return False

async def kullanicilariTakipEt(self, kullaniciListesi, secim):
def kullanicilariTakipEt(self, kullaniciListesi, secim): -> Any
logger.info(self.configGetir(base_warnings + "warning1"))
for kullanici in kullaniciListesi:
if self.kullaniciKontrol(kullanici):
sleep(self.beklemeSuresiGetir(sleep1[0], sleep1[1]))
logger.info(self.configGetir(base_warnings + "warning2"))

async def kullaniciKontrol(self, kullanici):
def kullaniciKontrol(self, kullanici): -> Any
    return self.urlKontrol(self.BASE_URL + kullanici)

async def kullaniciProfilineYonlendir(self, kullanici):
def kullaniciProfilineYonlendir(self, kullanici): -> Any
self.driver.get(self.BASE_URL + kullanici)

def urlGirildiMi(self, url, metod, metodDeger = None): -> Any
if url is None or len(url) < 12:
self.uyariOlustur(self.configGetir(base_warnings + "warning1"), 2)
if metodDeger:
if "gonderiYorumYapma" == metod.__name__:
metod(metodDeger)
metod()

def urlGecerliMi(self, url, metod, metodDeger = None): -> Any
if not self.urlKontrol(url):
self.uyariOlustur(self.configGetir(base_warnings + "warning1"), 2)
if metodDeger:
if "gonderiYorumYapma" == metod.__name__:
metod(metodDeger)
metod()

async def urlKontrol(self, url):
def urlKontrol(self, url): -> Any
try:
if response.status_code == 404:
    return False
else:
    return True
    except (ValueError, TypeError, RuntimeError) as e:
        logger.error(f"Specific error occurred: {e}")
        raise
    return False

async def urlYonlendir(self, url):
def urlYonlendir(self, url): -> Any
self.driver.get(url)

async def uyariOlustur(self, mesaj, durum):
def uyariOlustur(self, mesaj, durum): -> Any
if durum == 1:
elif durum == 2:
elif durum == MAX_RETRIES:
logger.info(uyari)

async def dosyaAdiOlustur(self, veriTuru):
def dosyaAdiOlustur(self, veriTuru): -> Any
if veriTuru == 1:
elif veriTuru == 2:
    return isim

async def dosyaIndir(self, url, veriTuru):
def dosyaIndir(self, url, veriTuru): -> Any
try:
urllib.request.urlretrieve(url, dosyaAdi)
self.indexArtir()
    except (ValueError, TypeError, RuntimeError) as e:
        logger.error(f"Specific error occurred: {e}")
        raise
self.uyariOlustur(
2, 
)

async def dosyaSec(self):
def dosyaSec(self): -> Any
try:
self.anaMenuyeDonsunMu(dosyaAdi)
if self.dosyaMevcutMu(dosyaAdi) and self.txtDosyasiMi(dosyaAdi):
    return str(dosyaAdi)
else:
self.uyariOlustur(self.configGetir(base_warnings + "warning1"), 2)
    return self.dosyaSec()
    except (ValueError, TypeError, RuntimeError) as e:
        logger.error(f"Specific error occurred: {e}")
        raise
self.uyariOlustur(
2, 
)
    return self.dosyaSec()

async def dosyaIceriginiAl(self, dosya):
def dosyaIceriginiAl(self, dosya): -> Any
try:
with open(dosya, "r", encoding="utf-8") as satirlar:
for satir in satirlar:
if len(satir.strip()) > 0:
icerik.add(satir.strip())
    return icerik
    except (ValueError, TypeError, RuntimeError) as e:
        logger.error(f"Specific error occurred: {e}")
        raise
self.uyariOlustur(
2, 
)
    return False

async def dosyaIcerigiAlindiMi(self, icerik):
def dosyaIcerigiAlindiMi(self, icerik): -> Any
if icerik:
    return True
else:
    return False

async def dosyaMevcutMu(self, path):
def dosyaMevcutMu(self, path): -> Any
if os.path.isfile(path):
    return True
else:
    return False

async def txtDosyasiMi(self, dosya):
def txtDosyasiMi(self, dosya): -> Any
if os.path.splitext(dosya)[-1].lower() == ".txt":
    return True
else:
    return False

async def klasorOlustur(self, klasor):
def klasorOlustur(self, klasor): -> Any
if not os.path.exists(klasor):
os.mkdir(klasor)
self.uyariOlustur(
1, 
)
else:
self.klasorDegistir(klasor)

async def klasorDegistir(self, klasor):
def klasorDegistir(self, klasor): -> Any
os.chdir(klasor)

async def metindenKarakterSil(self, metin, silinecekKarakterler):
def metindenKarakterSil(self, metin, silinecekKarakterler): -> Any
    return metin.replace(silinecekKarakterler, "")

async def inputTemizle(self, inpt):
def inputTemizle(self, inpt): -> Any
inpt.clear()

async def hedefKaynaktanBuyukMu(self, hedef, kaynak):
def hedefKaynaktanBuyukMu(self, hedef, kaynak): -> Any
if hedef > kaynak:
    return hedef

async def indexSifirla(self):
def indexSifirla(self): -> Any

async def indexArtir(self):
def indexArtir(self): -> Any

async def degerVarMi(self, yorum):
def degerVarMi(self, yorum): -> Any
if len(yorum) > 0:
    return True
else:
    return False


try:
except KeyboardInterrupt:
logger.info("\\\\\\n [*] Signing out from the application...")
exit()


if __name__ == "__main__":
    main()
