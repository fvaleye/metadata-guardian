import pyarrow as pa

from metadata_guardian import (
    DataRule,
    DataRules,
    MetadataGuardianReport,
    MetadataGuardianResults,
    ReportResults,
)


def test_report_append_results_and_generate_csv_should_be_ok(tmpdir):
    csv_file = tmpdir.mkdir("test").join("results.csv")
    category = "category"
    content = "content"
    second_category = "second_category"
    second_content = "second_content"
    results = ReportResults(
        source="source1",
        results=[
            MetadataGuardianResults(
                category=category,
                content=content,
                data_rules=[
                    DataRule(
                        rule_name="rule_name",
                        regex_pattern="pattern",
                        documentation="documentation",
                    )
                ],
            )
        ],
    )
    other_report = MetadataGuardianReport(
        report_results=[
            ReportResults(
                source="source2",
                results=[
                    MetadataGuardianResults(
                        category=second_category,
                        content=second_content,
                        data_rules=[
                            DataRule(
                                rule_name="rule_name_2",
                                regex_pattern="pattern-2",
                                documentation="documentation",
                            )
                        ],
                    )
                ],
            )
        ]
    )

    report = MetadataGuardianReport(report_results=[results])
    report.append(other_report)
    report.to_csv(csv_file)
    csv_table = pa.csv.read_csv(csv_file)

    assert csv_table.column("category")[0].as_py() == category
    assert csv_table.column("category")[1].as_py() == second_category
    assert csv_table.column("source")[0].as_py() == "source1"
    assert csv_table.column("source")[1].as_py() == "source2"
    assert csv_table.column("content")[0].as_py() == content
    assert csv_table.column("content")[1].as_py() == second_content

    assert report.report_results[0].source == "source1"
    assert report.report_results[1].source == "source2"
    assert report.report_results[0].results[0].category == category
    assert report.report_results[1].results[0].category == second_category
    assert report.report_results[0].results[0].content == content
    assert report.report_results[1].results[0].content == second_content
