from abc import abstractmethod
from typing import Any, List, Optional

from ...exceptions import MetadataGuardianException
from ..metadata_source import MetadataSource


class ExternalMetadataSource(MetadataSource):
    """ExternalMetadataSource Source."""

    connection: Optional[Any] = None

    @abstractmethod
    def get_column_names(
        self,
        database_name: str,
        table_name: str,
        include_comment: bool = False,
    ) -> List[str]:
        """
        Get the column names from the schema.
        :param database_name: the database name
        :param table_name: the table name
        :param include_comment: include the comment
        :return: the list of the column names
        """
        pass

    @abstractmethod
    def get_table_names_list(self, database_name: str) -> List[str]:
        """
        Get the table names list from the database.
        :param database_name: the database name
        :return: the list of the table names of the database
        """
        pass

    @abstractmethod
    def get_connection(self) -> None:
        """
        Get the connection of the source.
        :return:
        """
        pass


class ExternalMetadataSourceException(MetadataGuardianException):
    """Raised where there is an exception to describe a external metadata source exception."""

    pass
