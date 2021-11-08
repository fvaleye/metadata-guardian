import asyncio
import os
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional

from loguru import logger
from pyarrow import cpu_count

from .data_rules import DataRules
from .report import MetadataGuardianReport, ReportResults
from .source import ExternalMetadataSource, LocalMetadataSource, MetadataSource


class Scanner(ABC):
    """Scanner interface."""

    @abstractmethod
    def scan_local(self, source: LocalMetadataSource) -> MetadataGuardianReport:
        """
        Scan the column names from the local source.
        :param source: the LocalMetadataSource to scan
        :return: a Metadata Guardian report
        """
        pass

    @abstractmethod
    def scan_external(
        self,
        source: ExternalMetadataSource,
        database_name: str,
        table_name: Optional[str] = None,
        include_comment: bool = False,
    ) -> MetadataGuardianReport:
        """
        Scan the column names from the external source.
        :param source: the ExternalMetadataSource to scan
        :param database_name: the name of the database
        :param table_name: the name of the table
        :param include_comment: the scan include the comment section
        :return: a Metadata Guardian report
        """
        pass

    @abstractmethod
    async def scan_external_async(
        self,
        source: ExternalMetadataSource,
        database_name: str,
        tasks_limit: int,
        table_name: Optional[str] = None,
        include_comment: bool = False,
    ) -> MetadataGuardianReport:
        """
        Scan the column names from the external source asynchronously.
        :param source: the ExternalMetadataSource to scan
        :param database_name: the name of the database
        :param tasks_limit: the limit of the tasks to run in parallel
        :param table_name: the name of the table
        :param include_comment: the scan include the comment section
        :return: a Metadata Guardian report
        """
        pass


@dataclass
class ColumnScanner(Scanner):
    """Column Scanner instance."""

    data_rules: DataRules

    def scan_local(self, source: LocalMetadataSource) -> MetadataGuardianReport:
        """
        Scan the column names from the local source.
        :param source: the MetadataSource to scan
        :return: a Metadata Guardian report
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
        table_name: Optional[str] = None,
        include_comment: bool = False,
    ) -> MetadataGuardianReport:
        """
        Scan the column names from the external source using a table name or a database name.
        :param source: the ExternalMetadataSource to scan
        :param database_name: the name of the database
        :param table_name: the name of the table
        :param include_comment: the scan include the comment section
        :return: a Metadata Guardian report
        """
        if table_name:
            logger.debug(
                f"Get the column names list from the table {database_name}.{table_name}"
            )
            report = MetadataGuardianReport(
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
        else:
            report = MetadataGuardianReport()
            logger.debug(
                f"Get the table names list from the database {database_name} for {source.type}"
            )
            table_names_list = source.get_table_names_list(database_name=database_name)
            for table_name in table_names_list:
                logger.debug(
                    f"Get the column names list from the table {database_name}.{table_name}"
                )
                report.append(
                    MetadataGuardianReport(
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
                )
        return report

    async def scan_external_async(
        self,
        source: ExternalMetadataSource,
        database_name: str,
        tasks_limit: int = cpu_count(),
        table_name: Optional[str] = None,
        include_comment: bool = False,
    ) -> MetadataGuardianReport:
        """
        Scan the column names from the external source using a table name or a database name.
        Note that it can generate multiple concurrent calls to your metadata source.

        :param source: the ExternalMetadataSource to scan
        :param database_name: the name of the database
        :param tasks_limit: the limit of the tasks to run in parallel
        :param table_name: the name of the table
        :param include_comment: the scan include the comment section
        :return: a Metadata Guardian report
        """
        semaphore = asyncio.Semaphore(tasks_limit)

        async def async_validate_words(table_name: str) -> ReportResults:
            async with semaphore:
                logger.debug(
                    f"Get the column names list from the table {database_name}.{table_name}"
                )
                loop = asyncio.get_event_loop()
                words = await loop.run_in_executor(
                    None,
                    source.get_column_names,
                    database_name,
                    table_name,
                    include_comment,
                )
                return ReportResults(
                    source=f"{database_name}.{table_name}",
                    results=self.data_rules.validate_words(words=words),
                )

        if table_name:
            tasks = [async_validate_words(table_name=table_name)]
        else:
            table_names_list = source.get_table_names_list(database_name=database_name)
            logger.debug(
                f"Get the table names list from the database {database_name} for {source.type}"
            )

            tasks = [
                async_validate_words(table_name=table_name)
                for table_name in table_names_list
            ]
        report_results = await asyncio.gather(*tasks)
        report = MetadataGuardianReport(report_results=report_results)
        return report


@dataclass
class ContentFilesScanner:
    """Content Files Scanner instance."""

    data_rules: DataRules

    def scan_local_file(self, path: str) -> MetadataGuardianReport:
        """
        Scan a file with data rules.
        :param path: the path of the file to scan
        :return: a Metadata Guardian report
        """
        return MetadataGuardianReport(
            report_results=[
                ReportResults(
                    source=path, results=self.data_rules.validate_file(path=path)
                )
            ]
        )

    def scan_directory(
        self, directory_path: str, file_names_extension: str
    ) -> MetadataGuardianReport:
        """
        Scan all the files inside directory path with the file name extension.
        :param directory_path: the directory path to scan
        :param file_names_extension: the file name extension to include (without the .)
        :return: a Metadata Guardian report
        """
        report = MetadataGuardianReport()
        for root, dirs, files in os.walk(directory_path):
            for name in files:
                if name.endswith(f".{file_names_extension}"):
                    report.append(
                        other_report=self.scan_local_file(path=f"{root}/{name}")
                    )
        return report
