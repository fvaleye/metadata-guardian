from dataclasses import dataclass
from typing import Any, List, Optional

import boto3
import botocore
from loguru import logger
from mypy_boto3_athena.client import AthenaClient
from mypy_boto3_glue.client import GlueClient

from .external_metadata_source import ExternalMetadataSource


@dataclass
class AthenaSource(ExternalMetadataSource):
    """Athena Source instance."""

    s3_staging_dir: str
    catalog_name: str = "AWSDataCatalog"
    region_name: Optional[str] = None
    aws_access_key_id: Optional[str] = None
    aws_secret_access_key: Optional[str] = None

    def get_connection(self) -> AthenaClient:
        """
        Get Athena connection.
        :return: a new Athena connection.
        """
        return boto3.client(
            "athena",
            region_name=self.region_name,
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
        )

    def get_column_names(
        self, database_name: str, table_name: str, include_comment: bool = False
    ) -> List[str]:
        """
        Get column names from the table.
        :param database_name: the database name
        :param table_name: the table name
        :param include_comment: include the comment
        :return: the list of the column names
        """
        client = self.get_connection()

        try:
            response = client.get_table_metadata(
                CatalogName=self.catalog_name,
                DatabaseName=database_name,
                TableName=table_name,
            )
            columns = list()
            for row in response["TableMetadata"]["Columns"]:
                columns.append(row["Name"].lower())
                if include_comment:
                    columns.append(row["Comment"].lower())
            return columns
        except botocore.exceptions.ClientError as error:
            logger.exception(
                f"Error in getting columns name from Athena {database_name}.{table_name} for catalog {self.catalog_name}"
            )
            raise error

    @property
    def type(self) -> str:
        """
        The type of the source.
        :return: the name o of the source.
        """
        return "AWSAthena"


@dataclass
class GlueSource(ExternalMetadataSource):
    """Glue Source instance."""

    region_name: Optional[str] = None
    aws_access_key_id: Optional[str] = None
    aws_secret_access_key: Optional[str] = None

    def get_connection(self) -> GlueClient:
        """
        Get the Glue connection
        :return: one Glue client
        """
        return boto3.client(
            "glue",
            region_name=self.region_name,
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
        )

    def get_column_names(
        self, database_name: str, table_name: str, include_comment: bool = False
    ) -> List[str]:
        """
        Get the column names from Glue table.
        :param database_name: the name of the database
        :param table_name: the name of the table
        :param include_comment: include the comments
        :return: the list of the column names
        """
        try:
            client = self.get_connection()

            response = client.get_table(DatabaseName=database_name, Name=table_name)
            columns = list()
            for row in response["Table"]["StorageDescriptor"]["Columns"]:
                columns.append(row["Name"].lower())
                if include_comment:
                    columns.append(row["Comment"].lower())
            return columns
        except botocore.exceptions.ClientError as error:
            logger.exception(
                f"Error in getting columns name from Glue: {database_name}.{table_name}"
            )
            raise error

    @property
    def type(self) -> str:
        """
        The type of the source.
        :return: the name of the source.
        """
        return "AWSGlue"
