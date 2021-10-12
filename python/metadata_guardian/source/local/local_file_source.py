from dataclasses import dataclass
from typing import Any, Dict, List

from .local_metadata_source import LocalMetadataSource


@dataclass
class LocalFileSource(LocalMetadataSource):
    def read(self):
        """
        Read the local file.
        :return: the file content
        """
        with open(self.local_path, "rb") as file:
            lines = file.readlines()
        return [line.rstrip() for line in lines]

    def schema(self) -> Dict[str, Any]:
        """
        Get the schema.
        :return:
        """
        raise NotImplementedError()

    def get_column_names(self) -> List[str]:
        """
        Get all the lines of the file
        :return: the lines of the files
        """
        lines = list()
        with open(self.local_path, "r") as file:
            content = file.readlines()
            for line in content:
                if line:
                    lines.append(line)
        return lines

    @property
    def type(self) -> str:
        """
        The type of the source.
        :return: the name o of the source.
        """
        return "LocalFile"
