from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Union

from google.cloud import bigquery
from loguru import logger

from .external_metadata_source import ExternalMetadataSource


@dataclass
class BigQuerySource(ExternalMetadataSource):
    """Instance of a BigQuery source."""

    service_account_json_path: str
    project: Optional[str] = None
    location: Optional[str] = None

    def get_connection(self) -> Any:
        """
        Get the Big Query connection.
        :return: a BigQuery Client
        """
        try:
            return bigquery.Client.from_service_account_json(
                self.service_account_json_path,
                project=self.project,
                location=self.location,
            )
        except Exception as exception:
            logger.exception("Error when connecting to BigQuery")
            raise exception

    def get_column_names(
        self, database_name: str, table_name: str, include_comment: bool = False
    ) -> List[str]:
        """
        Get column names from the table.
        :param database_name: in that case the dataset
        :param table_name: the table name
        :param include_comment: include the comment
        :return: the list of the column names
        """

        try:
            client = self.get_connection()
            query_job = client.query(
                f'SELECT column_name, description FROM `{database_name}.INFORMATION_SCHEMA.COLUMN_FIELD_PATHS` WHERE table_name = "{table_name}"'
            )
            results = query_job.result()
            columns = list()
            for row in results:
                columns.append(row.column_name.lower())
                if include_comment:
                    columns.append(row.description.lower())
            return columns
        except Exception as exception:
            logger.exception(
                f"Error in getting columns name from BigQuery {database_name}.{table_name}"
            )
            raise exception

    def get_table_names_list(self, database_name: str) -> List[str]:
        """
        Get the table names list from the GCP dataset.
        :param database_name: in that case the dataset
        :return: the list of the table names list
        """

        try:
            client = self.get_connection()
            query_job = client.query(
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
        return "BigQuery"
