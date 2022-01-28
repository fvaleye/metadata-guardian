from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, Iterator, List, Optional

from loguru import logger

from ..metadata_source import ColumnMetadata
from .external_metadata_source import (
    ExternalMetadataSource,
    ExternalMetadataSourceException,
)

try:
    import pymysql

    MYSQL_INSTALLED = True
except ImportError:
    logger.debug("MySQL optional dependency is not installed.")
    MYSQL_INSTALLED = False

if MYSQL_INSTALLED:

    class MySQLAuthenticator(Enum):
        """Authentication method for MySQL source."""

        USER_PWD = 1

    @dataclass
    class MySQLSource(ExternalMetadataSource):
        """Instance of a MySQL source."""

        user: str
        password: str
        host: str
        database: Optional[str] = None
        authenticator: MySQLAuthenticator = MySQLAuthenticator.USER_PWD
        extra_connection_args: Dict[str, Any] = field(default_factory=dict)

        def create_connection(self) -> None:
            """
            Create a MySQL connection based on the MySQLAuthenticator.

            :return:
            """
            if self.authenticator == MySQLAuthenticator.USER_PWD:
                self.connection = pymysql.connect(
                    host=self.host,
                    user=self.user,
                    password=self.password,
                    database=self.database,
                    cursorclass=pymysql.cursors.DictCursor,
                    **self.extra_connection_args,
                )

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
                if not self.connection or not self.connection.open:
                    self.create_connection()
                cursor = self.connection.cursor()
                cursor.execute(f"SHOW FULL COLUMNS FROM {database_name}.{table_name}")
                rows = cursor.fetchall()
                for row in rows:
                    column_name = row["Field"]
                    column_comment = None
                    if include_comment and row["Comment"]:
                        column_comment = row["Comment"]
                    yield ColumnMetadata(
                        column_name=column_name, column_comment=column_comment
                    )
            except Exception as exception:
                logger.exception(
                    f"Error in getting columns name from MySQL {database_name}.{table_name}"
                )
                raise exception
            finally:
                cursor.close()

        def get_table_names_list(self, database_name: str) -> Iterator[str]:
            """
            Get the table names list from the MySQL database.

            :param database_name: the database name
            :return: the list of the table names of the database
            """
            try:
                if not self.connection or not self.connection.open:
                    self.create_connection()
                cursor = self.connection.cursor()
                cursor.execute(f"SHOW TABLES IN {database_name}")
                rows = cursor.fetchall()
                for row in rows:
                    table_name = list(row.values())[0]
                    yield table_name
            except Exception as exception:
                logger.exception(
                    f"Error in getting table names from the database {database_name} in MySQL"
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
            return "MySQL"
