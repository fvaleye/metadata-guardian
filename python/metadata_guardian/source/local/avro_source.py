import json
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from avro.datafile import DataFileReader, DataFileWriter
from avro.io import DatumReader, DatumWriter

from .local_metadata_source import LocalMetadataSource


@dataclass
class AvroSource(LocalMetadataSource):
    """Instance for a local Avro file."""

    def read(self) -> DataFileReader:
        """Read the AVRO file."""
        with open(self.local_path, "rb") as file:
            return DataFileReader(file, DatumReader())

    def schema(self) -> Dict[str, Any]:
        """
        Get the AVRO schema.
        :return: the schema
        """
        reader = self.read()
        return json.loads(reader.meta["avro.schema"])

    def get_field_attribute(self, attribute_name: str) -> Optional[List[str]]:
        """
        Get the specific attribute from the AVRO Schema.
        :param attribute_name: the attribute name to get
        :return: the list of attributes in the fields
        """
        return [
            field[attribute_name] if attribute_name in field else None
            for field in self.schema()["fields"]
        ]

    def get_column_names(self) -> List[str]:
        """
        Get column names from the AVRO file.
        :return: the list of the column names
        """
        return [field["name"] for field in self.schema()["fields"]]

    @property
    def namespace(self) -> str:
        """
        Namespace of the AVRO schema.
        :return: the namespace
        """
        return self.schema()["namespace"]

    @property
    def type(self) -> str:
        """
        The type of the source.
        :return: the name o of the source.
        """
        return "LocalAvroSource"
