from typing import Any, Dict, Iterator, List, Optional

from loguru import logger
from pydantic import Field

from ..metadata_source import ColumnMetadata
from .external_metadata_source import (
    ExternalMetadataSource,
    ExternalMetadataSourceException,
)

try:
    from deltalake import DeltaTable

    DELTA_LAKE_INSTALLED = True
except ImportError:
    logger.debug("Delta Lake optional dependency is not installed.")
    DELTA_LAKE_INSTALLED = False

if DELTA_LAKE_INSTALLED:

    class DeltaTableSource(ExternalMetadataSource):
        uri: str
        extra_connection_args: Dict[str, Any] = Field(default_factory=dict)

        def create_connection(self) -> None:
            """
            Create the DeltaTable instance.

            :return:
            """
            self._connection = DeltaTable(self.uri, **self.extra_connection_args)

        def close_connection(self) -> None:
            pass

        def get_column_names(
            self,
            database_name: Optional[str] = None,
            table_name: Optional[str] = None,
            include_comment: bool = False,
        ) -> Iterator[ColumnMetadata]:
            """
            Get column names from the Delta table.

            :param database_name: the database name
            :param table_name: the table name
            :param include_comment: include the comment
            :return: the list of the column names
            """
            try:
                if not self._connection:
                    self.create_connection()
                schema = self._connection.schema()
                for field in schema.fields:
                    column_comment = None
                    if include_comment and field.metadata:
                        column_comment = str(field.metadata)
                    yield ColumnMetadata(
                        column_name=field.name, column_comment=column_comment
                    )
            except Exception as exception:
                logger.exception(
                    f"Error in getting columns name from the DeltaTable {self.uri}"
                )
                raise ExternalMetadataSourceException(exception)

        def get_table_names_list(self, database_name: str) -> Iterator[str]:
            """
            Not relevant, just return the current Delta Table URI.

            :param database_name: the database name
            :return: the list of the table names of the database
            """
            yield self.uri

        @classmethod
        def type(cls) -> str:
            """
            The type of the source.

            :return: the name of the source.
            """
            return "Delta Table"
