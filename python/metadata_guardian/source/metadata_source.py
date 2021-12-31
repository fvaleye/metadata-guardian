from abc import ABC, abstractmethod


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
