from dataclasses import dataclass

from .local_metadata_source import LocalMetadataSource


@dataclass
class ParquetSource(LocalMetadataSource):
    """Instance for a local Parquet file."""

    @property
    def type(self) -> str:
        """
        The type of the source.
        :return: the name of the source.
        """
        return "LocalParquet"
