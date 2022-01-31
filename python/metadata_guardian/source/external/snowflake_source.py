from enum import Enum
from typing import Any, Dict, Iterator, List, Optional

from loguru import logger
from pydantic import Field

from ..metadata_source import ColumnMetadata
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
        extra_connection_args: Dict[str, Any] = Field(default_factory=dict)

        def create_connection(self) -> None:
            """
            Create a Snowflake connection based on the SnowflakeAuthenticator.

            :return:
            """
            if self.authenticator == SnowflakeAuthenticator.USER_PWD:
                self._connection = snowflake.connector.connect(
                    account=self.sf_account,
                    user=self.sf_user,
                    password=self.sf_password,
                    warehouse=self.warehouse,
                    converter_class=SnowflakeNoConverterToPython,
                    **self.extra_connection_args,
                )
            elif self.authenticator == SnowflakeAuthenticator.OKTA:
                self._connection = snowflake.connector.connect(
                    account=self.sf_account,
                    user=self.sf_user,
                    password=self.sf_password,
                    warehouse=self.warehouse,
                    authenticator=f"https://{self.okta_account_name}.okta.com/",
                    converter_class=SnowflakeNoConverterToPython,
                    **self.extra_connection_args,
                )
            elif self.authenticator == SnowflakeAuthenticator.TOKEN:
                self._connection = snowflake.connector.connect(
                    account=self.sf_account,
                    user=self.sf_user,
                    password=self.sf_password,
                    warehouse=self.warehouse,
                    authenticator="oauth",
                    token=self.oauth_token,
                    converter_class=SnowflakeNoConverterToPython,
                    **self.extra_connection_args,
                )

        def close_connection(self) -> None:
            """
            Close the Snowflake connection.
            :return:
            """
            self._connection.close()

        def get_column_names(
            self, database_name: str, table_name: str, include_comment: bool = False
        ) -> Iterator[ColumnMetadata]:
            """
            Get column names from the table.

            :param database_name: the database name
            :param table_name: the table name
            :param include_comment: include the comment
            :return: the list of the column names
            """
            try:
                if not self._connection or self._connection.is_closed():
                    self.create_connection()
                cursor = self._connection.cursor()
                cursor.execute(
                    f'SHOW COLUMNS IN "{database_name}"."{self.schema_name}"."{table_name}"'
                )
                rows = cursor.fetchall()
                for row in rows:
                    column_name = row[2]
                    column_comment = None
                    if include_comment:
                        column_comment = row[8]
                    yield ColumnMetadata(
                        column_name=column_name, column_comment=column_comment
                    )
            except Exception as exception:
                logger.exception(
                    f"Error in getting columns name from Snowflake {database_name}.{self.schema_name}.{table_name}"
                )
                raise exception
            finally:
                cursor.close()

        def get_table_names_list(self, database_name: str) -> Iterator[str]:
            """
            Get the table names list from the Snowflake database.

            :param database_name: the database name
            :return: the list of the table names of the database
            """
            try:
                if not self._connection or self._connection.is_closed():
                    self.create_connection()
                cursor = self._connection.cursor()
                cursor.execute(f'SHOW TABLES IN DATABASE "{database_name}"')
                rows = cursor.fetchall()
                for row in rows:
                    table_name = row[1]
                    yield table_name.upper()
            except Exception as exception:
                logger.exception(
                    f"Error in getting table names from the database {database_name} in Snowflake"
                )
                raise ExternalMetadataSourceException(exception)
            finally:
                cursor.close()

        @classmethod
        def type(cls) -> str:
            """
            The type of the source.

            :return: the name of the source.
            """
            return "Snowflake"
