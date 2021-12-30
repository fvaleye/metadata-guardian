from unittest.mock import patch

from confluent_kafka.schema_registry import RegisteredSchema, Schema

from metadata_guardian.source import (
    KafkaSchemaRegistryAuthentication,
    KafkaSchemaRegistrySource,
)


@patch("confluent_kafka.schema_registry.SchemaRegistryClient")
def test_kafka_schema_registry_source_get_column_names(mock_connection):
    url = "url"
    subject_name = "subject_name"
    expected = ["key", "value", "doc"]

    source = KafkaSchemaRegistrySource(
        url=url,
    )
    schema_id = "schema_id"
    schema_str = """{
        "fields": [
            {
                "name": "key",
                "type": "string"
            },
            {
                "name": "value",
                "type": "string",
                "doc": "doc"
            }
        ],
        "name": "test_one",
        "namespace": "test.one",
        "type": "record"
    }"""
    schema = RegisteredSchema(
        schema_id=schema_id,
        schema=Schema(schema_str, "AVRO", []),
        subject=subject_name,
        version=1,
    )
    mock_connection.get_latest_version.return_value = schema
    source.connection = mock_connection

    column_names = source.get_column_names(
        database_name=None, table_name=subject_name, include_comment=True
    )

    assert column_names == expected
    assert source.authenticator == KafkaSchemaRegistryAuthentication.USER_PWD


@patch("confluent_kafka.schema_registry.SchemaRegistryClient")
def test_kafka_schema_registry_source_get_table_names_list(mock_connection):
    url = "url"
    expected = ["subject1", "subject2"]

    source = KafkaSchemaRegistrySource(
        url=url,
    )
    subjects = ["subject1", "subject2"]
    mock_connection.get_subjects.return_value = subjects
    source.connection = mock_connection

    subjects_list = source.get_table_names_list(database_name=None)

    assert subjects_list == expected
    assert source.authenticator == KafkaSchemaRegistryAuthentication.USER_PWD
