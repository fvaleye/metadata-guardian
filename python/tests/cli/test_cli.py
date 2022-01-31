from metadata_guardian.cli.external import get_external_source
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
