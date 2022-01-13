import importlib.resources
from dataclasses import dataclass
from enum import Enum
from typing import List

from loguru import logger

from .metadata_guardian import RawDataRules


class AvailableCategory(Enum):
    """Available Data Rules Categories."""

    PII = "pii_rules.yaml"
    INCLUSION = "inclusion_rules.yaml"


@dataclass
class DataRule:
    """DataRule instance with a regex pattern and a documentation."""

    rule_name: str
    regex_pattern: str
    documentation: str


@dataclass
class MetadataGuardianResults:
    """Metadata Guardian Results instance with the content that matches with the data rules."""

    category: str
    content: str
    data_rules: List[DataRule]


@dataclass(init=False)
class DataRules:
    """Data Rules instances."""

    def __init__(self, data_rules: RawDataRules) -> None:
        self._data_rules = data_rules

    @classmethod
    def from_path(cls, path: str) -> "DataRules":
        """
        Get Data Rules from a path.

        :param path: the path of the yaml file
        :return: the Data Rules instance
        """
        data_rules = RawDataRules.from_path(path)
        return cls(data_rules=data_rules)

    @classmethod
    def from_available_category(cls, category: AvailableCategory) -> "DataRules":
        """
        Get Data Rules from an available category.

        :param category: the available category of the data rules
        :return: the Data Rules instance
        """
        logger.debug(f"Creating Data Rules from the category {category.value}")
        if not isinstance(category, AvailableCategory):
            raise ValueError("The category must be an instance of AvailableCategory")
        with importlib.resources.path(
            "metadata_guardian.rules", category.value
        ) as resource:
            path = str(resource)
            return cls.from_path(path=path)

    def validate_word(self, word: str) -> MetadataGuardianResults:
        """
        Validate a word with the data rules defined.

        :param word: the word to validate
        :return: the metadata guardian results
        """
        logger.debug(f"Validate the Data Rules with the word {word}")
        result = self._data_rules.validate_word(word=word)
        return MetadataGuardianResults(
            category=result._category,
            content=result._content,
            data_rules=[
                DataRule(
                    data_rule.rule_name,
                    data_rule.pattern,
                    data_rule.documentation,
                )
                for data_rule in result._data_rules
            ],
        )

    def validate_words(self, words: List[str]) -> List[MetadataGuardianResults]:
        """
        Validate a list of words with the data rules defined.:param word: the word to validate.

        :param words: the words to validate
        :return: the metadata guardian results
        """
        logger.debug(f"Validate the Data Rules with the words {words}")
        results = self._data_rules.validate_words(words=words)
        return [
            MetadataGuardianResults(
                category=result._category,
                content=result._content,
                data_rules=[
                    DataRule(
                        data_rule.rule_name,
                        data_rule.pattern,
                        data_rule.documentation,
                    )
                    for data_rule in result._data_rules
                ],
            )
            for result in results
        ]

    def validate_file(self, path: str) -> List[MetadataGuardianResults]:
        """
        Validate a file content with the data rules defined.

        :param path: the file path
        :return: the metadata guardian results
        """
        logger.debug(f"Validate the Data Rules in the path {path}")
        results = self._data_rules.validate_file(path)
        return [
            MetadataGuardianResults(
                category=result._category,
                content=result._content,
                data_rules=[
                    DataRule(
                        data_rule.rule_name,
                        data_rule.pattern,
                        data_rule.documentation,
                    )
                    for data_rule in result._data_rules
                ],
            )
            for result in results
        ]
