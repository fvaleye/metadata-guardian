import json
from dataclasses import dataclass
from enum import Enum
from typing import Any, List, Optional

from loguru import logger

from .external_metadata_source import (
    ExternalMetadataSource,
    ExternalMetadataSourceException,
)

try:
    from confluent_kafka.schema_registry import SchemaRegistryClient

    KAFKA_SCHEMA_REGISTRY_INSTALLED = True
except ImportError:
    logger.debug("Kafka Schema Registry optional dependency is not installed.")
    KAFKA_SCHEMA_REGISTRY_INSTALLED = False

if KAFKA_SCHEMA_REGISTRY_INSTALLED:

    class KafkaSchemaRegistryAuthentication(Enum):
        """Authentication method for Kafka Schema Registry source."""

        USER_PWD = 1

    @dataclass
    class KafkaSchemaRegistrySource(ExternalMetadataSource):
        """Instance of a Kafka Schema Registry source."""

        url: str
        ssl_certificate_location: Optional[str] = None
        ssl_key_location: Optional[str] = None
        connection: Optional[SchemaRegistryClient] = None
        authenticator: Optional[
            KafkaSchemaRegistryAuthentication
        ] = KafkaSchemaRegistryAuthentication.USER_PWD
        comment_field_name: str = "doc"

        def create_connection(self) -> None:
            """
            Create the connection of the Kafka Schema Registry.

            :return:
            """
            if self.authenticator == KafkaSchemaRegistryAuthentication.USER_PWD:
                self.connection = SchemaRegistryClient(
                    {
                        "url": self.url,
                    }
                )
            else:
                raise NotImplementedError()

        def close_connection(self) -> None:
            """
            Close the Kafka Schema Registry connection.

            :return:
            """
            self.connection.__exit__()

        def get_column_names(
            self, database_name: str, table_name: str, include_comment: bool = False
        ) -> List[str]:
            """
            Get the column names from the subject.

            :param database_name: not relevant
            :param table_name: the subject name
            :param include_comment: include the comment
            :return: the list of the column names
            """
            try:
                if not self.connection:
                    self.create_connection()
                registered_schema = self.connection.get_latest_version(table_name)
                columns = list()
                for field in json.loads(registered_schema.schema.schema_str)["fields"]:
                    columns.append(field["name"])
                    if include_comment and self.comment_field_name in field:
                        columns.append(field[self.comment_field_name])
                return columns
            except Exception as exception:
                logger.exception(
                    f"Error in getting columns name from the Kafka Schema Registry {table_name}"
                )
                raise exception

        def get_table_names_list(self, database_name: str) -> List[str]:
            """
            Get all the subjects from the Schema Registry.

            :param database_name: not relevant in that case
            :return: the list of the table names of the database
            """
            try:
                if not self.connection:
                    self.create_connection()
                all_subjects = self.connection.get_subjects()
                return all_subjects
            except Exception as exception:
                logger.exception(
                    f"Error all the subjects from the subject in the Kafka Schema Registry"
                )
                raise ExternalMetadataSourceException(exception)

        @property
        def type(self) -> str:
            """
            The type of the source.

            :return: the name of the source.
            """
            return "Kafka Schema Registry"
