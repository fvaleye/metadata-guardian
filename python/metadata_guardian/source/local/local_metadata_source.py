from abc import abstractmethod
from dataclasses import dataclass

from ..metadata_source import MetadataSource


@dataclass
class LocalMetadataSource(MetadataSource):
    """LocalMetadata Source contract."""

    local_path: str

    @abstractmethod
    def read(self):
        """
        Read the source local file.
        :return: the file content
        """
        pass

    @abstractmethod
    def schema(self):
        """
        Get the source schema
        :return: the schema
        """
        pass
