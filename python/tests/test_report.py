from metadata_guardian.data_rules import DataRules, MetadataGuardianResults
from metadata_guardian.report import MetadataGuardianReport, ReportResults


def test_report_append_results():
    category = "category"
    content = "content"
    second_category = "second_category"
    second_content = "second_content"
    results = ReportResults(
        source="source1",
        results=[
            MetadataGuardianResults(category=category, content=content, data_rules=[])
        ],
    )
    other_report = MetadataGuardianReport(
        report_results=[
            ReportResults(
                source="source2",
                results=[
                    MetadataGuardianResults(
                        category=second_category, content=second_content, data_rules=[]
                    )
                ],
            )
        ]
    )

    report = MetadataGuardianReport(report_results=[results])
    report.append(other_report)

    assert report.report_results[0].source == "source1"
    assert report.report_results[1].source == "source2"
    assert report.report_results[0].results[0].category == category
    assert report.report_results[1].results[0].category == second_category
    assert report.report_results[0].results[0].content == content
    assert report.report_results[1].results[0].content == second_content
