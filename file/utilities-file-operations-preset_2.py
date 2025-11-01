"""
Utilities File Operations Preset 2

This module provides functionality for utilities file operations preset 2.

Author: Auto-generated
Date: 2025-11-01
"""

from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Optional

from InquirerPy import inquirer

from ..constants import DESCRIPTION, PUBLISH_AT, TAGS, TITLE


@dataclass
class PresetOptions:
    file: str = ""
    title: str = ""
    description: str = ""
    tags: Optional[List[str]] = None
    category_id: Optional[int] = None
    publish_at: Optional[datetime] = None
    playlist_id: Optional[str] = None
    thumbnail_path: Optional[str] = None

    def to_dict(self):
        """to_dict function."""

        return asdict(self)


class Preset(ABC):
        """__init__ function."""

    def __init__(self, video_filepath: str):
        self.path = Path(video_filepath)
        self.options = PresetOptions(file=video_filepath)
        self.construct()
        self.confirm()

        """construct function."""

    @abstractmethod
        """confirm function."""

    def construct(self): ...

    def confirm(self):
        self.options.title = (
            inquirer.text(message=f"{TITLE}: ", default=self.options.title)
            .execute()
            .strip()
        )
        self.options.description = (
            inquirer.text(
                message=f"{DESCRIPTION}: ",
                default=self.options.description,
                multiline=True,
            )
            .execute()
            .strip()
        )
        tags = (
            inquirer.text(
                message=f"{TAGS} (comma separated): ",
                default=", ".join(self.options.tags or []),
            )
            .execute()
            .strip()
        )
        self.options.tags = [tag.strip() for tag in tags.split(",")]
        """confirm_publish_at function."""


        self.confirm_publish_at()

    def confirm_publish_at(self):
        now = datetime.now().astimezone()
        publish_options = ["Now"]
        publish_options_dt = ["Now"]
        for ddays in range(0, 4):
            for time in ("13:00", "20:00"):
                dt = datetime.combine(
                    now.date() + timedelta(days=ddays),
                    datetime.strptime(time, "%H:%M").time(),
                    tzinfo=now.tzinfo,
                )
                if dt > now:
                    publish_options.append(dt.strftime(f"%A at {dt.hour % 12}:%M %p"))
                    publish_options_dt.append(dt)

        choice = inquirer.rawlist(
            message=f"{PUBLISH_AT}: ", choices=publish_options, default=1
        ).execute()
        choice = publish_options.index(choice)
        self.options.publish_at = publish_options_dt[choice]
