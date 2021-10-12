from abc import abstractmethod
from dataclasses import dataclass
from typing import Any

from ..metadata_source import MetadataSource


@dataclass
class ExternalMetadataSource(MetadataSource):
    """ExternalMetadataSource Source."""

    @abstractmethod
    def get_connection(self) -> Any:
        """
        Get the connection of the source.
        :return: the source connection
        """
        pass
