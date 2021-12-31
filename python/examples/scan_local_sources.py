import argparse
import os

from metadata_guardian import AvailableCategory, ColumnScanner, DataRules
from metadata_guardian.source import AvroSource, ORCSource, ParquetSource


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


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--data-rules",
        choices=["PII", "INCLUSION"],
        default="PII",
        help="The Data Rules to use",
    )
    parser.add_argument(
        "--local-source",
        choices=["Avro", "Parquet", "Orc"],
        required=True,
        help="The Local Metadata Source to use",
    )
    parser.add_argument(
        "--scanner", choices=["ColumnScanner"], help="The scanner to use"
    )
    parser.add_argument("--path", required=True, help="The path of the file to scan")
    parser.add_argument(
        "--include_comments", default=True, help="Include the comments in the scan"
    )
    args = parser.parse_args()
    data_rules = DataRules.from_available_category(
        category=AvailableCategory[args.data_rules]
    )
    column_scanner = ColumnScanner(data_rules=data_rules)

    if args.local_source == "Avro":
        source = AvroSource(local_path=args.path)
    elif args.local_source == "Parquet":
        source = ParquetSource(local_path=args.path)
    elif args.local_source == "Orc":
        source = ORCSource(local_path=args.path)

    report = column_scanner.scan_local(source)
    report.to_console()
