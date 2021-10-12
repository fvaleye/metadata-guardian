from dataclasses import dataclass
from typing import Any, List, Optional

import boto3
import botocore
from loguru import logger

from .external_metadata_source import ExternalMetadataSource


@dataclass
class AthenaSource(ExternalMetadataSource):
    """Athena Source instance."""

    s3_staging_dir: str
    database_name: str
    table_name: str
    catalog_name: str = "AWSDataCatalog"
    region_name: Optional[str] = None
    aws_access_key_id: Optional[str] = None
    aws_secret_access_key: Optional[str] = None

    def get_connection(self) -> Any:
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

    def get_column_names(self) -> List[str]:
        """
        Get column names from the table.
        :return: the list of the column names
        """
        client = self.get_connection()

        try:
            response = client.get_table_metadata(
                CatalogName=self.catalog_name,
                DatabaseName=self.database_name,
                TableName=self.table_name,
            )
            column_names = list()
            for row in response["TableMetadata"]["Columns"]:
                column_names.append(row["Name"])
            return column_names
        except botocore.exceptions.ClientError as error:
            logger.exceptionf(
                f"Error in getting columns name from Athena {self.database_name}.{self.table_name} for catalog {self.catalog_name}"
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

    database_name: str
    table_name: str
    region_name: Optional[str] = None
    aws_access_key_id: Optional[str] = None
    aws_secret_access_key: Optional[str] = None

    def get_connection(self):
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

    def get_column_names(self) -> List[str]:
        """
        Get the column names from Glue table.
        :return: the list of the column names
        """
        client = self.get_connection()

        try:
            response = client.get_table(
                DatabaseName=self.database_name, Name=self.table_name
            )
            column_names = list()
            for row in response["Table"]["StorageDescriptor"]["Columns"]:
                column_names.append(row["Name"])
            return column_names
        except botocore.exceptions.ClientError as error:
            logger.exception("Error in getting columns name from Athena")
            raise error

    @property
    def type(self) -> str:
        """
        The type of the source.
        :return: the name o of the source.
        """
        return "AWSGlue"
