Usage
====================================

Metadata Guardian
-----------------

Scan the column names of a local source:

>>> from metadata_guardian import DataRules, ColumnScanner, AvailableCategory
>>> from metadata_guardian.source import ParquetSource
>>>
>>> data_rules = DataRules.from_available_category(category=AvailableCategory.PII)
>>> source = ParquetSource("file.parquet")
>>> column_scanner = ColumnScanner(data_rules=data_rules)
>>> report = column_scanner.scan_local(source)
>>> report.to_console()

Scan the column names of a external source on a table:

>>> from metadata_guardian import DataRules, ColumnScanner, AvailableCategory
>>> from metadata_guardian.source.external.snowflake_source import SnowflakeSource
>>>
>>> data_rules = DataRules.from_available_category(category=AvailableCategory.PII)
>>> source = SnowflakeSource(sf_account="account", sf_user="sf_user", sf_password="sf_password", warehouse="warehouse", schema_name="schema_name")
>>> column_scanner = ColumnScanner(data_rules=data_rules)
>>> report = column_scanner.scan_external(source, database_name="database_name", table_name="table_name", include_comment=True)
>>> report.to_console()

Scan the column names of a external source on database:

>>> from metadata_guardian import DataRules, ColumnScanner, AvailableCategory
>>> from metadata_guardian.source.external.snowflake_source import SnowflakeSource
>>>
>>> data_rules = DataRules.from_available_category(category=AvailableCategory.PII)
>>> source = SnowflakeSource(sf_account="account", sf_user="sf_user", sf_password="sf_password", warehouse="warehouse", schema_name="schema_name")
>>> column_scanner = ColumnScanner(data_rules=data_rules)
>>> report = column_scanner.scan_external(source, database_name="database_name", include_comment=True)
>>> report.to_console()

Scan the column names of an external source for a database asynchronously with asyncio:

>>> import asyncio
>>> from metadata_guardian import DataRules, ColumnScanner, AvailableCategory
>>> from metadata_guardian.source.external.snowflake_source import SnowflakeSource
>>>
>>> data_rules = DataRules.from_available_category(category=AvailableCategory.PII)
>>> source = SnowflakeSource(sf_account="account", sf_user="sf_user", sf_password="sf_password", warehouse="warehouse", schema_name="schema_name")
>>> column_scanner = ColumnScanner(data_rules=data_rules)
>>> report = asyncio.run(column_scanner.scan_external(source, database_name="database_name", include_comment=True))
>>> report.to_console()

Scan the column names of a local source:

>>> from metadata_guardian import DataRules, ColumnScanner, AvailableCategory, MetadataGuardianReport
>>> from metadata_guardian.source import ParquetSource
>>>
>>> data_rules = DataRules.from_available_category(category=AvailableCategory.PII)
>>> column_scanner = ColumnScanner(data_rules=data_rules)
>>> report = MetadataGuardianReport()
>>> for path in paths:
>>>     source = ParquetSource(path)
>>>     report.append(column_scanner.scan_local(source))
>>> report.to_console()

Scan content of a file:

>>> from metadata_guardian import DataRules, ContentFilesScanner, AvailableCategory
>>>
>>> data_rules = DataRules.from_available_category(category=AvailableCategory.PII)
>>> content_file_scanner = ContentFilesScanner(data_rules=data_rules)
>>> report = content_file_scanner.scan_local_file(path="path")
>>> report.to_console()

