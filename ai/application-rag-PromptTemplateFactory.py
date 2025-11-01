"""
Application Rag Prompttemplatefactory

This module provides functionality for application rag prompttemplatefactory.

Author: Auto-generated
Date: 2025-11-01
"""

from abc import ABC, abstractmethod
from typing import Any

from langchain.prompts import PromptTemplate
from llm_engineering.domain.queries import Query
from pydantic import BaseModel


class PromptTemplateFactory(ABC, BaseModel):
    @abstractmethod
    def create_template(self) -> PromptTemplate:
        """create_template function."""

        pass


class RAGStep(ABC):
        """__init__ function."""

    def __init__(self, mock: bool = False) -> None:
        self._mock = mock

        """generate function."""

    @abstractmethod
    def generate(self, query: Query, *args, **kwargs) -> Any:
        pass
