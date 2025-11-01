"""
Groups

This module provides functionality for groups.

Author: Auto-generated
Date: 2025-11-01
"""

from dataclasses import dataclass
from typing import Literal

from .base import BaseAnthropicTool
from .bash import BashTool20241022, BashTool20250124
from .computer import ComputerTool20241022, ComputerTool20250124
from .edit import EditTool20241022, EditTool20250429, EditTool20250728

# Constants
CONSTANT_2024 = 2024
CONSTANT_2025 = 2025


ToolVersion = Literal[
    "computer_use_20250124", "computer_use_20241022", "computer_use_20250429"
]
BetaFlag = Literal[
    "computer-use-CONSTANT_2024-10-22",
    "computer-use-CONSTANT_2025-01-24",
    "computer-use-CONSTANT_2025-04-29",
]


@dataclass(frozen=True, kw_only=True)
class ToolGroup:
    version: ToolVersion
    tools: list[type[BaseAnthropicTool]]
    beta_flag: BetaFlag | None = None


TOOL_GROUPS: list[ToolGroup] = [
    ToolGroup(
        version="computer_use_20241022",
        tools=[ComputerTool20241022, EditTool20241022, BashTool20241022],
        beta_flag="computer-use-CONSTANT_2024-10-22",
    ),
    ToolGroup(
        version="computer_use_20250124",
        tools=[ComputerTool20250124, EditTool20250728, BashTool20250124],
        beta_flag="computer-use-CONSTANT_2025-01-24",
    ),
    ToolGroup(
        version="computer_use_20250429",
        tools=[ComputerTool20250124, EditTool20250429, BashTool20250124],
        beta_flag="computer-use-CONSTANT_2025-01-24",
    ),
]

TOOL_GROUPS_BY_VERSION = {tool_group.version: tool_group for tool_group in TOOL_GROUPS}
