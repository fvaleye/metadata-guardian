from types import SimpleNamespace
from unittest.mock import Mock, patch

from google.cloud import bigquery

from metadata_guardian.source import BigQuerySource


@patch("google.cloud.bigquery.Client.from_service_account_json")
def test_big_query_source_get_column_names(mock_connection):
    service_account_json_path = ""
    dataset_name = "test_dataset"
    table_name = "test_table"
    results = SimpleNamespace(
        schema=[
            bigquery.SchemaField(
                "timestamp", "STRING", mode="REQUIRED", description="description1"
            ),
            bigquery.SchemaField(
                "address_id", "STRING", mode="REQUIRED", description="description2"
            ),
        ]
    )
    mock_connection.return_value = mock_connection
    mock_connection.get_table.return_value = results
    expected = ["timestamp", "description1", "address_id", "description2"]

    column_names = BigQuerySource(
        service_account_json_path=service_account_json_path
    ).get_column_names(
        database_name=dataset_name, table_name=table_name, include_comment=True
    )

    assert column_names == expected


@patch("google.cloud.bigquery.Client.from_service_account_json")
def test_big_query_source_get_table_names_list(mock_connection):
    service_account_json_path = ""
    dataset_name = "test_dataset"
    results = [
        SimpleNamespace(table_name="test_table"),
        SimpleNamespace(table_name="test_table2"),
    ]
    mock_connection.return_value = mock_connection
    response = Mock()
    response.result.return_value = results
    mock_connection.query.return_value = response
    expected = ["test_table", "test_table2"]

    table_names_list = BigQuerySource(
        service_account_json_path=service_account_json_path
    ).get_table_names_list(
        database_name=dataset_name,
    )

    assert table_names_list == expected
