from dataclasses import dataclass
from enum import Enum
from typing import Any, List, Optional

from loguru import logger

from .external_metadata_source import (
    ExternalMetadataSource,
    ExternalMetadataSourceException,
)

try:
    import snowflake.connector
    from snowflake.connector import SnowflakeConnection
    from snowflake.connector.converter_null import SnowflakeNoConverterToPython

    SNOWFLAKE_INSTALLED = True
except ImportError:
    logger.debug("Snowflake optional dependency is not installed.")
    SNOWFLAKE_INSTALLED = False

if SNOWFLAKE_INSTALLED:

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

        def create_connection(self) -> None:
            """
            Create a Snowflake connection based on the SnowflakeAuthenticator.

            :return:
            """
            if self.authenticator == SnowflakeAuthenticator.USER_PWD:
                self.connection = snowflake.connector.connect(
                    account=self.sf_account,
                    user=self.sf_user,
                    password=self.sf_password,
                    warehouse=self.warehouse,
                    converter_class=SnowflakeNoConverterToPython,
                )
            elif self.authenticator == SnowflakeAuthenticator.OKTA:
                self.connection = snowflake.connector.connect(
                    account=self.sf_account,
                    user=self.sf_user,
                    password=self.sf_password,
                    warehouse=self.warehouse,
                    authenticator=f"https://{self.okta_account_name}.okta.com/",
                    converter_class=SnowflakeNoConverterToPython,
                )
            elif self.authenticator == SnowflakeAuthenticator.TOKEN:
                self.connection = snowflake.connector.connect(
                    account=self.sf_account,
                    user=self.sf_user,
                    password=self.sf_password,
                    warehouse=self.warehouse,
                    authenticator="oauth",
                    token=self.oauth_token,
                    converter_class=SnowflakeNoConverterToPython,
                )

        def close_connection(self) -> None:
            """
            Close the Snowflake connection.
            :return:
            """
            self.connection.close()

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
                if not self.connection or self.connection.is_closed():
                    self.create_connection()
                cursor = self.connection.cursor()
                cursor.execute(
                    f'SHOW COLUMNS IN "{database_name}"."{self.schema_name}"."{table_name}"'
                )
                rows = cursor.fetchall()
                columns = list()
                for row in rows:
                    column_name = row[2]
                    columns.append(column_name)
                    if include_comment:
                        column_comment = row[8]
                        columns.append(column_comment)
                return columns
            except Exception as exception:
                logger.exception(
                    f"Error in getting columns name from Snowflake {database_name}.{self.schema_name}.{table_name}"
                )
                raise exception
            finally:
                cursor.close()

        def get_table_names_list(self, database_name: str) -> List[str]:
            """
            Get the table names list from the Snowflake database.

            :param database_name: the database name
            :return: the list of the table names of the database
            """
            try:
                if not self.connection or self.connection.is_closed():
                    self.create_connection()
                cursor = self.connection.cursor()
                cursor.execute(f'SHOW TABLES IN DATABASE "{database_name}"')
                rows = cursor.fetchall()
                table_list = list()
                for row in rows:
                    table_name = row[1]
                    table_list.append(table_name.upper())
                return table_list
            except Exception as exception:
                logger.exception(
                    f"Error in getting table names from the database {database_name} in Snowflake"
                )
                raise ExternalMetadataSourceException(exception)
            finally:
                cursor.close()

        @property
        def type(self) -> str:
            """
            The type of the source.

            :return: the name of the source.
            """
            return "Snowflake"
