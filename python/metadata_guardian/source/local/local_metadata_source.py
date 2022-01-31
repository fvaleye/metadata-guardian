from typing import Any, Dict, Iterator, List

import pyarrow
from pyarrow.dataset import Dataset
from pyarrow.fs import FileSystem, LocalFileSystem
from pydantic import Field

from ..metadata_source import ColumnMetadata, MetadataSource


class LocalMetadataSource(MetadataSource):
    """LocalMetadata Source contract."""

    local_path: str
    fs: FileSystem = LocalFileSystem()
    extra_connection_args: Dict[str, Any] = Field(default_factory=dict)

    class Config:
        arbitrary_types_allowed = True

    def read(self) -> Dataset:
        """
        Read the source local file.

        :return: the file content
        """
        return pyarrow.dataset.dataset(
            self.local_path, filesystem=self.fs, **self.extra_connection_args
        )

    def get_column_names(self) -> Iterator[ColumnMetadata]:
        """
        Get the column names from the schema.

        :return: the list of the column names
        """
        for column_name in self.read().schema.names:
            yield ColumnMetadata(column_name=column_name)
