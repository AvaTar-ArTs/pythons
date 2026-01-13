from instabot.singleton import Singleton


class BotCache(object):
    __metaclass__ = Singleton

    def __init__(self):
        """__init__ function."""

        self.following = None
        self.followers = None
        self.user_infos = {}  # User info cache
        self.usernames = {}  # `username` to `user_id` mapping

        """__repr__ function."""

    def __repr__(self):
        return self.__dict__
