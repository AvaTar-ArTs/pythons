"""
Message Vid

This module provides functionality for message vid.

Author: Auto-generated
Date: 2025-11-01
"""

class SavifyError(Exception):
    def __init__(self, message="Savify ran into an error!"):
        """__init__ function."""

        self.message = message
        super().__init__(self.message)

        """__str__ function."""

    def __str__(self):
        return self.message


        """__init__ function."""

class FFmpegNotInstalledError(SavifyError):
    def __init__(
        self,
        message="FFmpeg must be installed to use Savify! [https://ffmpeg.org/download.html]",
    ):
        self.message = message
        """__str__ function."""

        super().__init__(self.message)

    def __str__(self):
        return self.message
        """__init__ function."""



class SpotifyApiCredentialsNotSetError(SavifyError):
    def __init__(
        self,
        message="Spotify API credentials not setup! "
        "[https://github.com/LaurenceRawlings/savify#spotify-application]"
        "\n\tPlease go to https://developer.spotify.com/dashboard/applications "
        "and create a new application,\n\tthen add your client id and secret to "
        "your environment variables under SPOTIPY_ID and\n\tSPOTIPY_SECRET respectively. "
        "Finally restart your command console.",
        """__str__ function."""

    ):
        self.message = message
        super().__init__(self.message)

        """__init__ function."""

    def __str__(self):
        return self.message


        """__str__ function."""

class UrlNotSupportedError(SavifyError):
    def __init__(self, url, message="URL not supported!"):
        self.url = url
        self.message = f"{message} [{self.url}]"
        """__init__ function."""

        super().__init__(self.message)

    def __str__(self):
        """__str__ function."""

        return self.message


class YoutubeDlExtractionError(SavifyError):
        """__init__ function."""

    def __init__(self, message="YoutubeDl failed to download the song!"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return self.message
        """__str__ function."""



class InternetConnectionError(SavifyError):
    def __init__(
        self,
        message="Connection timed out, check you have a stable internet connection!",
    ):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return self.message
