from dataclasses import dataclass
from enum import Enum
from typing import Any, List, Optional

from loguru import logger

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
                if not self.connection or not self.connection.open:
                    self.create_connection()
                cursor = self.connection.cursor()
                cursor.execute(f"SHOW FULL COLUMNS FROM {database_name}.{table_name}")
                rows = cursor.fetchall()
                columns = list()
                for row in rows:
                    column_name = row["Field"]
                    columns.append(column_name)
                    if include_comment:
                        column_comment = row["Comment"]
                        if column_comment:
                            columns.append(column_comment)
                return columns
            except Exception as exception:
                logger.exception(
                    f"Error in getting columns name from MySQL {database_name}.{table_name}"
                )
                raise exception
            finally:
                cursor.close()

        def get_table_names_list(self, database_name: str) -> List[str]:
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
                table_list = list()
                for row in rows:
                    table_name = list(row.values())[0]
                    table_list.append(table_name)
                return table_list
            except Exception as exception:
                logger.exception(
                    f"Error in getting table names from the database {database_name} in MySQL"
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
            return "MySQL"
