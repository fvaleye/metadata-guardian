import pytest

from metadata_guardian.source import ColumnMetadata
from metadata_guardian.source.local.orc_source import ORCSource


@pytest.mark.parametrize("local_file", ["example.orc"], indirect=["local_file"])
def test_orc_source(local_file):
    source = ORCSource(local_path=local_file)
    expected = [
        ColumnMetadata(column_name="boolean1"),
        ColumnMetadata(column_name="byte1"),
        ColumnMetadata(column_name="short1"),
        ColumnMetadata(column_name="int1"),
        ColumnMetadata(column_name="long1"),
        ColumnMetadata(column_name="float1"),
        ColumnMetadata(column_name="double1"),
        ColumnMetadata(column_name="bytes1"),
        ColumnMetadata(column_name="string1"),
        ColumnMetadata(column_name="middle"),
        ColumnMetadata(column_name="list"),
        ColumnMetadata(column_name="map"),
    ]

    column_names = source.get_column_names()

    assert expected == column_names
