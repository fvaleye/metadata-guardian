from dataclasses import dataclass
from enum import Enum
from typing import Any, List, Optional

import snowflake.connector
from loguru import logger

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
    database_name: str
    schema_name: str
    table_name: str
    okta_account_name: Optional[str] = None
    oauth_token: Optional[str] = None
    oauth_host: Optional[str] = None
    authenticator: SnowflakeAuthenticator = SnowflakeAuthenticator.USER_PWD

    def get_connection(self) -> Any:
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
        self,
    ) -> List[str]:
        """
        Get column names from the Delta table.
        :return: the list of the column names
        """
        connection = self.get_connection()
        cursor = connection.cursor()

        try:
            cursor = connection.cursor()
            cursor.execute(
                f'SHOW COLUMNS IN "{self.database_name}"."{self.schema_name}"."{self.table_name}"'
            )
            rows = cursor.fetchall()
            column_names = list()
            for row in rows:
                column_names.append(row[2])
            return column_names
        except Exception as exception:
            logger.exception(
                f"Error in getting columns name from Snowflake {self.schema_name}.{self.database_name}.{self.table_name}"
            )
            raise exception
        finally:
            cursor.close()
            connection.close()

    @property
    def type(self) -> str:
        """
        The type of the source.
        :return: the name o of the source.
        """
        return "Snowflake"
