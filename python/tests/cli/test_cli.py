from metadata_guardian.cli.external import get_external_source, scan_async
from metadata_guardian.cli.local import get_local_source
from metadata_guardian.source import MySQLSource, ParquetSource


def test_get_external_source_():
    source = "MySQL"
    configuration = (
        '{"user": "user", "password": "password", "host": "host",'
        ' "extra_connection_args": {"test": "True"}}'
    )
    expected = MySQLSource.parse_raw(configuration)

    source = get_external_source(source=source, configuration=configuration)

    assert source == expected


def test_get_local_source_():
    source = "Parquet"
    path = "path"
    expected = ParquetSource(**{"local_path": path})

    source = get_local_source(source=source, path=path)

    assert source == expected


def test_scan_async_opens_source_once(mocker):
    source = mocker.MagicMock()
    report = mocker.MagicMock()
    column_scanner = mocker.MagicMock()
    column_scanner.scan_external_async = mocker.AsyncMock(return_value=report)
    mocker.patch(
        "metadata_guardian.cli.external.get_external_source", return_value=source
    )
    mocker.patch("metadata_guardian.cli.external.DataRules.from_path")
    mocker.patch(
        "metadata_guardian.cli.external.ColumnScanner", return_value=column_scanner
    )

    scan_async("MySQL", "database", "rules.yaml", "{}")

    source.__enter__.assert_called_once_with()
    source.__exit__.assert_called_once()
