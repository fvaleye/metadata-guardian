from unittest.mock import patch

from metadata_guardian.source.external.snowflake_source import (
    SnowflakeAuthenticator,
    SnowflakeSource,
)


@patch("snowflake.connector")
def test_snowflake_source_get_column_names(mock_connection):
    database_name = "test_database"
    schema_name = "PUBLIC"
    table_name = "test_table"
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
    expected = ["column1", "comment1", "column2", "comment2"]

    source = SnowflakeSource(
        sf_account=sf_account,
        sf_user=sf_user,
        sf_password=sf_password,
        warehouse=warehouse,
        schema_name=schema_name,
    )

    column_names = source.get_column_names(
        database_name=database_name, table_name=table_name, include_comment=True
    )

    assert column_names == expected
    assert source.authenticator == SnowflakeAuthenticator.USER_PWD
