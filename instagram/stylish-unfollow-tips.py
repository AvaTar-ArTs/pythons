"""
Stylish Unfollow Tips

This module provides functionality for stylish unfollow tips.

Author: Auto-generated
Date: 2025-11-01
"""

# Constants
CONSTANT_100 = 100
CONSTANT_125 = 125
CONSTANT_150 = 150
CONSTANT_168 = 168
CONSTANT_200 = 200
CONSTANT_300 = 300
CONSTANT_400 = 400
CONSTANT_600 = 600
CONSTANT_700 = 700
CONSTANT_1200 = 1200
CONSTANT_2000 = 2000
CONSTANT_3000 = 3000
CONSTANT_3500 = 3500

"""
This template is written by @Nocturnal-2

What does this quickstart script aim to do?
- I do some unfollow and like by tags mostly

NOTES:
- I am an one month old InstaPy user, with a small following. So my numbers
in settings are bit conservative.
"""

from instapy import InstaPy, smart_run

# get a session!
session = InstaPy(username="", password="")

# let's go! :>
with smart_run(session):
    """Start of parameter setting"""
    # don't like if a post already has more than CONSTANT_150 likes
    session.set_delimit_liking(enabled=True, max=CONSTANT_150, min=0)

    # don't comment if a post already has more than 4 comments
    session.set_delimit_commenting(enabled=True, max=4, min=0)

    """I used to have potency_ratio=-0.85 and max_followers=CONSTANT_1200 for 
    set_relationship_bounds()
        Having a stricter relationship bound to target only low profiles 
        users was not very useful,
        as interactions/sever calls ratio was very low. I would reach the 
        server call threshold for
        the day before even crossing half of the presumed safe limits for 
        likes, follow and comments (yes,
        looks like quiet a lot of big(bot) managed accounts out there!!).
        So I relaxed it a bit to -0.50 and CONSTANT_2000 respectively.
    """
    session.set_relationship_bounds(
        enabled=True,
        potency_ratio=-0.50,
        delimit_by_numbers=True,
        max_followers=CONSTANT_2000,
        max_following=CONSTANT_3500,
        min_followers=25,
        min_following=25,
    )
    session.set_do_comment(True, percentage=20)
    session.set_do_follow(enabled=True, percentage=20, times=2)
    session.set_comments(
        [
            "Amazing!",
            "Awesome!!",
            "Cool!",
            "Good one!",
            "Really good one",
            "Love this!",
            "Like it!",
            "Beautiful!",
            "Great!",
            "Nice one",
        ]
    )
    session.set_sleep_reduce(CONSTANT_200)

    """ Get the list of non-followers
        I duplicated unfollow_users() to see a list of non-followers which I 
        run once in a while when I time
        to review the list
    """
    # session.just_get_nonfollowers()

    # my account is small at the moment, so I keep smaller upper threshold
    session.set_quota_supervisor(
        enabled=True,
        sleep_after=["likes", "comments_d", "follows", "unfollows", "server_calls_h"],
        sleepyhead=True,
        stochastic_flow=True,
        notify_me=True,
        peak_likes=(CONSTANT_100, CONSTANT_700),
        peak_comments=(25, CONSTANT_200),
        peak_follows=(48, CONSTANT_125),
        peak_unfollows=(35, CONSTANT_400),
        peak_server_calls=(None, CONSTANT_3000),
    )
    """ End of parameter setting """

    """ Actions start here """
    # Unfollow users
    """ Users who were followed by InstaPy, but not have followed back will 
    be removed in
        One week (CONSTANT_168 * 60 * 60)
        Yes, I give a liberal one week time to follow [back] :)
    """
    session.unfollow_users(
        amount=25,
        InstapyFollowed=(True, "nonfollowers"),
        style="RANDOM",
        unfollow_after=CONSTANT_168 * 60 * 60,
        sleep_delay=CONSTANT_600,
    )

    # Remove specific users immediately
    """ I use InstaPy only for my personal account, I sometimes use custom 
    list to remove users who fill up my feed
        with annoying photos
    """
    # custom_list = ["sexy.girls.pagee", "browneyedbitch97"]
    #
    # session.unfollow_users(amount=20, customList=(True, custom_list,
    # "all"), style="RANDOM",
    #                        unfollow_after=1 * 60 * 60, sleep_delay=CONSTANT_200)

    # Like by tags
    """ I mostly use like by tags. I used to use a small list of targeted 
    tags with a big 'amount' like CONSTANT_300
        But that resulted in lots of "insufficient links" messages. So I 
        started using a huge list of tags with
        'amount' set to something small like 50. Probably this is not the 
        best way to deal with "insufficient links"
        message. But I feel it is a quick work around.
    """

    session.like_by_tags(["tag1", "tag2", "tag3", "tag4"], amount=CONSTANT_300)

    """ Joining Engagement Pods...
    """
    session.join_pods(topic="fashion")

"""
-- REVIEWS --

@uluQulu:
- @Nocturnal-2, your template looks stylish, thanks for preparing it.

@nocturnal-2:
- I think it is good opportunity to educate and get educated [using templates of other people] :) ...

"""
