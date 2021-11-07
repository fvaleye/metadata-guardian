from dataclasses import dataclass, field
from typing import List, NamedTuple, Tuple

from loguru import logger
from rich.console import Console
from rich.table import Table

from .data_rules import MetadataGuardianResults


@dataclass
class ReportResults:
    """Metadata Guardian Results."""

    source: str
    results: List[MetadataGuardianResults] = field(default_factory=list)


@dataclass
class MetadataGuardianReport:
    """Metadata Guardian Report."""

    report_results: List[ReportResults] = field(default_factory=list)

    def append(self, other_report: "MetadataGuardianReport") -> None:
        """
        Concat the results before making the report.
        :param other_report: other report to append
        :return:
        """
        self.report_results = self.report_results + other_report.report_results

    def to_console(self) -> None:
        """
        Display the metadata guardian results to the console.
        :return:
        """
        _console = Console()
        _table = Table(
            title="MetadataGuardian report", show_header=True, header_style="bold dim"
        )
        _table.add_column("Category", style="yellow", width=30)
        _table.add_column("Source", style="cyan", width=30)
        _table.add_column("Content", style="cyan", width=30)
        _table.add_column("Name", style="magenta", width=30)
        _table.add_column("Pattern")
        _table.add_column("Documentation", width=50)
        for report in self.report_results:
            for result in report.results:
                for data_rule in result.data_rules:
                    _table.add_row(
                        result.category,
                        report.source,
                        result.content,
                        data_rule.rule_name,
                        data_rule.regex_pattern,
                        data_rule.documentation,
                    )
        if _table.rows:
            logger.warning(f"MetadataGuardian detected data rules violation(s).")
            _console.print(_table)
        else:
            logger.info(
                f"No data rules violation(s) were detected by MetadataGuardian."
            )
