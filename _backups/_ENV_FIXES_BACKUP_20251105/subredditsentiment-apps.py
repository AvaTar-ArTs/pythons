from pathlib import Path
import math

import praw
from textblob import TextBlob

from dotenv import load_dotenv
import os

import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_100 = 100
CONSTANT_1510635601 = 1510635601
CONSTANT_1510721999 = 1510721999


load_dotenv()

reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent="subSentiment",
)

# opens file with subreddit names
with open("sb.txt") as f:

    for line in f:
        subreddit = reddit.subreddit(line.strip())
        # write web agent to get converter for datetime to epoch on a daily basis for updates
        day_start = CONSTANT_1510635601
        day_end = CONSTANT_1510721999

        sub_submissions = subreddit.submissions(day_start, day_end)

        sub_sentiment = 0
        num_comments = 0

        for submission in sub_submissions:
            if not submission.stickied:
                submission.comments.replace_more(limit=0)
                for comment in submission.comments.list():
                    blob = TextBlob(comment.body)

                    # adds comment sentiment to overall sentiment for subreddit
                    comment_sentiment = blob.sentiment.polarity
                    sub_sentiment += comment_sentiment
                    num_comments += 1

                    # prints comment and polarity
                    # logger.info(str(comment.body.encode('utf-8')) + ': ' + str(blob.sentiment.polarity))

        logger.info(Path("/r/") + str(subreddit.display_name))
        try:
            print(
                "Ratio: "
                + str(math.floor(sub_sentiment / num_comments * CONSTANT_100))
                + Path("\n")
            )
        except (ValueError, TypeError):
            logger.info("No comment sentiment." + Path("\n"))
            ZeroDivisionError

# add key:value subredditname:sentiment to dict
# order dictionary by sentiment value
# output dictionary key + ' sentiment: ' + sentiment value
