from abc import abstractmethod
from typing import Any, Dict, Iterator, List, Optional

from loguru import logger
from pydantic import PrivateAttr

from ...exceptions import MetadataGuardianException
from ..metadata_source import ColumnMetadata, MetadataSource


class ExternalMetadataSource(MetadataSource):
    """ExternalMetadataSource Source."""

    _connection: Any = PrivateAttr()

    def __init__(self, **data: Any) -> None:
        super().__init__(**data)
        self._connection = None

    def __enter__(self) -> "ExternalMetadataSource":
        try:
            self.create_connection()
        except Exception as exception:
            logger.exception(
                "Error raised while opening the Metadata Source connection"
            )
            raise exception
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> "ExternalMetadataSource":  # type: ignore
        try:
            self.close_connection()
        except Exception as exception:
            logger.exception(
                "Error raised while closing the Metadata Source connection"
            )
            raise exception
        return self

    @abstractmethod
    def get_column_names(
        self,
        database_name: str,
        table_name: str,
        include_comment: bool = False,
    ) -> Iterator[ColumnMetadata]:
        """
        Get the column names from the schema.

        :param database_name: the database name
        :param table_name: the table name
        :param include_comment: include the comment
        :return: the list of the column names
        """
        pass

    @abstractmethod
    def get_table_names_list(self, database_name: str) -> Iterator[str]:
        """
        Get the table names list from the database.

        :param database_name: the database name
        :return: the list of the table names of the database
        """
        pass

    @abstractmethod
    def create_connection(self) -> None:
        """
        Create the connection of the source.

        :return:
        """
        pass

    def close_connection(self) -> None:
        """
        Close the connection of the source.

        :return:
        """
        pass


class ExternalMetadataSourceException(MetadataGuardianException):
    """Raised where there is an exception to describe a external metadata source exception."""

    pass
