from dataclasses import dataclass, field
from typing import List, NamedTuple, Optional, Tuple

from rich.console import Console
from rich.markup import escape
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

    def __init__(self, disable: bool) -> None:
        super().__init__(
            SpinnerColumn(),
            "[progress.description]{task.description}: [red]{task.fields[current_item]}",
            BarColumn(),
            "[progress.percentage]{task.percentage:>3.0f}% ({task.completed}/{task.total})-",
            TimeRemainingColumn(),
            disable=disable,
        )

    def __enter__(self) -> "ProgressionBar":
        super().__enter__()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:  # type: ignore
        if self.task_id is not None:
            super().update(self.task_id, current_item="Done")
        super().__exit__(exc_type, exc_val, exc_tb)

    def add_task_with_item(
        self,
        item_name: str,
        source_type: str,
        total: int,
        current_item: str = "Starting",
    ) -> None:
        """
        Add task in the Progression Bar.

        :param item_name: the name of the item to search
        :param current_item: the name of the current item
        :param source_type: the source type
        :param total: total of the number of tables
        :return: the created Task
        """
        task_details = f"[{item_name}]" if item_name else ""
        task_description = f"[bold cyan]Searching in the {escape(source_type)} metadata source{escape(task_details)}"
        task_id = super().add_task(
            description=task_description,
            total=total,
            current_item=escape(current_item),
        )
        self.task_id = task_id

    def update_item(self, current_item: str) -> None:
        """
        Update the current item of the task.

        :param current_item: the name of the current item
        :return:
        """
        if self.task_id is not None:
            super().update(self.task_id, advance=1, current_item=current_item)


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
            header_style="bold",
            show_lines=True,
        )
        _table.add_column("Category", style="yellow", no_wrap=True)
        _table.add_column("Source", style="cyan", no_wrap=True)
        _table.add_column("Content", style="cyan", no_wrap=True)
        _table.add_column("Name", style="magenta", no_wrap=True)
        _table.add_column("Documentation")
        for report in self.report_results:
            for result in report.results:
                for data_rule in result.data_rules:
                    _table.add_row(
                        result.category,
                        report.source,
                        result.content.strip(),
                        data_rule.rule_name,
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
