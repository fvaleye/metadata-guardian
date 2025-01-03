extern crate pyo3;

use ::metadata_guardian::crate_version;
use ::metadata_guardian::DataRule;
use ::metadata_guardian::DataRules;
use ::metadata_guardian::MetadataGuardianError;
use ::metadata_guardian::MetadataGuardianResults;
use pyo3::create_exception;
use pyo3::exceptions::PyException;
use pyo3::prelude::*;
use pyo3::types::PyType;
create_exception!(metadata_guardian, PyMetadataGuardianError, PyException);

/// Python Metadata Guardian Errors.
impl PyMetadataGuardianError {
    /// Errors from the MetadataGuardian crate
    fn from_raw(err: MetadataGuardianError) -> PyErr {
        PyMetadataGuardianError::new_err(err.to_string())
    }
}

/// Raw Data Rules for Python binding.
#[pyclass]
struct RawDataRules {
    /// Data rules used by the Metadata Guardian.
    _data_rules: DataRules,
}

/// Raw Data Rule for Python binding.
#[pyclass]
#[derive(Clone)]
struct RawDataRule {
    /// Name of the rule
    #[pyo3(get)]
    rule_name: String,
    /// Regex pattern
    #[pyo3(get)]
    pattern: String,
    /// Documentation of the rule
    #[pyo3(get)]
    documentation: String,
}

/// Metadata Guardian results for Python Binding.
#[pyclass]
struct RawMetadataGuardianResults {
    /// Category of the matched rules.
    #[pyo3(get)]
    _category: String,
    /// Content matched the rules.
    #[pyo3(get)]
    _content: String,
    /// The rules that matches the content.
    #[pyo3(get)]
    _data_rules: Vec<RawDataRule>,
}

/// Create RawMetadataGuardianResults form MetadataGuardianResults
impl From<&MetadataGuardianResults<'_>> for RawMetadataGuardianResults {
    fn from(metadata_guardian_results: &MetadataGuardianResults) -> RawMetadataGuardianResults {
        RawMetadataGuardianResults {
            _category: metadata_guardian_results.category.to_string(),
            _content: metadata_guardian_results.content.to_string(),
            _data_rules: metadata_guardian_results
                .data_rules
                .iter()
                .map(|data_rule| RawDataRule {
                    rule_name: data_rule.rule_name.clone(),
                    pattern: data_rule.pattern.clone(),
                    documentation: data_rule.documentation.clone(),
                })
                .collect(),
        }
    }
}

#[pymethods]
impl RawDataRule {
    /// Create a new Raw Data Rule instance.
    #[new]
    fn new(rule_name: &str, pattern: &str, documentation: &str) -> PyResult<RawDataRule> {
        Ok(RawDataRule {
            rule_name: rule_name.to_string(),
            pattern: pattern.to_string(),
            documentation: documentation.to_string(),
        })
    }
}

#[pymethods]
impl RawDataRules {
    /// Create a new Raw Data Rules instance.
    #[new]
    fn new(category: &str, data_rules: Vec<RawDataRule>) -> PyResult<RawDataRules> {
        let data_rules = DataRules {
            category: category.to_string(),
            data_rules: data_rules
                .iter()
                .map(|data_rule| DataRule {
                    rule_name: data_rule.rule_name.clone(),
                    pattern: data_rule.pattern.clone(),
                    documentation: data_rule.documentation.clone(),
                })
                .collect(),
        };
        Ok(RawDataRules {
            _data_rules: data_rules,
        })
    }

    /// Create a new Raw Data Rules instance from path.
    #[classmethod]
    fn from_path(_cls: &Bound<'_, PyType>, path: &str) -> PyResult<Self> {
        let data_rules = DataRules::from_path(path).map_err(PyMetadataGuardianError::from_raw)?;
        Ok(RawDataRules {
            _data_rules: data_rules,
        })
    }

    /// Validate a list of words using the data rules already defined.
    pub fn validate_words(&self, words: Vec<String>) -> PyResult<Vec<RawMetadataGuardianResults>> {
        let words: Vec<&str> = words.iter().map(AsRef::as_ref).collect();
        let data_rules = self
            ._data_rules
            .validate_words(words)
            .map_err(PyMetadataGuardianError::from_raw)?;
        Ok(data_rules
            .iter()
            .map(|metadata_guardian_results| {
                RawMetadataGuardianResults::from(metadata_guardian_results)
            })
            .collect())
    }

    /// Validate the word using the data rules already defined.
    pub fn validate_word(&self, word: &str) -> PyResult<RawMetadataGuardianResults> {
        let metadata_guardian_result = self
            ._data_rules
            .validate_word(word)
            .map_err(PyMetadataGuardianError::from_raw)?;
        Ok(RawMetadataGuardianResults::from(&metadata_guardian_result))
    }

    /// Validate the file content using the data rules already defined.
    pub fn validate_file(&self, uri: &str) -> PyResult<Vec<RawMetadataGuardianResults>> {
        let data_rules = self
            ._data_rules
            .validate_file(uri)
            .map_err(PyMetadataGuardianError::from_raw)?;
        Ok(data_rules
            .iter()
            .map(|metadata_guardian_results| {
                RawMetadataGuardianResults::from(metadata_guardian_results)
            })
            .collect())
    }
}

#[pyfunction]
fn rust_core_version() -> &'static str {
    crate_version()
}

#[pymodule]
fn metadata_guardian(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(rust_core_version, m)?)?;
    m.add_class::<RawDataRule>()?;
    m.add_class::<RawDataRules>()?;
    m.add_class::<RawMetadataGuardianResults>()?;
    m.add("MetadataGuardianError", m.get_type())?;
    Ok(())
}
