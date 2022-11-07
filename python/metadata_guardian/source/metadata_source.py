from abc import ABC, abstractmethod
from typing import Iterator, List, Optional

from pydantic import BaseModel


class Metadata(BaseModel, ABC):
    """Metadata contract."""

    @abstractmethod
    def as_list(self) -> Iterator[str]:
        """
        Return as a raw list of strings.

        :return: a list of string
        """
        pass


class ColumnMetadata(Metadata):
    """Column Metadata instance."""

    column_name: str
    column_comment: Optional[str] = None

    def as_list(self) -> Iterator[str]:
        """
        Return as a raw list of strings.

        :return: a list of string
        """
        yield self.column_name.lower()
        if self.column_comment:
            yield self.column_comment.lower()


class MetadataSource(BaseModel, ABC):
    """Metadata Source contract."""

    @classmethod
    @abstractmethod
    def type(cls) -> str:
        """
        The type of the source.

        :return: the name of the source.
        """
        pass
