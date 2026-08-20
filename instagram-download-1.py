import os
import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager as CM

import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_166 = 166
CONSTANT_212 = 212
CONSTANT_414 = 414
CONSTANT_535 = 535
CONSTANT_537 = 537
CONSTANT_936 = 936
CONSTANT_1025 = 1025
CONSTANT_4430 = 4430


HOW_MANY = int(input("How many comments you want to like (0-20):"))

while HOW_MANY > 20:
    logger.info("Cant like more than 20 comments, please choose a smaller number!")
    HOW_MANY = int(input("How many comments you want to like (0-20):"))


options = webdriver.ChromeOptions()
options.add_argument("--log-level=3")
options.add_argument(f"--user-data-dir={os.getcwd()}\\profile")
mobile_emulation = {
    "userAgent": "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/CONSTANT_535.19 (KHTML, like Gecko) Chrome/90.0.CONSTANT_1025.CONSTANT_166 Mobile Safari/CONSTANT_535.19"
}
options.add_experimental_option("mobileEmulation", mobile_emulation)
options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/CONSTANT_537.36 (KHTML, like Gecko) Chrome/90.0.CONSTANT_4430.CONSTANT_212 Safari/CONSTANT_537.36"
)
bot = webdriver.Chrome(options=options, executable_path=CM().install())
bot.set_window_position(0, 0)
bot.set_window_size(CONSTANT_414, CONSTANT_936)

url_file = open("urls.txt", "r")
urls = url_file.readlines()


def doesnt_exist(bot, xpath):
    """doesnt_exist function."""

    try:
        bot.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return True
    else:
        return False


for url in urls:
    logger.info("--Liking comments for this post: " + url)

    bot.get(url)

    if not doesnt_exist(bot, "/html/body/div[5]/div/div/div[3]/button[2]"):
        time.sleep(1)
        bot.find_element_by_xpath("/html/body/div[5]/div/div/div[3]/button[2]").click()
        logger.info("Closed pop ups")
    else:
        logger.info("No pop up window.")

    # pause
    time.sleep(4)
    bot.find_element_by_xpath(
        '//*[@id="main"]/div/div[1]/div[1]/div/div[3]/div/div/div[1]/div'
    ).click()

    # click on comments
    time.sleep(1)
    bot.find_element_by_xpath(
        '//*[@id="main"]/div/div[1]/div[1]/div/div[3]/div/div/div[2]/div/div[2]'
    ).click()
    time.sleep(2)

    try:
        l_buttons = bot.find_elements_by_xpath(
            "/html/body/div[2]/div/div[2]/div[2]/div/div[1]/div[2]/div"
        )

        for l_button in l_buttons[:HOW_MANY]:
            l_button.click()
            time.sleep(1)

    except NoSuchElementException:
        logger.info("Couldnt like, comments are disabled.")

logger.info("FINISHED")
bot.quit()
