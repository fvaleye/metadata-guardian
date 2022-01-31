from typing import Any, Dict, Iterator, List, Optional, Union

from loguru import logger
from pydantic import Field

from ..metadata_source import ColumnMetadata
from .external_metadata_source import (
    ExternalMetadataSource,
    ExternalMetadataSourceException,
)

try:
    from google.cloud import bigquery

    GCP_INSTALLED = True
except ImportError:
    logger.debug("GCP optional dependency is not installed.")
    GCP_INSTALLED = False

if GCP_INSTALLED:

    class BigQuerySource(ExternalMetadataSource):
        """Instance of a BigQuery source."""

        service_account_json_path: str
        project: Optional[str] = None
        location: Optional[str] = None
        extra_connection_args: Dict[str, Any] = Field(default_factory=dict)

        def create_connection(self) -> None:
            """
            Get the Big Query connection.

            :return:
            """
            try:
                self._connection = bigquery.Client.from_service_account_json(
                    self.service_account_json_path,
                    project=self.project,
                    location=self.location,
                    **self.extra_connection_args,
                )
            except Exception as exception:
                logger.exception("Error when connecting to BigQuery")
                raise exception

        def close_connection(self) -> None:
            """
            Close the BigQuery connection.

            :return:
            """
            self._connection.close()

        def get_column_names(
            self, database_name: str, table_name: str, include_comment: bool = False
        ) -> Iterator[ColumnMetadata]:
            """
            Get column names from the table of the dataset.

            :param database_name: in that case the dataset
            :param table_name: the table name
            :param include_comment: include the comment
            :return: the list of the column names
            """

            try:
                if not self._connection:
                    self.create_connection()

                table_reference = self._connection.dataset(
                    database_name, project=self.project
                ).table(table_name)
                table = self._connection.get_table(table_reference)
                for column in table.schema:
                    column_name = column.name
                    column_comment = None
                    if include_comment and column.description:
                        column_comment = column.description
                    yield ColumnMetadata(
                        column_name=column_name, column_comment=column_comment
                    )
            except Exception as exception:
                logger.exception(
                    f"Error in getting columns name from BigQuery {database_name}.{table_name}"
                )
                raise ExternalMetadataSourceException(exception)

        def get_table_names_list(self, database_name: str) -> Iterator[str]:
            """
            Get the table names list from the GCP dataset.

            :param database_name: in that case the dataset
            :return: the list of the table names list
            """

            try:
                if not self._connection:
                    self.create_connection()
                query_job = self._connection.query(
                    f"SELECT table_name FROM `{database_name}.INFORMATION_SCHEMA.TABLES`"
                )
                results = query_job.result()
                for row in results:
                    yield row.table_name
            except Exception as exception:
                logger.exception(
                    f"Error in getting the table names list name from BigQuery {database_name}"
                )
                raise exception

        @classmethod
        def type(cls) -> str:
            """
            The type of the source.

            :return: the name bof the source.
            """
            return "GCP BigQuery"
