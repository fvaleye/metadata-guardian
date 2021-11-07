from abc import abstractmethod
from typing import Any, List

from ..metadata_source import MetadataSource


class ExternalMetadataSource(MetadataSource):
    """ExternalMetadataSource Source."""

    @abstractmethod
    def get_column_names(
        self, database_name: str, table_name: str, include_comment: bool = False
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
    def get_connection(self) -> Any:
        """
        Get the connection of the source.
        :return: the source connection
        """
        pass
