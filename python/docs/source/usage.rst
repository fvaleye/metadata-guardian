Usage
====================================

Metadata Guardian
-----------------

Local Source, one result
.. code-block:: python

>>> from metadata_guardian import DataRules, ColumnScanner, AvailableCategory
>>> from metadata_guardian.source import AvroSchemaSource
>>>
>>> data_rules = DataRules.from_available_category(category=AvailableCategory.PII)
>>> source = AvroSchemaSource("avro_schema.json")
>>> column_scanner = ColumnScanner(data_rules=data_rules)
>>> report = column_scanner.scan_local(source)
>>> report
MetadataGuardianReport(report_results=[ReportResults(source='/Users/florian.valeye/Documents/workspace/MetadataGuardian/python/metadata_guardian/test2.json', results=[MetadataGuardianResults(category='PII', content='username', data_rules=[DataRule(rule_name='user name', regex_pattern='(.*user(id|name|).*)', documentation='The user name is a personal identifiable information.\n')])])])
>>> report.to_console()

Scan column names of an external Source, one result
.. code-block:: python

>>> from metadata_guardian import DataRules, ColumnScanner, AvailableCategory
>>> from metadata_guardian.source import SnowflakeSource
>>>
>>> data_rules = DataRules.from_available_category(category=AvailableCategory.PII)
>>> source = SnowflakeSource(sf_account="account", sf_user="sf_user", sf_password="sf_password", warehouse="warehouse", schema_name="schema_name")
>>> column_scanner = ColumnScanner(data_rules=data_rules)
>>> report = column_scanner.scan_external(source, database_name="database_name", table_name="table_name", include_comment=True)
>>> report.to_console()

Scan column names of a local source, multiple result
.. code-block:: python

>>> from metadata_guardian import DataRules, ColumnScanner, AvailableCategory, MetadataGuardianReport
>>> from metadata_guardian.source import AvroSchemaSource
>>>
>>> data_rules = DataRules.from_available_category(category=AvailableCategory.PII)
>>> column_scanner = ColumnScanner(data_rules=data_rules)
>>> report = MetadataGuardianReport()
>>> for path in paths:
>>>     source = AvroSchemaSource(path)
>>>     report.append(column_scanner.scan_local(source))
>>> report.to_console()

Scan content of a file
>>> from metadata_guardian import DataRules, ContentFileScanner, AvailableCategory
>>> from metadata_guardian.source import SnowflakeSource
>>>
>>> data_rules = DataRules.from_available_category(category=AvailableCategory.PII)
>>> column_scanner = ContentFileScanner(data_rules=data_rules)
>>> report = column_scanner.scan_local_file(path="path")
>>> report.to_console()

