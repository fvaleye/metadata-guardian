from unittest.mock import Mock, patch

from deltalake import DataType, Field, Schema
from deltalake.schema import PrimitiveType

from metadata_guardian.source import ColumnMetadata, DeltaTableSource


@patch("deltalake.DeltaTable")
def test_deltatable_source_get_column_names(mock_connection):
    uri = "s3://test_table"
    schema = Schema(
        fields=[
            Field(
                "timestamp",
                PrimitiveType("timestamp"),
                False,
                {"comment": "comment1"},
            ),
            Field(
                "address_id",
                PrimitiveType("integer"),
                False,
                {"comment": "comment2"},
            ),
        ],
    )
    mock_connection.schema.return_value = schema
    expected = [
        ColumnMetadata(
            column_name="timestamp", column_comment="{'comment': 'comment1'}"
        ),
        ColumnMetadata(
            column_name="address_id", column_comment="{'comment': 'comment2'}"
        ),
    ]

    delta_table = DeltaTableSource(uri=uri)
    delta_table._connection = mock_connection
    column_names = delta_table.get_column_names(include_comment=True)

    assert list(column_names) == expected
