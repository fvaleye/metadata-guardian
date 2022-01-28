from dataclasses import dataclass

from .local_metadata_source import LocalMetadataSource


@dataclass
class ParquetSource(LocalMetadataSource):
    """Instance for a local Parquet file."""

    @classmethod
    @property
    def type(cls) -> str:
        """
        The type of the source.

        :return: the name of the source.
        """
        return "Parquet"
