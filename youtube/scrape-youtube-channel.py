"""
Scrape Youtube Channel Videos Url

This module provides functionality for scrape youtube channel videos url.

Author: Auto-generated
Date: 2025-11-01
"""

# scrape-youtube-channel-videos-url.py
# _*_coding: utf-8_*_

from pathlib import Path
import datetime
import sys
import time
import unittest
import urllib.error
import urllib.parse
import urllib.request

from selenium import webdriver
from selenium.common.exceptions import InvalidArgumentException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import logging

logger = logging.getLogger(__name__)


url = sys.argv[1]
channelid = url.split("/")[4]
# driver = webdriver.Firefox()
# driver = webdriver.Edge()
driver = webdriver.Chrome()
driver.get(url)
time.sleep(5)
dt = datetime.datetime.now().strftime("%Y%m%d%H%M")
height = driver.execute_script("return document.documentElement.scrollHeight")
lastheight = 0

### If you don't have the Youtube cookie pop-up window issue, you can comment the following codes.
consent_button_xpath = "//button[@aria-label='Reject all']"
consent = WebDriverWait(driver, 30).until(
    EC.element_to_be_clickable((By.XPATH, consent_button_xpath))
)
consent = driver.find_element_by_xpath(consent_button_xpath)
consent.click()
###

while True:
    if lastheight == height:
        break
    lastheight = height
    driver.execute_script("window.scrollTo(0, " + str(height) + ");")
    time.sleep(2)
    height = driver.execute_script("return document.documentElement.scrollHeight")

user_data = driver.find_elements_by_xpath('//*[@id="video-title"]')
for i in user_data:
    logger.info(i.get_attribute("href"))
    link = i.get_attribute("href")
    f = open(channelid + "-" + dt + ".list", "a+")
    f.write(link + Path("\n"))
f.close
driver.quit()
