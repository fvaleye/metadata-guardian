import asyncio
import os
from unittest.mock import patch

from metadata_guardian.data_rules import AvailableCategory, DataRules
from metadata_guardian.report import MetadataGuardianReport, ReportResults
from metadata_guardian.scanner import ColumnScanner, ContentFilesScanner
from metadata_guardian.source.external.snowflake_source import SnowflakeSource


@patch("snowflake.connector")
def test_column_scanner_table_name(mock_connection):
    database_name = "test_database"
    schema_name = "PUBLIC"
    table_name = "TEST_TABLE"
    sf_account = "sf_account"
    sf_user = "sf_user"
    sf_password = "sf_password"
    warehouse = "warehouse"
    mocked_cursor_one = mock_connection.connect().cursor.return_value
    mocked_cursor_one.description = [["name"], ["phone"]]
    mocked_cursor_one.fetchall.return_value = [
        (database_name, table_name, "column1", "", "", "", "", "", "comment1"),
        (database_name, table_name, "column2", "", "", "", "", "", "comment2"),
    ]
    mocked_cursor_one.execute.call_args == f'SHOW COLUMNS IN "{database_name}"."{schema_name}"."{table_name}"'
    expected = MetadataGuardianReport(
        report_results=[
            ReportResults(source=f"{database_name}.{table_name}", results=[])
        ]
    )

    source = SnowflakeSource(
        sf_account=sf_account,
        sf_user=sf_user,
        sf_password=sf_password,
        warehouse=warehouse,
        schema_name=schema_name,
    )
    data_rules = DataRules.from_available_category(category=AvailableCategory.INCLUSION)

    report = ColumnScanner(data_rules=data_rules).scan_external(
        database_name=database_name, table_name=table_name, source=source
    )

    assert report == expected


@patch("snowflake.connector")
def test_column_scanner_database_name(mock_connection):
    database_name = "test_database"
    schema_name = "PUBLIC"
    table_name = "TEST_TABLE"
    table_name_2 = "TEST_TABLE_2"
    sf_account = "sf_account"
    sf_user = "sf_user"
    sf_password = "sf_password"
    warehouse = "warehouse"
    mocked_cursor_one = mock_connection.connect().cursor.return_value
    mocked_cursor_one.description = [["name"], ["phone"]]
    mocked_cursor_one.fetchall.return_value = [
        (database_name, table_name, "column1", "", "", "", "", "", "comment1"),
        (database_name, table_name_2, "column2", "", "", "", "", "", "comment2"),
    ]
    mocked_cursor_one.execute.call_args == f'SHOW COLUMNS IN "{database_name}"."{schema_name}"."{table_name}"'
    expected = MetadataGuardianReport(
        report_results=[
            ReportResults(source=f"{database_name}.{table_name}", results=[]),
            ReportResults(source=f"{database_name}.{table_name_2}", results=[]),
        ]
    )

    source = SnowflakeSource(
        sf_account=sf_account,
        sf_user=sf_user,
        sf_password=sf_password,
        warehouse=warehouse,
        schema_name=schema_name,
    )
    data_rules = DataRules.from_available_category(category=AvailableCategory.INCLUSION)

    report = ColumnScanner(data_rules=data_rules).scan_external(
        database_name=database_name, source=source
    )

    assert report == expected


@patch("snowflake.connector")
def test_column_scanner_database_name_async(mock_connection):
    database_name = "test_database"
    schema_name = "PUBLIC"
    table_name = "TEST_TABLE"
    table_name_2 = "TEST_TABLE_2"
    sf_account = "sf_account"
    sf_user = "sf_user"
    sf_password = "sf_password"
    warehouse = "warehouse"
    mocked_cursor_one = mock_connection.connect().cursor.return_value
    mocked_cursor_one.description = [["name"], ["phone"]]
    mocked_cursor_one.fetchall.return_value = [
        (database_name, table_name, "column1", "", "", "", "", "", "comment1"),
        (database_name, table_name_2, "column2", "", "", "", "", "", "comment2"),
    ]
    mocked_cursor_one.execute.call_args == f'SHOW COLUMNS IN "{database_name}"."{schema_name}"."{table_name}"'
    expected = MetadataGuardianReport(
        report_results=[
            ReportResults(source=f"{database_name}.{table_name}", results=[]),
            ReportResults(source=f"{database_name}.{table_name_2}", results=[]),
        ]
    )

    source = SnowflakeSource(
        sf_account=sf_account,
        sf_user=sf_user,
        sf_password=sf_password,
        warehouse=warehouse,
        schema_name=schema_name,
    )
    data_rules = DataRules.from_available_category(category=AvailableCategory.INCLUSION)

    report = asyncio.run(
        ColumnScanner(data_rules=data_rules).scan_external_async(
            database_name=database_name, source=source
        )
    )

    assert report == expected


def test_local_directory_scan():
    directory_path = os.path.join(os.path.dirname(__file__), "resources")
    file_names_extension = "txt"

    data_rules = DataRules.from_available_category(category=AvailableCategory.INCLUSION)

    report = ContentFilesScanner(data_rules=data_rules).scan_directory(
        directory_path=directory_path, file_names_extension=file_names_extension
    )

    assert "resources/inclusion_violation.txt" in str(report)
