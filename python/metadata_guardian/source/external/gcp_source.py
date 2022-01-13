from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Union

from loguru import logger

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

    @dataclass
    class BigQuerySource(ExternalMetadataSource):
        """Instance of a BigQuery source."""

        service_account_json_path: str
        project: Optional[str] = None
        location: Optional[str] = None

        def create_connection(self) -> None:
            """
            Get the Big Query connection.
            :return:
            """
            try:
                self.connection = bigquery.Client.from_service_account_json(
                    self.service_account_json_path,
                    project=self.project,
                    location=self.location,
                )
            except Exception as exception:
                logger.exception("Error when connecting to BigQuery")
                raise exception

        def close_connection(self) -> None:
            """
            Close the BigQuery connection
            :return:
            """
            self.connection.close()

        def get_column_names(
            self, database_name: str, table_name: str, include_comment: bool = False
        ) -> List[str]:
            """
            Get column names from the table of the dataset.
            :param database_name: in that case the dataset
            :param table_name: the table name
            :param include_comment: include the comment
            :return: the list of the column names
            """

            try:
                if not self.connection:
                    self.create_connection()

                table_reference = self.connection.dataset(
                    database_name, project=self.project
                ).table(table_name)
                table = self.connection.get_table(table_reference)
                columns = list()
                for column in table.schema:
                    columns.append(column.name.lower())
                    if include_comment and column.description:
                        columns.append(column.description.lower())
                return columns
            except Exception as exception:
                logger.exception(
                    f"Error in getting columns name from BigQuery {database_name}.{table_name}"
                )
                raise ExternalMetadataSourceException(exception)

        def get_table_names_list(self, database_name: str) -> List[str]:
            """
            Get the table names list from the GCP dataset.
            :param database_name: in that case the dataset
            :return: the list of the table names list
            """

            try:
                if not self.connection:
                    self.create_connection()
                query_job = self.connection.query(
                    f"SELECT table_name FROM `{database_name}.INFORMATION_SCHEMA.TABLES`"
                )
                results = query_job.result()
                table_names_list = list()
                for row in results:
                    table_names_list.append(row.table_name.lower())
                return table_names_list
            except Exception as exception:
                logger.exception(
                    f"Error in getting the table names list name from BigQuery {database_name}"
                )
                raise exception

        @property
        def type(self) -> str:
            """
            The type of the source.
            :return: the name bof the source.
            """
            return "GCP BigQuery"
