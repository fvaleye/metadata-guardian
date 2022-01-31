import json
from typing import Any, Dict, Iterator, List, Optional

from loguru import logger

from .local_metadata_source import ColumnMetadata, LocalMetadataSource

try:
    from avro.datafile import DataFileReader, DataFileWriter
    from avro.io import DatumReader, DatumWriter

    AVRO_INSTALLED = True

except ImportError:
    logger.warning("AVRO optional dependency is not installed.")
    AVRO_INSTALLED = False

if AVRO_INSTALLED:

    class AvroSource(LocalMetadataSource):
        """Instance for a local Avro file."""

        def read(self) -> DataFileReader:
            """Read the AVRO file."""
            with open(self.local_path, "rb") as file:
                return DataFileReader(file, DatumReader())

        def get_field_attribute(
            self, attribute_name: str
        ) -> List[Optional[ColumnMetadata]]:
            """
            Get the specific attribute from the AVRO Schema.

            :param attribute_name: the attribute name to get
            :return: the list of attributes in the fields
            """
            reader = self.read()
            schema = json.loads(reader.meta["avro.schema"])
            return [
                ColumnMetadata(column_name=str(field[attribute_name]))
                if attribute_name in field
                else None
                for field in schema["fields"]
            ]

        def get_column_names(self) -> Iterator[ColumnMetadata]:
            """
            Get column names from the AVRO file.

            :return: the list of the column names
            """
            reader = self.read()
            schema = json.loads(reader.meta["avro.schema"])
            for field in schema["fields"]:
                yield ColumnMetadata(column_name=field["name"])

        @property
        def namespace(self) -> str:
            """
            Namespace of the AVRO schema.

            :return: the namespace
            """
            reader = self.read()
            schema = json.loads(reader.meta["avro.schema"])
            return schema["namespace"]

        @classmethod
        def type(cls) -> str:
            """
            The type of the source.

            :return: the name o of the source.
            """
            return "Avro"
