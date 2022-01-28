from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Iterator, List, Optional


class Metadata(ABC):
    """Metadata contract."""

    @abstractmethod
    def as_list(self) -> Iterator[str]:
        """
        Return as a raw list of strings.

        :return: a list of string
        """
        pass


@dataclass
class ColumnMetadata(Metadata):
    """Column Metadata instance."""

    column_name: str
    column_comment: Optional[str] = None

    def as_list(self) -> Iterator[str]:
        """
        Return as a raw list of strings.

        :return: a list of string
        """
        yield self.column_name
        if self.column_comment:
            yield self.column_comment


class MetadataSource(ABC):
    """Metadata Source contract."""

    @classmethod
    def type(cls) -> str:
        """
        The type of the source.

        :return: the name of the source.
        """
        pass
