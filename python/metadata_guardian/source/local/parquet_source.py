from .local_metadata_source import LocalMetadataSource


class ParquetSource(LocalMetadataSource):
    """Instance for a local Parquet file."""

    @classmethod
    def type(cls) -> str:
        """
        The type of the source.

        :return: the name of the source.
        """
        return "Parquet"
