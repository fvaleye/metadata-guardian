import argparse
import os

from metadata_guardian import (
    AvailableCategory,
    ColumnScanner,
    DataRules,
    ExternalMetadataSource,
)
from metadata_guardian.source import (
    AthenaSource,
    BigQuerySource,
    DeltaTableSource,
    GlueSource,
    KafkaSchemaRegistrySource,
    MySQLSource,
    SnowflakeSource,
)


def get_snowflake() -> ExternalMetadataSource:
    return SnowflakeSource(
        sf_account=os.environ["SNOWFLAKE_ACCOUNT"],
        sf_user=os.environ["SNOWFLAKE_USER"],
        sf_password=os.environ["SNOWFLAKE_PASSWORD"],
        warehouse=os.environ["SNOWFLAKE_WAREHOUSE"],
        schema_name=os.environ["SNOWFLAKE_SCHEMA_NAME"],
    )


def get_gcp_bigquery() -> ExternalMetadataSource:
    return BigQuerySource(
        service_account_json_path=os.environ["BIGQUERY_SERVICE_ACCOUNT"],
        project=os.environ["BIGQUERY_PROJECT"],
        location=os.environ["BIGQUERY_LOCATION"],
    )


def get_kafka_schema_registry() -> ExternalMetadataSource:
    return KafkaSchemaRegistrySource(url=os.environ["KAFKA_SCHEMA_REGISTRY_URL"])


def get_delta_table() -> ExternalMetadataSource:
    return DeltaTableSource(uri=os.environ["DELTA_TABLE_URI"])


def get_mysql() -> ExternalMetadataSource:
    return MySQLSource(
        user=os.environ["MYSQL_USER"],
        password=os.environ["MYSQL_PASSWORD"],
        host=os.environ["MYSQL_HOST"],
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--data-rules",
        choices=["PII", "INCLUSION"],
        default="PII",
        help="The Data Rules to use",
    )
    parser.add_argument(
        "--external-source",
        choices=[
            "Snowflake",
            "GCP BigQuery",
            "Kafka Schema Registry",
            "Delta Table",
            "MySQL",
        ],
        required=True,
        help="The External Metadata Source to use",
    )
    parser.add_argument(
        "--scanner", choices=["ColumnScanner"], help="The scanner to use"
    )
    parser.add_argument(
        "--database_name", required=True, help="The database name to scan"
    )
    parser.add_argument(
        "--include_comments", default=True, help="Include the comments in the scan"
    )
    args = parser.parse_args()
    data_rules = DataRules.from_available_category(
        category=AvailableCategory[args.data_rules]
    )
    column_scanner = ColumnScanner(data_rules=data_rules)

    if args.external_source == "Snowflake":
        source = get_snowflake()
    elif args.external_source == "GCP BigQuery":
        source = get_gcp_bigquery()
    elif args.external_source == "Kafka Schema Registry":
        source = get_kafka_schema_registry()
    elif args.external_source == "Delta Table":
        source = get_delta_table()
    elif args.external_source == "MySQL":
        source = get_mysql()

    with source:
        report = column_scanner.scan_external(
            source,
            database_name=args.database_name,
            include_comment=args.include_comments,
        )
        report.to_console()
