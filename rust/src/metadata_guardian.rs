use rayon::prelude::*;
use regex::RegexSet;
use serde::{Deserialize, Serialize};
use std::fs::File;
use std::io::BufRead;
use std::io::BufReader;

/// Metadata Guardian specific error.
#[derive(thiserror::Error, Debug)]
pub enum MetadataGuardianError {
    /// Error returned when there is an error in reading the yaml file.
    #[error("Error when reading the file: {}", .source)]
    FileNotFound {
        /// File error details returned.
        #[from]
        source: std::io::Error,
    },
    /// Error returned when there is an error in parsing the yaml file.
    #[error("Error when parsing the YAML file: {}", .source)]
    InvalidYaml {
        /// YAML error details returned.
        #[from]
        source: serde_yaml::Error,
    },
    /// The Regex given by the Data Rules are not valid.
    #[error("Error when applying the Regex {}", .source)]
    InvalidRegex {
        /// Regex error details returned.
        #[from]
        source: regex::Error,
    },
}

/// A Data Rule instance specify a specific rule with a regex pattern.
#[derive(Debug, PartialEq, Serialize, Deserialize)]
pub struct DataRule {
    /// Name of the rule
    pub rule_name: String,
    /// Regex pattern
    pub pattern: String,
    /// Documentation of the rule
    pub documentation: String,
}

impl DataRule {
    /// Create a new instance of the DataRule.
    pub fn new(rule_name: String, pattern: String, documentation: String) -> Self {
        Self {
            rule_name,
            pattern,
            documentation,
        }
    }
}

/// A Data Rules specifies all the regex to apply based on one category.
#[derive(Debug, PartialEq, Serialize, Deserialize)]
pub struct DataRules {
    /// Category of the regex
    category: String,
    /// All the data rules
    data_rules: Vec<DataRule>,
}

impl DataRules {
    /// Create a new Data Rules.
    pub fn new(path: &str) -> Result<Self, MetadataGuardianError> {
        let file = std::fs::File::open(path)?;
        let data_rules: DataRules = serde_yaml::from_reader(file)?;
        Ok(data_rules)
    }

    /// Validate a word based on the data rules.
    pub fn validate_word<'a>(
        &'a self,
        word: &'a str,
    ) -> Result<MetadataGuardianResults<'a>, MetadataGuardianError> {
        let patterns: Vec<&str> = self
            .data_rules
            .iter()
            .map(|dr| dr.pattern.as_ref())
            .collect();
        let regex_set = RegexSet::new(&patterns)?;
        let result = regex_set.matches(word).into_iter().collect::<Vec<usize>>();
        Ok(MetadataGuardianResults {
            category: &self.category,
            content: word.to_string(),
            data_rules: self
                .data_rules
                .iter()
                .enumerate()
                .filter(|(index, _)| result.contains(index))
                .map(|(_, dr)| dr)
                .collect(),
        })
    }

    /// Validate a list of words based on the data rules.
    pub fn validate_words<'a>(
        &'a self,
        words: Vec<&'a str>,
    ) -> Result<Vec<MetadataGuardianResults<'a>>, MetadataGuardianError> {
        let patterns: Vec<&str> = self
            .data_rules
            .iter()
            .map(|dr| dr.pattern.as_ref())
            .collect();
        let regex_set = RegexSet::new(&patterns).unwrap();

        let results = words
            .into_iter()
            .filter(|line| !line.is_empty())
            .par_bridge()
            .fold(Vec::new, |mut accumulator, content| {
                let data_rules = regex_set
                    .matches(content)
                    .into_iter()
                    .map(|index| &self.data_rules[index])
                    .collect::<Vec<&DataRule>>();
                if !data_rules.is_empty() {
                    accumulator.push(MetadataGuardianResults {
                        category: &self.category,
                        content: content.to_string(),
                        data_rules,
                    });
                }
                accumulator
            })
            .reduce(Vec::new, |mut vector_1, mut vector_2| {
                vector_1.append(&mut vector_2);
                vector_1
            });

        Ok(results)
    }

    /// Validate a file content based on the data rules.
    pub fn validate_file<'a>(
        &'a self,
        uri: &'a str,
    ) -> Result<Vec<MetadataGuardianResults<'a>>, MetadataGuardianError> {
        let patterns: Vec<&str> = self
            .data_rules
            .iter()
            .map(|dr| dr.pattern.as_ref())
            .collect();
        let file = File::open(uri)?;
        let regex_set = RegexSet::new(&patterns)?;
        let reader = BufReader::new(file);

        let results = reader
            .lines()
            .filter_map(|line: Result<String, _>| line.ok())
            .par_bridge()
            .fold(Vec::new, |mut accumulator, content| {
                let patterns_matched = regex_set.matches(&content).into_iter();
                let data_rules = patterns_matched
                    .into_iter()
                    .map(|index| &self.data_rules[index])
                    .collect::<Vec<&DataRule>>();
                if !data_rules.is_empty() {
                    accumulator.push(MetadataGuardianResults {
                        category: &self.category,
                        content,
                        data_rules,
                    });
                }
                accumulator
            })
            .reduce(Vec::new, |mut vector_1, mut vector_2| {
                vector_1.append(&mut vector_2);
                vector_1
            });

        Ok(results)
    }
}

/// Metadata Guardian results.
#[derive(Debug, PartialEq)]
pub struct MetadataGuardianResults<'a> {
    /// Content matched the rule.
    pub category: &'a str,
    /// Content matched the rule.
    pub content: String,
    /// The rules that matches the content.
    pub data_rules: Vec<&'a DataRule>,
}

/// Returns rust crate version, can be use used in language bindings to expose Rust core version
pub fn crate_version() -> &'static str {
    env!("CARGO_PKG_VERSION")
}
