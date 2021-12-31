Installation
====================================

Using Pip
---------
.. code-block:: bash

   # Install all the metadata sources
   pip install 'metadata_guardian[all]'

   # Install with one metadata source in the list
   pip install 'metadata_guardian[snowflake,avro,aws,gcp,deltalake,kafka_schema_registry]'