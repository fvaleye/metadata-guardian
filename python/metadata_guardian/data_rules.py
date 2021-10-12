from dataclasses import dataclass
from enum import Enum
from typing import List

from .metadata_guardian import RawDataRules


class AvailableCategory(Enum):
    """Available Data Rules Categories."""

    PII = "PII"
    INCLUSION = "INCLUSION"


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

    def __init__(self, uri: str) -> None:
        self._data_rules = RawDataRules(uri)

    @classmethod
    def from_available_category(cls, category: AvailableCategory) -> "DataRules":
        """
        Get Data Rules from an available category.
        :param category: the available category of the data rules
        :return:
        """
        return cls(uri=RawDataRules.get_data_rules_uri(category.value))

    def validate_word(self, word: str) -> MetadataGuardianResults:
        """
        Validate a word with the data rules defined.
        :param word: the word to validate
        :return: the metadata guardian results
        """
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
        Validate a list of words with the data rules defined.:param word: the word to validate
        :param words: the words to validate
        :return: the metadata guardian results
        """
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

    def __str__(self) -> str:
        return f"DataRules({[str(data_rule) for data_rule in self._data_rules]})"

    def __repr__(self) -> str:
        return f"DataRules({[str(data_rule) for data_rule in self._data_rules]})"
