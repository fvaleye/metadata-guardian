from dataclasses import dataclass, field
from typing import List, NamedTuple, Optional, Tuple

from rich.console import Console
from rich.progress import (
    BarColumn,
    Progress,
    SpinnerColumn,
    TaskID,
    TextColumn,
    TimeRemainingColumn,
)
from rich.table import Table

from .data_rules import MetadataGuardianResults


@dataclass(init=False)
class ProgressionBar(Progress):
    """
    Progression Bar provides a progression bar to display the results of the scanner.
    """

    task_id: Optional[TaskID] = None

    def __init__(self) -> None:
        super().__init__(
            SpinnerColumn(),
            "[progress.description]{task.description}: [red]{task.fields[current_item]}",
            BarColumn(),
            "[progress.percentage]{task.percentage:>3.0f}% ({task.completed}/{task.total})-",
            TimeRemainingColumn(),
        )

    def add_task(  # type: ignore
        self, item_name: str, source_type: str, total: int, current_item: str = ""
    ) -> int:
        """
        Add task in the Progression Bar.
        :param item_name: the name of the item to search
        :param current_item: the name of the current item
        :param source_type: the source type
        :param total: total of the number of tables
        :return: the created Task
        """
        task_id = super().add_task(
            f"[bold cyan]Searching in {item_name} for the {source_type} metadata source",
            total=total,
            current_item=current_item,
        )
        self.task_id = task_id
        return task_id

    def update(self, current_item: str) -> None:  # type: ignore
        """
        Update the task of the Progression Bar.
        :param current_item: the name of the current item
        :return:
        """
        if self.task_id is not None:
            super().update(self.task_id, advance=1, current_item=current_item)

    def terminate(self) -> None:
        """
        Terminate the current task
        :return:
        """
        if self.task_id is not None:
            super().update(self.task_id, current_item="Done")


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
            title=":magnifying_glass_tilted_right: Metadata Guardian report",
            show_header=True,
            header_style="bold dim",
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
            _console.print(
                f":exclamation: Metadata Guardian detected {len(_table.rows)} data rules violations."
            )
            _console.print(_table)
        else:
            _console.print(
                f":thumbs_up: No data rules violation were detected by Metadata Guardian."
            )
