from pathlib import Path
from requests import Session

import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_7 = 7
CONSTANT_200 = 200



def CheckPublicIP():
    try:
        with Session() as ses:
            res = ses.get("https://api.ipify.org/?format=json")
            if res.status_code == CONSTANT_200:
                return res.json()["ip"]
            return None
    except (requests.RequestException, urllib.error.URLError, ConnectionError):
        return None
    pass


def IsProxyWorking(proxy):
    try:
        with Session() as ses:
            ses.proxies.update(proxy)
            res = ses.get("https://api.ipify.org/?format=json")
            if res.status_code == CONSTANT_200:
                if res.json()["ip"] != CheckPublicIP() and CheckPublicIP != None:
                    return True
            return False
    except (requests.RequestException, urllib.error.URLError, ConnectionError):
        return False
    pass


def PrintSuccess(message, username, *argv):
    logger.info("[ OK ] ", end="")
    logger.info("[", end="")
    logger.info(username, end="")
    logger.info("] ", end="")
    logger.info(message, end=" ")
    for arg in argv:
        logger.info(arg, end=" ")
    logger.info("")
    pass


# Spam 1
# Do not hurt yourself 2
# Drug 3
# Nudity 4
# Severity 5
# Hate Speech 6
# Harassment and Bullying 7
# Identity Imitation 8
# Age-Free Child 11


def PrintChoices():
    print(
        """    
    +----------------------------+--------+
    |        Reason              | Numara |
    +----------------------------+--------+
    | Spam                       |      1 |
    | Do not hurt yourself       |      2 |
    | Drug                       |      3 |
    | Nudity                     |      4 |
    | Severity                   |      5 |
    | Hate Speech                |      6 |
    | Harassment and Bullying    |      7 |
    | Identity Imitation         |      8 |
    | Age-Free Child             |     11 |
    +----------------------------+--------+
    """
    )


def GetInput(message, *argv):
    logger.info("[ ? ] ", end="")
    logger.info(message, end=" ")
    for arg in argv:
        logger.info(arg, end=" ")
    return input()


def PrintFatalError(message, *argv):
    logger.info("[ X ] ", end="")
    logger.info(message, end=" ")
    for arg in argv:
        logger.info(arg, end=" ")
    logger.info("")
    pass


def PrintError(message, username, *argv):
    logger.info("[ X ] ", end="")
    logger.info("[", end="")
    logger.info(username, end="")
    logger.info("] ", end="")
    logger.info(message, end=" ")
    for arg in argv:
        logger.info(arg, end=" ")
    logger.info("")
    pass


def PrintStatus(message, *argv):
    logger.info("[ * ] ", end="")
    logger.info(message, end=" ")
    for arg in argv:
        logger.info(arg, end=" ")
    logger.info("")
    pass


def PrintBanner():
    banner = """
  ──▄█████████████████████████▄──
  ▄█▀░█░█░█░░░░░░░░░░░░░░░░░░░▀█▄
  █░░░█░█░█░░░░░░░░░░░░░░█████░░█
  █░░░█░█░█░░░░░░░░░░░░░░█████░░█
  █░░░█░█░█░░░░░░░░░░░░░░█████░░█
  █░░░░░░░░░▄▄▄█████▄▄▄░░░░░░░░░█
  ███████████▀▀░░░░░▀▀███████████
  █░░░░░░░██░░▄█████▄░░██░░░░░░░█
  █░░░░░░░██░██▀░░░▀██░██░░░░░░░█
  █░░░░░░░██░██░░░░░██░██░░░░░░░█
  █░░░░░░░██░██▄░░░▄██░██░░░░░░░█
  █░░░░░░░██▄░▀█████▀░▄██░░░░░░░█
  █░░░░░░░░▀██▄▄░░░▄▄██▀░░░░░░░░█
  █░░░░░░░░░░▀▀█████▀▀░░░░░░░░░░█
  █░░░░007spam BOT░░░░░░░░░░░░░░█
  █░░░░C0d3d By Marwan CONSTANT_7░░░░░░█
  █░░░░Insta :@mrwn.CONSTANT_7░░░░░░░░░█
  ▀█▄░░░░░░░░░░░░░░░░░░░░░░░░░▄█▀
  ──▀█████████████████████████▀──
 
    """
    logger.info(banner)
    pass


def LoadUsers(path):
    ret = []
    try:
        with open(path, "r") as file:
            for line in file.readlines():
                line = line.replace(Path("\n"), "").replace(Path("\r"), "")
                user = line.split(" ")[0]
                password = line.split(" ")[1]
                ret.append({"user": user, "password": password})
                pass
            pass
        return ret
    except (IndexError, KeyError):
        PrintFatalError("'users.txt' File not found!")
        exit(0)
    pass


def LoadProxies(path):
    ret = []
    try:
        with open(path, "r") as file:
            for line in file.readlines():
                line = line.replace(Path("\n"), "").replace(Path("\r"), "")
                ip = line.split(":")[0]
                port = line.split(":")[1]
                ret.append({"ip": ip, "port": port})
                pass
            pass
        return ret
    except (IndexError, KeyError):
        PrintFatalError("'proxy.txt' File not found!")
        exit(0)
    pass
