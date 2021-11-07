from dataclasses import dataclass
from enum import Enum
from typing import Any, List, Optional

import snowflake.connector
from loguru import logger
from snowflake.connector import SnowflakeConnection

from .external_metadata_source import ExternalMetadataSource


class SnowflakeAuthenticator(Enum):
    """Authentication method for Snowflake source."""

    USER_PWD = 1
    OKTA = 2
    TOKEN = 3


@dataclass
class SnowflakeSource(ExternalMetadataSource):
    """Instance of a Snowflake source."""

    sf_account: str
    sf_user: str
    sf_password: str
    warehouse: str
    schema_name: str
    okta_account_name: Optional[str] = None
    oauth_token: Optional[str] = None
    oauth_host: Optional[str] = None
    authenticator: SnowflakeAuthenticator = SnowflakeAuthenticator.USER_PWD

    def get_connection(self) -> SnowflakeConnection:
        if self.authenticator == SnowflakeAuthenticator.USER_PWD:
            return snowflake.connector.connect(
                account=self.sf_account,
                user=self.sf_user,
                password=self.sf_password,
                warehouse=self.warehouse,
            )
        elif self.authenticator == SnowflakeAuthenticator.OKTA:
            return snowflake.connector.connect(
                account=self.sf_account,
                user=self.sf_user,
                password=self.sf_password,
                warehouse=self.warehouse,
                authenticator=f"https://{self.okta_account_name}.okta.com/",
            )
        elif self.authenticator == SnowflakeAuthenticator.TOKEN:
            return snowflake.connector.connect(
                account=self.sf_account,
                user=self.sf_user,
                password=self.sf_password,
                warehouse=self.warehouse,
                authenticator="oauth",
                token=self.oauth_token,
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
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            cursor.execute(
                f'SHOW COLUMNS IN "{database_name}"."{self.schema_name}"."{table_name}"'
            )
            rows = cursor.fetchall()
            columns = list()
            for row in rows:
                column_name = row[2]
                columns.append(column_name.lower())
                if include_comment:
                    column_comment = row[8]
                    columns.append(column_comment.lower())
            return columns
        except Exception as exception:
            logger.exception(
                f"Error in getting columns name from Snowflake {self.schema_name}.{database_name}.{table_name}"
            )
            raise exception
        finally:
            cursor.close()
            connection.close()

    def get_table_names_list(self, database_name: str) -> List[str]:
        """
        Get the table names list from the Snowflake database.
        :param database_name: the database name
        :return: the list of the table names of the database
        """
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            cursor.execute(f'SHOW TABLES IN DATABASE "{database_name.upper()}"')
            rows = cursor.fetchall()
            table_list = list()
            for row in rows:
                table_name = row[1]
                table_list.append(table_name.upper())
            return table_list
        except Exception as exception:
            logger.exception(
                f"Error in getting table names from the database {database_name} in Snowflake {database_name}"
            )
            raise exception
        finally:
            cursor.close()
            connection.close()

    @property
    def type(self) -> str:
        """
        The type of the source.
        :return: the name of the source.
        """
        return "Snowflake"
