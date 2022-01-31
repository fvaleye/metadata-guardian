from typing import Any, Dict, Iterator, List, Optional, Text, Union

from loguru import logger

from .local_metadata_source import ColumnMetadata, LocalMetadataSource

try:
    from avro.schema import parse

    AVRO_INSTALLED = True

except ImportError:
    logger.warning("AVRO optional dependency is not installed.")
    AVRO_INSTALLED = False

if AVRO_INSTALLED:

    class AvroSchemaSource(LocalMetadataSource):
        """Instance for a local Avro Schema file."""

        def read(self) -> Union[Text, bytes]:
            """Read the AVRO Schema file."""
            with open(self.local_path, "r") as file:
                return file.read()

        def get_column_names(self) -> Iterator[ColumnMetadata]:
            """
            Get column names from the AVRO Schema file.

            :return: the list of the column names
            """
            schema = parse(self.read())
            for field in schema.fields:
                yield ColumnMetadata(column_name=field.name)

        @property
        def namespace(self) -> str:
            """
            Namespace of the AVRO schema.

            :return: the namespace
            """
            schema = parse(self.read())
            return schema.namespace

        @classmethod
        def type(cls) -> str:
            """
            The type of the source.

            :return: the name o of the source.
            """
            return "AvroSchema"
