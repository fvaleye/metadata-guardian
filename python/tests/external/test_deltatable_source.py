from unittest.mock import Mock, patch

from deltalake import Field, Schema

from metadata_guardian.source import DeltaTableSource


@patch("deltalake.DeltaTable")
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
    mock_connection.schema.return_value = schema
    expected = [
        "timestamp",
        "{'comment': 'comment1'}",
        "address_id",
        "{'comment': 'comment2'}",
    ]

    delta_table = DeltaTableSource(uri=uri)
    delta_table.connection = mock_connection
    column_names = delta_table.get_column_names(include_comment=True)

    assert column_names == expected


@patch("deltalake.DeltaTable.from_data_catalog")
def test_deltatable_source_get_column_names_from_database_and_table(mock_connection):
    uri = "s3://test_table"
    database_name = "database_name"
    table_name = "table_name"
    external_data_catalog_disable = False
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

    column_names = DeltaTableSource(
        uri=uri, external_data_catalog_disable=external_data_catalog_disable
    ).get_column_names(
        database_name=database_name, table_name=table_name, include_comment=True
    )

    assert column_names == expected
