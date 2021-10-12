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
            Field(name="timestamp", type="string", nullable=False, metadata={}),
            Field(name="address_id", type="int", nullable=False, metadata={}),
        ],
        json_value={},
    )
    mock_connection.return_value = mock_connection
    mock_connection.schema.return_value = schema
    expected = ["timestamp", "address_id"]

    column_names = DeltaTableSource(uri=uri).get_column_names()

    assert column_names == expected
