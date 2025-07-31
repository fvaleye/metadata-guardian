import asyncio
import json
from typing import Any, List, Optional

import typer
from loguru import logger

from ... import ColumnScanner, DataRules
from ...source.external.external_metadata_source import ExternalMetadataSource

app = typer.Typer()


def get_external_source(source: str, configuration: str) -> ExternalMetadataSource:
    sources = list(displayed=False)
    if source not in sources:
        raise ValueError(f"This source is not available in the list: {sources}")

    try:
        selected_source = next(
            cls
            for cls in ExternalMetadataSource.__subclasses__()
            if cls.type() == source
        )
    except Exception as exception:
        logger.exception("This source initiation failed.")
        raise exception
    return selected_source.parse_raw(configuration)


@app.command(help="List the external metadata sources")
def list(displayed: bool = True) -> List[str]:
    sources = [cls.type() for cls in ExternalMetadataSource.__subclasses__()]
    if displayed:
        logger.info(f"Available External sources: {sources}")
    return sources


@app.command(help="Scan async the external metadata sources with the ColumnScanner")
def scan_async(
    external_source: str,
    database_name: str,
    data_rules_path: str,
    configuration: str,
    table_name: Optional[str] = None,
    include_comments: bool = False,
) -> None:
    source = get_external_source(source=external_source, configuration=configuration)

    data_rules = DataRules.from_path(path=data_rules_path)
    column_scanner = ColumnScanner(
        data_rules=data_rules, progression_bar_disabled=False
    )
    with source:
        with source:
            report = asyncio.run(
                column_scanner.scan_external_async(
                    source,
                    database_name=database_name,
                    include_comment=include_comments,
                    table_name=table_name,
                )
            )
            report.to_console()


@app.command(help="Scan the external metadata sources with the ColumnScanner")
def scan(
    external_source: str,
    database_name: str,
    data_rules_path: str,
    configuration: str,
    table_name: Optional[str] = None,
    include_comments: bool = False,
) -> None:
    source = get_external_source(source=external_source, configuration=configuration)

    data_rules = DataRules.from_path(path=data_rules_path)
    column_scanner = ColumnScanner(
        data_rules=data_rules, progression_bar_disabled=False
    )
    with source:
        report = column_scanner.scan_external(
            source,
            database_name=database_name,
            table_name=table_name,
            include_comment=include_comments,
        )
        report.to_console()
