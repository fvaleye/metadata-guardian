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
        :return: a new DeltaTable instance
        """
        return DeltaTable(self.uri)

    def get_column_names(self) -> List[str]:
        """
        Get column names from the Delta table.
        :return: the list of the column names
        """
        delta_table = self.get_connection()

        try:
            schema = delta_table.schema()
            column_names = list()
            for field in schema.fields:
                column_names.append(field.name)
            return column_names
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
