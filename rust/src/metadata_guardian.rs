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
#[derive(Debug, PartialEq, Eq, Serialize, Deserialize)]
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
#[derive(Debug, Serialize, Deserialize)]
pub struct DataRules {
    /// Category of the regex
    pub category: String,
    /// All the data rules
    pub data_rules: Vec<DataRule>,
    /// Compiled regex set (not serialized, reconstructed after deserialization)
    #[serde(skip)]
    regex_set: RegexSet,
}

impl PartialEq for DataRules {
    fn eq(&self, other: &Self) -> bool {
        self.category == other.category && self.data_rules == other.data_rules
    }
}

impl Eq for DataRules {}

impl DataRules {
    /// Create a new Data Rules.
    pub fn new(category: &str, data_rules: Vec<DataRule>) -> Result<Self, MetadataGuardianError> {
        let patterns: Vec<&str> = data_rules.iter().map(|dr| dr.pattern.as_str()).collect();
        let regex_set = RegexSet::new(&patterns)?;

        Ok(DataRules {
            category: category.to_string(),
            data_rules,
            regex_set,
        })
    }

    /// Create a new Data Rules from a path.
    pub fn from_path(path: &str) -> Result<Self, MetadataGuardianError> {
        let file = std::fs::File::open(path)?;

        // Deserialize into a temporary struct that doesn't have the regex_set field
        #[derive(Deserialize)]
        struct TempDataRules {
            category: String,
            data_rules: Vec<DataRule>,
        }

        let temp: TempDataRules = serde_yaml::from_reader(file)?;
        Self::new(&temp.category, temp.data_rules)
    }

    /// Validate a word based on the data rules.
    pub fn validate_word<'a>(&'a self, word: &'a str) -> MetadataGuardianResults<'a> {
        let data_rules: Vec<&DataRule> = self
            .regex_set
            .matches(word)
            .into_iter()
            .map(|index| &self.data_rules[index])
            .collect();
        MetadataGuardianResults {
            category: &self.category,
            content: word.to_string(),
            data_rules,
        }
    }

    /// Validate a list of words based on the data rules.
    pub fn validate_words<'a>(&'a self, words: Vec<&'a str>) -> Vec<MetadataGuardianResults<'a>> {
        words
            .into_par_iter()
            .filter(|line| !line.is_empty())
            .flat_map(|content| {
                let data_rules: Vec<&DataRule> = self
                    .regex_set
                    .matches(content)
                    .into_iter()
                    .map(|index| &self.data_rules[index])
                    .collect();
                if !data_rules.is_empty() {
                    Some(MetadataGuardianResults {
                        category: &self.category,
                        content: content.to_string(),
                        data_rules,
                    })
                } else {
                    None
                }
            })
            .collect()
    }

    /// Validate a file content based on the data rules.
    pub fn validate_file<'a>(
        &'a self,
        uri: &'a str,
    ) -> Result<Vec<MetadataGuardianResults<'a>>, MetadataGuardianError> {
        let file = File::open(uri)?;
        let reader = BufReader::new(file);

        let results = reader
            .lines()
            .map_while(Result::ok)
            .par_bridge()
            .flat_map(|content| {
                let data_rules: Vec<&DataRule> = self
                    .regex_set
                    .matches(&content)
                    .into_iter()
                    .map(|index| &self.data_rules[index])
                    .collect();

                if !data_rules.is_empty() {
                    Some(MetadataGuardianResults {
                        category: &self.category,
                        content,
                        data_rules,
                    })
                } else {
                    None
                }
            })
            .collect();

        Ok(results)
    }
}

/// Metadata Guardian results.
#[derive(Debug, PartialEq, Eq)]
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
