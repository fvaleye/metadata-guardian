import pytest

from metadata_guardian.source.local.avro_source import AvroSource


@pytest.mark.parametrize("local_file", ["users.avro"], indirect=["local_file"])
def test_avro_source(local_file):
    source = AvroSource(local_path=local_file)
    expected = ["name", "favorite_number", "favorite_color"]

    column_names = source.get_column_names()

    assert expected == column_names


@pytest.mark.parametrize("local_file", ["users.avro"], indirect=["local_file"])
def test_avro_source_namespace(local_file):
    source = AvroSource(local_path=local_file)
    expected = "example.avro"

    assert expected == source.namespace


@pytest.mark.parametrize("local_file", ["users.avro"], indirect=["local_file"])
def test_avro_source_attribute_type(local_file):
    source = AvroSource(local_path=local_file)
    expected = ["string", ["int", "null"], ["string", "null"]]

    field_attribute_type = source.get_field_attribute(attribute_name="type")

    assert expected == field_attribute_type
