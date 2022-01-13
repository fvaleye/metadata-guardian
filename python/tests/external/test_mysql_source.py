from unittest.mock import patch

from metadata_guardian.source import MySQLAuthenticator, MySQLSource


@patch("pymysql.connect")
def test_mysql_source_get_column_names(mock_connection):
    database_name = "test"
    table_name = "test_table"
    user = "user"
    host = "localhost"
    password = "password"
    mock_connection.cursor.return_value = mock_connection
    mock_connection.fetchall.return_value = [
        {
            "Field": "words",
            "Type": "varchar(45)",
            "Collation": "utf8_general_ci",
            "Null": "YES",
            "Key": "",
            "Default": None,
            "Extra": "",
            "Privileges": "select,insert,update,references",
            "Comment": "Use column to contain words",
        },
        {
            "Field": "name",
            "Type": "varchar(45)",
            "Collation": "utf8_general_ci",
            "Null": "YES",
            "Key": "",
            "Default": None,
            "Extra": "",
            "Privileges": "select,insert,update,references",
            "Comment": "",
        },
    ]
    mock_connection.execute.call_args == f"SHOW FULL COLUMNS FROM {database_name}.{table_name}"
    expected = ["words", "Use column to contain words", "name"]

    source = MySQLSource(
        host=host,
        user=user,
        password=password,
    )
    source.connection = mock_connection

    column_names = source.get_column_names(
        database_name=database_name, table_name=table_name, include_comment=True
    )

    assert column_names == expected
    assert source.authenticator == MySQLAuthenticator.USER_PWD


@patch("pymysql.connect")
def test_mysql_source_get_table_names_list(mock_connection):
    database_name = "test"
    user = "user"
    host = "localhost"
    password = "password"
    mock_connection.cursor.return_value = mock_connection
    mock_connection.fetchall.return_value = [
        {"Tables_in_test": "t1"},
        {"Tables_in_test": "t2"},
    ]
    mock_connection.execute.call_args == f"SHOW TABLES IN {database_name}"
    expected = ["t1", "t2"]

    source = MySQLSource(
        host=host,
        user=user,
        password=password,
    )
    source.connection = mock_connection

    table_names = source.get_table_names_list(database_name=database_name)

    assert table_names == expected
    assert source.authenticator == MySQLAuthenticator.USER_PWD
