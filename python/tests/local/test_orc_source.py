import pytest

from metadata_guardian.source.local.orc_source import ORCSource


@pytest.mark.parametrize("local_file", ["example.orc"], indirect=["local_file"])
def test_orc_source(local_file):
    source = ORCSource(local_path=local_file)
    expected = [
        "boolean1",
        "byte1",
        "short1",
        "int1",
        "long1",
        "float1",
        "double1",
        "bytes1",
        "string1",
        "middle",
        "list",
        "map",
    ]

    column_names = source.get_column_names()

    assert expected == column_names
