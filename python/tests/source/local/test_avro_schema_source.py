import pytest

from metadata_guardian.source import AvroSchemaSource, ColumnMetadata


@pytest.mark.parametrize(
    "local_file", ["users_avro_schema.json"], indirect=["local_file"]
)
def test_avro_schema_source(local_file):
    source = AvroSchemaSource(local_path=local_file)
    expected = [
        ColumnMetadata(column_name="name"),
        ColumnMetadata(column_name="favorite_number"),
        ColumnMetadata(column_name="favorite_color"),
    ]

    column_names = source.get_column_names()

    assert list(column_names) == expected


@pytest.mark.parametrize(
    "local_file", ["users_avro_schema.json"], indirect=["local_file"]
)
def test_avro_schema_source_namespace(local_file):
    source = AvroSchemaSource(local_path=local_file)
    expected = "example.avro"

    assert expected == source.namespace
