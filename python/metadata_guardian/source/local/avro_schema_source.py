import json
from dataclasses import dataclass
from typing import Any, Dict, Iterator, List, Optional, Text, Union

from .local_metadata_source import ColumnMetadata, LocalMetadataSource


@dataclass
class AvroSchemaSource(LocalMetadataSource):
    """Instance for a local Avro Schema file."""

    def read(self) -> Union[Text, bytes]:
        """Read the AVRO Schema file."""
        with open(self.local_path, "r") as file:
            return file.read()

    def schema(self) -> Dict[str, Any]:
        """
        Get the AVRO schema.

        :return: the schema
        """
        content = self.read()
        return json.loads(content)

    def get_field_attribute(
        self, attribute_name: str
    ) -> Optional[List[ColumnMetadata]]:
        """
        Get the specific attribute from the AVRO Schema file.

        :param attribute_name: the attribute name to get
        :return: the list of attributes in the fields
        """
        return [
            ColumnMetadata(column_name=str(field[attribute_name]))
            if attribute_name in field
            else None
            for field in self.schema()["fields"]
        ]

    def get_column_names(self) -> Iterator[ColumnMetadata]:
        """
        Get column names from the AVRO Schema file.

        :return: the list of the column names
        """
        for field in self.schema()["fields"]:
            yield ColumnMetadata(column_name=field["name"])

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
        return "AvroSchema"
