from metadata_guardian.source import ColumnMetadata


def test_column_metadata():
    column_name = "column_name"
    column_comment = "column_comment"
    expected = [column_name, column_comment]

    column_metadata = ColumnMetadata(
        column_name=column_name, column_comment=column_comment
    )

    assert list(column_metadata.as_list()) == expected
