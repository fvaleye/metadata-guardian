from dataclasses import dataclass
from typing import Any, List, Optional

from deltalake import DeltaTable
from loguru import logger

from .external_metadata_source import ExternalMetadataSource


@dataclass
class DeltaTableSource(ExternalMetadataSource):
    uri: str

    def get_connection(self) -> Any:
        """
        Get the DeltaTable instance.
        :return: the DeltaTable instance
        """
        return DeltaTable(self.uri)

    def get_column_names(
        self,
        database_name: Optional[str] = None,
        table_name: Optional[str] = None,
        include_comment: bool = False,
    ) -> List[str]:
        """
        Get column names from the table.
        :param database_name: the database name
        :param table_name: the table name
        :param include_comment: include the comment
        :return: the list of the column names
        """
        try:
            delta_table = self.get_connection()
            schema = delta_table.schema()
            columns = list()
            for field in schema.fields:
                columns.append(field.name.lower())
                if include_comment and field.metadata:
                    columns.append(str(field.metadata).lower())
            return columns
        except Exception as error:
            logger.exception(
                f"Error in getting columns name from the DeltaTable: {self.uri}"
            )
            raise error

    @property
    def type(self) -> str:
        """
        The type of the source.
        :return: the name o of the source.
        """
        return "DeltaTable"
