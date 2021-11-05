extern crate pyo3;

use metadata_guardian::DataRules;
use pyo3::create_exception;
use pyo3::exceptions::PyException;
use pyo3::prelude::*;

create_exception!(metadata_guardian, PyMetadataGuardianError, PyException);

/// Python Metadata Guardian Errors.
impl PyMetadataGuardianError {
    /// Errors from the MetadataGuardian crate
    fn from_raw(err: metadata_guardian::MetadataGuardianError) -> pyo3::PyErr {
        PyMetadataGuardianError::new_err(err.to_string())
    }
}

/// Raw Data Rules for Python binding.
#[pyclass]
struct RawDataRules {
    /// Data rules used by the Metadata Guardian.
    _data_rules: metadata_guardian::DataRules,
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
impl<'a> From<&metadata_guardian::MetadataGuardianResults<'a>> for RawMetadataGuardianResults {
    fn from(
        metadata_guardian_results: &metadata_guardian::MetadataGuardianResults,
    ) -> RawMetadataGuardianResults {
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
impl RawDataRules {
    /// Create a new Raw Data Rules instance
    #[new]
    fn new(path: &str) -> PyResult<Self> {
        let data_rules = DataRules::new(path).map_err(PyMetadataGuardianError::from_raw)?;
        Ok(RawDataRules {
            _data_rules: data_rules,
        })
    }

    /// Validate a list of words using the data rules already defined.
    pub fn validate_words(&self, words: Vec<&str>) -> PyResult<Vec<RawMetadataGuardianResults>> {
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
    metadata_guardian::crate_version()
}

#[pymodule]
fn metadata_guardian(py: Python, module: &PyModule) -> PyResult<()> {
    env_logger::Builder::from_env(env_logger::Env::default().default_filter_or("warn")).init();
    module.add_function(pyo3::wrap_pyfunction!(rust_core_version, module)?)?;
    module.add_class::<RawDataRules>()?;
    module.add_class::<RawMetadataGuardianResults>()?;
    module.add(
        "MetadataGuardianError",
        py.get_type::<PyMetadataGuardianError>(),
    )?;
    Ok(())
}
