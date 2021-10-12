from abc import ABC, abstractmethod
from typing import List


class MetadataSource(ABC):
    """Metadata Source contract."""

    @abstractmethod
    def get_column_names(self) -> List[str]:
        """
        Get the column names from the schema.
        :return: the list of the column names
        """
        pass

    @property
    @abstractmethod
    def type(self) -> str:
        """
        The type of the source.
        :return: the name o of the source.
        """
        pass
