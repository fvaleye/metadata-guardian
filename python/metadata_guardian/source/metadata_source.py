from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Optional


class Metadata(ABC):
    """Metadata contract."""

    @abstractmethod
    def as_list(self) -> List[str]:
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

    def as_list(self) -> List[str]:
        """
        Return as a raw list of strings.

        :return: a list of string
        """
        temp_list = list()
        temp_list.append(self.column_name)
        if self.column_comment:
            temp_list.append(self.column_comment)
        return temp_list


class MetadataSource(ABC):
    """Metadata Source contract."""

    @property
    @abstractmethod
    def type(self) -> str:
        """
        The type of the source.

        :return: the name o of the source.
        """
        pass
