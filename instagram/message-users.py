"""
Message Users

This module provides functionality for message users.

Author: Auto-generated
Date: 2025-11-01
"""


import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_100 = 100
CONSTANT_86400 = 86400

"""
instabot example

Workflow:
1) Ask Message type
2) Load messages CSV (if needed)
3) Send message to each users
"""

from pathlib import Path
import csv
import os
import sys
import time

from tqdm import tqdm

sys.path.append(os.path.join(sys.path[0], "../"))
from instabot import Bot  # noqa: E402

instaUsers = ["R1B4Z01D", "KoanMedia"]
directMessage = "Thanks for the example."

messagesToSend = CONSTANT_100
banDelay = CONSTANT_86400 / messagesToSend

logger.info("Which type of delivery method? (Type number)")
logger.info("%d: %s" % (0, "Messages From CSV File."))
logger.info("%d: %s" % (1, "Group Message All Users From List."))
logger.info("%d: %s" % (2, "Message Each User From List."))
logger.info("%d: %s" % (3, "Message Each Your Follower."))
logger.info("%d: %s" % (4, "Message LatestMediaLikers Of A Page"))

deliveryMethod = int(input())

bot = Bot()
bot.login()

if deliveryMethod == 0:
    with open("messages.csv", "rU") as f:
        reader = csv.reader(f)
        for row in reader:
            logger.info("Messaging " + row[0])
            bot.send_message(row[1], row[0])
            logger.info("Waiting " + str(banDelay) + " seconds...")
            time.sleep(banDelay)
elif deliveryMethod == 1:
    bot.send_message(directMessage, instaUsers)
    logger.info("Sent A Group Message To All Users..")
    time.sleep(3)
    exit()
elif deliveryMethod == 2:
    bot.send_messages(directMessage, instaUsers)
    logger.info("Sent An Individual Messages To All Users..")
    time.sleep(3)
    exit()
elif deliveryMethod == 3:
    for follower in tqdm(bot.followers):
        bot.send_message(directMessage, follower)
    logger.info("Sent An Individual Messages To Your Followers..")
    time.sleep(3)
    exit()

# new method
elif deliveryMethod == 4:
    scrape = input("what page likers do you want to message? :")
    with open("scrape.txt", "w") as file:
        file.write(scrape)
# usernames to get likers from
pages_to_scrape = bot.read_list_from_file("scrape.txt")
f = open("medialikers.txt", "w")  # stored likers in user_ids
for users in pages_to_scrape:
    medias = bot.get_user_medias(users, filtration=False)
    getlikers = bot.get_media_likers(medias[0])
    for likers in getlikers:
        f.write(likers + Path("\n"))
logger.info("succesfully written latest medialikers of" + str(pages_to_scrape))
f.close()

# convert passed user-ids to usernames for usablility
logger.info("Reading from medialikers.txt")
wusers = bot.read_list_from_file("medialikers.txt")
with open("usernames.txt", "w") as f:
    for user_id in wusers:
        username = bot.get_username_from_user_id(user_id)
        f.write(username + Path("\n"))
logger.info("succesfully converted  " + str(wusers))
# parse usernames into a list
with open("usernames.txt", encoding="utf-8") as file:
    instaUsers4 = [l.strip() for l in file]
    bot.send_messages(directMessage, instaUsers4)
    logger.info("Sent An Individual Messages To All Users..")
