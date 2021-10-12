from typing import List

from loguru import logger
from rich.console import Console
from rich.table import Table

from .data_rules import MetadataGuardianResults


class MetadataGuardianReport:
    """Metadata Guardian Results."""

    @classmethod
    def to_console(cls, results: List[MetadataGuardianResults]) -> None:
        """
        Display the metdata guardian results to the console.
        :param results: the results to display
        :return:
        """
        _console = Console()
        _table = Table(
            title="MetadataGuardian report", show_header=True, header_style="bold dim"
        )
        _table.add_column("Category", style="yellow", width=30)
        _table.add_column("Content", style="cyan", width=30)
        _table.add_column("Name", style="magenta", width=30)
        _table.add_column("Pattern")
        _table.add_column("Documentation", width=50)
        for result in results:
            for data_rule in result.data_rules:
                _table.add_row(
                    result.category,
                    result.content,
                    data_rule.rule_name,
                    data_rule.regex_pattern,
                    data_rule.documentation,
                )
        if _table.rows:
            _console.log(
                f"MetadataGuardian detected {len(results)} data rule violation(s)."
            )
            _console.print(_table)
        else:
            logger.info(f"No data rule violation(s) were detected by MetadataGuardian.")
