from typing import List

import typer
from loguru import logger

from ... import ColumnScanner, DataRules
from ...source.local.local_metadata_source import LocalMetadataSource

app = typer.Typer()


def get_local_source(source: str, path: str):  # type: ignore
    sources = list(displayed=False)
    if source not in sources:
        raise ValueError(f"This source is not available in the list: {sources}")

    try:
        selected_source = next(
            cls
            for cls in LocalMetadataSource.__subclasses__()
            if str(cls.type) == source
        )(local_path=path)
    except Exception as exception:
        logger.exception("This source initiation failed.")
        raise exception
    return selected_source


@app.command(help="List the local metadata sources")
def list(displayed: bool = True) -> List[str]:
    sources = [str(cls.type) for cls in LocalMetadataSource.__subclasses__()]
    if displayed:
        logger.info(f"Available External sources: {sources}")
    return sources


@app.command(help="Scan the local metadata sources with the ColumnScanner")
def scan(local_source: str, data_rules_path: str, path: str) -> None:
    source = get_local_source(source=local_source, path=path)

    data_rules = DataRules.from_path(path=data_rules_path)
    column_scanner = ColumnScanner(
        data_rules=data_rules, progression_bar_disabled=False
    )
    report = column_scanner.scan_local(source=source)
    report.to_console()
