from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import pyarrow
from pyarrow.orc import ORCFile

from .local_metadata_source import LocalMetadataSource


@dataclass
class ORCSource(LocalMetadataSource):
    """Instance for a local ORC file."""

    def read(self) -> ORCFile:
        """
        Read the ORC file.
        :return:
        """
        return ORCFile(self.local_path)

    def schema(self) -> pyarrow.Schema:
        """
        Get the ORC File.
        :return: the orc schema
        """
        return self.read().schema

    def get_column_names(self) -> List[str]:
        """
        Get the column names from the schema.
        :return: the list of the column names
        """
        return self.schema().names

    @property
    def type(self) -> str:
        """
        The type of the source.
        :return: the name of the source.
        """
        return "LocalORC"
