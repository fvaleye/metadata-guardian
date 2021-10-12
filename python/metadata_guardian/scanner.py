from abc import ABC, abstractmethod
from dataclasses import dataclass

from .data_rules import DataRules
from .report import MetadataGuardianReport, ReportResults
from .source import ExternalMetadataSource, LocalMetadataSource, MetadataSource


class Scanner(ABC):
    """Scanner interface."""

    @abstractmethod
    def scan_local(self, source: LocalMetadataSource) -> MetadataGuardianReport:
        """
        Scan the column names from local source.
        :param source: the LocalMetadataSource to scan
        :return: Metadata Guardian report
        """
        pass

    @abstractmethod
    def scan_external(
        self,
        source: ExternalMetadataSource,
        database_name: str,
        table_name: str,
        include_comment: bool,
    ) -> MetadataGuardianReport:
        """
        Scan the column names from external source.
        :param source: the ExternalMetadataSource to scan
        :param database_name: the name of the database
        :param table_name: the name of the table
        :param include_comment: the scan include the comment section
        :return: Metadata Guardian report
        """
        pass


@dataclass
class ColumnScanner(Scanner):
    """Column Scanner instance."""

    data_rules: DataRules

    def scan_local(self, source: LocalMetadataSource) -> MetadataGuardianReport:
        """
        Scan the column names from source.
        :param source: the MetadataSource to scan
        :return: Metadata Guardian report
        """
        return MetadataGuardianReport(
            report_results=[
                ReportResults(
                    source=source.local_path,
                    results=self.data_rules.validate_words(
                        words=source.get_column_names()
                    ),
                )
            ]
        )

    def scan_external(
        self,
        source: ExternalMetadataSource,
        database_name: str,
        table_name: str,
        include_comment: bool,
    ) -> MetadataGuardianReport:
        """
        Scan the column names from external source.
        :param source: the ExternalMetadataSource to scan
        :param database_name: the name of the database
        :param table_name: the name of the table
        :param include_comment: the scan include the comment section
        :return: Metadata Guardian report
        """
        return MetadataGuardianReport(
            report_results=[
                ReportResults(
                    source=f"{database_name}.{table_name}",
                    results=self.data_rules.validate_words(
                        words=source.get_column_names(
                            database_name=database_name,
                            table_name=table_name,
                            include_comment=include_comment,
                        )
                    ),
                )
            ]
        )


@dataclass
class ContentFileScanner:
    """Content Files Scanner instance."""

    data_rules: DataRules

    def scan_local_file(self, path: str) -> MetadataGuardianReport:
        """
        Scan a file with data rules.
        :param path: the path of the file to scan
        :return: Metadata Guardian report
        """
        return MetadataGuardianReport(
            report_results=[
                ReportResults(
                    source=path, results=self.data_rules.validate_file(path=path)
                )
            ]
        )
