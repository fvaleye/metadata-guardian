from typing import Any, Dict, Iterator, List, Optional

from pyarrow.orc import ORCFile

from .local_metadata_source import ColumnMetadata, LocalMetadataSource


class ORCSource(LocalMetadataSource):
    """Instance for a local ORC file."""

    def read(self) -> ORCFile:
        """
        Read the ORC file.

        :return:
        """
        return ORCFile(self.local_path)

    def get_column_names(self) -> Iterator[ColumnMetadata]:
        """
        Get the column names from the schema.

        :return: the list of the column names
        """
        for column_name in self.read().schema.names:
            yield ColumnMetadata(column_name=column_name)

    @classmethod
    def type(cls) -> str:
        """
        The type of the source.

        :return: the name of the source.
        """
        return "ORC"
