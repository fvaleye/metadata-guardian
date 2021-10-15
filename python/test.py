from metadata_guardian.data_rules import DataRules
from metadata_guardian.report import MetadataGuardianReport
from metadata_guardian.source.external.aws_source import AthenaSource, GlueSource
from metadata_guardian.source.external.deltatable_source import DeltaTableSource
from metadata_guardian.source.external.snowflake_source import SnowflakeSource
from metadata_guardian.source.local.avro_source import AvroSource
from metadata_guardian.source.local.local_file_source import LocalFileSource

if __name__ == "__main__":
    report = MetadataGuardianReport()
    data_rules = DataRules(
        "/Users/florian.valeye/Documents/workspace/MetadataGuardian/rust/src/rules/inclusion_rules.yaml"
    )
    results = data_rules.validate_word("master")
    local_file_source = LocalFileSource(
        local_path="/Users/florian.valeye/Documents/workspace/MetadataGuardian/python/metadata_guardian/test.txt"
    )
    results = data_rules.validate_from_metadata(source=local_file_source)
    report.to_console(results)

    avro_source = AvroSource(
        local_path="/Users/florian.valeye/Documents/workspace/MetadataGuardian/python/tests/resources/users.avro"
    )
    field_names = avro_source.get_column_names()
    data_rules = DataRules(
        "/Users/florian.valeye/Documents/workspace/MetadataGuardian/rust/src/rules/inclusion_rules.yaml"
    )
    field_names.append("master")
    results = data_rules.validate_words(words=field_names)
    report.to_console(results)

    sf_source = SnowflakeSource(
        warehouse="ENGINEERING_WH",
        sf_account="backmarket.eu-west-1",
        sf_user="fvaleye",
        sf_password="C7,z4]G8m{ur+75;$yXy",
        database_name="BADOOM_DELTAS",
        schema_name="PUBLIC",
        table_name="BO_MERCHANT_ORDER_SILVER",
    )
    field_names = sf_source.get_column_names()
    results = data_rules.validate_words(words=field_names)
    report.to_console(results)

    athena = AthenaSource(
        s3_staging_dir="fva-dev-silver",
        database_name="test_database",
        table_name="test_table_alo_bronze_athena",
    )
    athena.get_column_names()

    glue = GlueSource(
        database_name="test_database", table_name="test_table_alo_bronze_athena"
    )
    glue.get_column_names()

    delta_table = DeltaTableSource(
        "s3://data-platform-europe-dev-silver/finance/payout_silver"
    )
    delta_table.get_column_names()
