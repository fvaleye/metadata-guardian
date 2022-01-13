import pytest

from metadata_guardian.data_rules import AvailableCategory, DataRules
from metadata_guardian.scanner import ColumnScanner, ContentFilesScanner
from metadata_guardian.source import AvroSchemaSource


@pytest.mark.parametrize("local_file", ["example_rules.yaml"], indirect=["local_file"])
def test_get_data_rules_from_path_should_work(local_file):
    data_rules = DataRules.from_path(path=local_file)
    assert data_rules._data_rules is not None


@pytest.mark.parametrize(
    "local_file", ["users_avro_schema.json"], indirect=["local_file"]
)
def test_get_data_rules_from_category_pii_with_violation(local_file):
    data_rules = DataRules.from_available_category(category=AvailableCategory.PII)
    source = AvroSchemaSource(local_file)

    md_results = ColumnScanner(data_rules=data_rules).scan_local(source=source)

    assert len(md_results.report_results[0].results) == 1
    assert (
        "tests/resources/users_avro_schema.json" in md_results.report_results[0].source
    )
    result = md_results.report_results[0].results[0]
    assert result.content == "name"
    assert result.category == "PII"
    assert len(result.data_rules) == 1
    data_rule = result.data_rules[0]
    assert data_rule.rule_name == "person"
    assert (
        data_rule.documentation
        == "The person is a personal identifiable information.\n"
    )


@pytest.mark.parametrize(
    "local_file", ["users_avro_schema.json"], indirect=["local_file"]
)
def test_get_data_rules_from_category_inclusion_no_violation(local_file):
    data_rules = DataRules.from_available_category(category=AvailableCategory.INCLUSION)
    source = AvroSchemaSource(local_file)

    md_results = ColumnScanner(data_rules=data_rules).scan_local(source=source)

    assert "resources/users_avro_schema.json" in md_results.report_results[0].source
    assert len(md_results.report_results[0].results) == 0


@pytest.mark.parametrize(
    "local_file", ["inclusion_violation.txt"], indirect=["local_file"]
)
def test_get_data_rules_from_category_inclusion_violation_content(local_file):
    data_rules = DataRules.from_available_category(category=AvailableCategory.INCLUSION)

    md_results = ContentFilesScanner(data_rules=data_rules).scan_local_file(local_file)

    assert len(md_results.report_results[0].results) == 1
    assert "resources/inclusion_violation.txt" in md_results.report_results[0].source
    result = md_results.report_results[0].results[0]
    assert (
        result.content
        == "feudal age in that they were not bound to the soil but to the master."
    )
    assert result.category == "INCLUSION"
    assert len(result.data_rules) == 1
    data_rule = result.data_rules[0]
    assert data_rule.rule_name == "master"
    assert (
        data_rule.documentation
        == '"Master–slave" is an offensive and exclusionary metaphor that cannot be detached from American\n'
        "history. Prefer describing a hierarchical relationship between nodes more precisely. Prefer using\n"
        "leader/follower, primary/replica or primary/standby.\n"
    )
