from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from fastparquet import ParquetFile

from .local_metadata_source import LocalMetadataSource


@dataclass
class ParquetSource(LocalMetadataSource):
    """Instance for a local Parquet file."""

    def read(self) -> Dict[str, Any]:
        """Read the Parquet file."""
        return ParquetFile(self.local_path)

    def schema(self):
        """
        Get the schema File.
        :return: the parquet schema
        """
        return self.read().schema

    def get_column_names(self) -> List[str]:
        """
        Get the column names from the schema.
        :return: the list of the column names
        """
        return self.read().columns

    @property
    def type(self) -> str:
        """
        The type of the source.
        :return: the name o of the source.
        """
        return "LocalParquetSchema"
