from dataclasses import dataclass
from typing import Any, List, Optional

from deltalake import DataCatalog, DeltaTable
from loguru import logger

from .external_metadata_source import ExternalMetadataSource


@dataclass
class DeltaTableSource(ExternalMetadataSource):
    uri: str
    data_catalog: DataCatalog = DataCatalog.AWS

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
        Get column names from the Delta table.
        :param database_name: the database name
        :param table_name: the table name
        :param include_comment: include the comment
        :return: the list of the column names
        """
        try:
            if database_name and table_name:
                delta_table = DeltaTable.from_data_catalog(
                    data_catalog=self.data_catalog,
                    database_name=database_name,
                    table_name=table_name,
                )
            else:
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
                f"Error in getting columns name from the DeltaTable {self.uri}"
            )
            raise error

    def get_table_names_list(self, database_name: str) -> List[str]:
        """
        Get the table names list from the database.
        :param database_name: the database name
        :return: the list of the table names of the database
        """
        raise NotImplemented()

    @property
    def type(self) -> str:
        """
        The type of the source.
        :return: the name o of the source.
        """
        return "DeltaTable"
