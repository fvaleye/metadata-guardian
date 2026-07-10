import pytest

from metadata_guardian.source import ColumnMetadata, MySQLSource


def test_column_metadata():
    column_name = "column_name"
    column_comment = "column_comment"
    expected = [column_name, column_comment]

    column_metadata = ColumnMetadata(
        column_name=column_name, column_comment=column_comment
    )

    assert list(column_metadata.as_list()) == expected


def test_external_source_propagates_context_errors(mocker):
    source = MySQLSource(user="user", password="password", host="host")
    mocker.patch.object(MySQLSource, "create_connection")
    mocker.patch.object(MySQLSource, "close_connection")

    with pytest.raises(RuntimeError, match="scan failed"):
        with source:
            raise RuntimeError("scan failed")
