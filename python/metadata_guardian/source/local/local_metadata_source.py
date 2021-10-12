from dataclasses import dataclass
from typing import Any, Dict, List

import pyarrow
from pyarrow import Schema
from pyarrow.dataset import Dataset
from pyarrow.fs import FileSystem, LocalFileSystem

from ..metadata_source import MetadataSource


@dataclass
class LocalMetadataSource(MetadataSource):
    """LocalMetadata Source contract."""

    local_path: str
    fs: FileSystem = LocalFileSystem()

    def read(self) -> Dataset:
        """
        Read the source local file.
        :return: the file content
        """
        return pyarrow.dataset.dataset(self.local_path, filesystem=self.fs)

    def schema(self) -> Schema:
        """
        Get the source schema
        :return: the file schema
        """
        return self.read().schema

    def get_column_names(self) -> List[str]:
        """
        Get the column names from the schema.
        :return: the list of the column names
        """
        return [column for column in self.schema().names]

    def type(self) -> str:
        return "LocalFile"
