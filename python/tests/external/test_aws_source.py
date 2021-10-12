from unittest.mock import patch

from metadata_guardian.source.external.aws_source import AthenaSource, GlueSource


@patch("boto3.client")
def test_athena_source_get_column_names(mock_connection):
    database_name = "test_database"
    table_name = "test_table"
    s3_staging_dir = "s3_test"
    response = {
        "TableMetadata": {
            "Name": table_name,
            "TableType": "EXTERNAL_TABLE",
            "Columns": [
                {"Name": "timestamp", "Type": "string", "Comment": "comment1"},
                {"Name": "address_id", "Type": "int", "Comment": "comment2"},
            ],
            "PartitionKeys": [],
            "Parameters": {},
        }
    }
    mock_connection.return_value = mock_connection
    mock_connection.get_table_metadata.return_value = response
    expected = ["timestamp", "comment1", "address_id", "comment2"]

    column_names = AthenaSource(s3_staging_dir=s3_staging_dir,).get_column_names(
        database_name=database_name, table_name=table_name, include_comment=True
    )

    assert column_names == expected


@patch("boto3.client")
def test_glue_source_get_column_names(mock_connection):
    database_name = "test_database"
    table_name = "test_table"
    response = {
        "Table": {
            "StorageDescriptor": {
                "Columns": [
                    {"Name": "timestamp", "Type": "string", "Comment": "comment1"},
                    {"Name": "address_id", "Type": "int", "Comment": "comment2"},
                ]
            }
        }
    }
    mock_connection.return_value = mock_connection
    mock_connection.get_table.return_value = response
    expected = ["timestamp", "comment1", "address_id", "comment2"]

    column_names = GlueSource().get_column_names(
        database_name=database_name, table_name=table_name, include_comment=True
    )

    assert column_names == expected