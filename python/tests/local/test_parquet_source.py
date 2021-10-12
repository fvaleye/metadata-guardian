import pytest

from metadata_guardian.source.local.parquet_source import ParquetSource


@pytest.mark.parametrize(
    "local_file", ["subscriptions.parquet"], indirect=["local_file"]
)
def test_parquet_source_column_names(local_file):
    source = ParquetSource(local_path=local_file)
    expected = ["timestamp", "id", "email"]

    column_names = source.get_column_names()

    assert expected == column_names
