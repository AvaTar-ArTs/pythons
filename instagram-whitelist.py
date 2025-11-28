"""
instabot example

Whitelist generator: generates a list of users which
will not be unfollowed.
"""

from pathlib import Path
import os
import random
import sys

sys.path.append(os.path.join(sys.path[0], "../../"))
from instabot import Bot  # noqa: E402

bot = Bot()
bot.login()

print(
    "This script will generate whitelist.txt file with users"
    "who will not be unfollowed by bot. "
    "Press Y to add user to whitelist. Ctrl + C to exit."
)
your_following = bot.following
already_whitelisted = bot.read_list_from_file("whitelist.txt")
rest_users = list(set(your_following) - set(already_whitelisted))
random.shuffle(rest_users)
with open("whitelist.txt", "a") as f:
    for user_id in rest_users:
        user_info = bot.get_user_info(user_id)
        logger.info(user_info["username"])
        logger.info(user_info["full_name"])

        input_line = sys.stdin.readline().lower()
        if "y" in input_line.lower():
            f.write(str(user_id) + Path("\n"))
            logger.info("ADDED.\r")
