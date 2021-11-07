from unittest.mock import patch

from deltalake import Field, Schema

from metadata_guardian.source.external.deltatable_source import DeltaTableSource


@patch(
    "metadata_guardian.source.external.deltatable_source.DeltaTableSource.get_connection"
)
def test_deltatable_source_get_column_names(mock_connection):
    uri = "s3://test_table"
    schema = Schema(
        fields=[
            Field(
                name="timestamp",
                type="string",
                nullable=False,
                metadata={"comment": "comment1"},
            ),
            Field(
                name="address_id",
                type="int",
                nullable=False,
                metadata={"comment": "comment2"},
            ),
        ],
        json_value={},
    )
    mock_connection.return_value = mock_connection
    mock_connection.schema.return_value = schema
    expected = [
        "timestamp",
        "{'comment': 'comment1'}",
        "address_id",
        "{'comment': 'comment2'}",
    ]

    column_names = DeltaTableSource(uri=uri).get_column_names(include_comment=True)

    assert column_names == expected


@patch("deltalake.DeltaTable.from_data_catalog")
def test_deltatable_source_get_column_names_from_database_and_table(mock_connection):
    uri = "s3://test_table"
    database_name = "database_name"
    table_name = "table_name"
    schema = Schema(
        fields=[
            Field(
                name="timestamp",
                type="string",
                nullable=False,
                metadata={"comment": "comment1"},
            ),
            Field(
                name="address_id",
                type="int",
                nullable=False,
                metadata={"comment": "comment2"},
            ),
        ],
        json_value={},
    )
    mock_connection.return_value = mock_connection
    mock_connection.schema.return_value = schema
    expected = [
        "timestamp",
        "{'comment': 'comment1'}",
        "address_id",
        "{'comment': 'comment2'}",
    ]

    column_names = DeltaTableSource(uri=uri).get_column_names(
        database_name=database_name, table_name=table_name, include_comment=True
    )

    assert column_names == expected
