use metadata_guardian::metadata_guardian::{DataRule, DataRules};
use std::path::PathBuf;

#[test]
fn test_validate_word_with_pii_should_not_contain_results() {
    let mut path = PathBuf::from(env!("CARGO_MANIFEST_DIR"));
    path.push("tests");
    path.push("resources");
    path.push("pii_rules.yaml");
    let data_guardian = DataRules::new(&path.into_os_string().into_string().unwrap()).unwrap();
    let content = "no pii";
    let category = "PII";
    let result = data_guardian.validate_word(content).unwrap();
    assert_eq!(result.category, category);
    assert_eq!(result.content, content);
    assert_eq!(result.data_rules.len(), 0);
}

#[test]
fn test_validate_word_with_pii_should_contains_results() {
    let mut path = PathBuf::from(env!("CARGO_MANIFEST_DIR"));
    path.push("tests");
    path.push("resources");
    path.push("pii_rules.yaml");
    let data_guardian = DataRules::new(&path.into_os_string().into_string().unwrap()).unwrap();
    let content = "test@gmail.com";
    let category = "PII";
    let result = data_guardian.validate_word(content).unwrap();
    let data_rules = vec![DataRule {
        pattern: "([a-z0-9!#$%&'*+/=?^_`{|.}~-]+@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?)".to_string(),
        documentation: "The email is a personal identifiable information.\n".to_string(),
        rule_name: "email content".to_string(),
    }];
    assert_eq!(result.category, category);
    assert_eq!(result.content, content);
    assert_eq!(result.data_rules[0], &data_rules[0]);
}

#[test]
fn test_validate_word_with_inclusion_should_contains_results() {
    let mut path = PathBuf::from(env!("CARGO_MANIFEST_DIR"));
    path.push("tests");
    path.push("resources");
    path.push("inclusion_rules.yaml");
    let data_guardian = DataRules::new(&path.into_os_string().into_string().unwrap()).unwrap();
    let content = "master";
    let category = "INCLUSION";
    let result = data_guardian.validate_word(content).unwrap();
    let data_rules = vec![DataRule {
        pattern: "\\b(slave|master|mastership)\\b".to_string(),
        documentation: "\"Master–slave\" is an offensive and exclusionary metaphor that cannot be detached from American\nhistory. Prefer describing a hierarchical relationship between nodes more precisely. Prefer using\nleader/follower, primary/replica or primary/standby.\n".to_string(),
        rule_name: "master".to_string(),
    }];
    assert_eq!(result.category, category);
    assert_eq!(result.content, content);
    assert_eq!(result.data_rules[0], &data_rules[0]);
}

#[test]
fn test_validate_words_with_inclusion_should_contains_results() {
    let mut path = PathBuf::from(env!("CARGO_MANIFEST_DIR"));
    path.push("tests");
    path.push("resources");
    path.push("inclusion_rules.yaml");
    let data_guardian = DataRules::new(&path.into_os_string().into_string().unwrap()).unwrap();
    let content = vec!["no error", "no error 2", "master"];
    let category = "INCLUSION";
    let results = data_guardian.validate_words(content).unwrap();
    let data_rules = vec![DataRule {
        pattern: "\\b(slave|master|mastership)\\b".to_string(),
        documentation: "\"Master–slave\" is an offensive and exclusionary metaphor that cannot be detached from American\nhistory. Prefer describing a hierarchical relationship between nodes more precisely. Prefer using\nleader/follower, primary/replica or primary/standby.\n".to_string(),
        rule_name: "master".to_string(),
    }];
    assert_eq!(results.len(), 1);
    let result = &results[0];
    assert_eq!(result.category, category);
    assert_eq!(result.content, "master");
    assert_eq!(result.data_rules[0], &data_rules[0]);
}

#[test]
fn test_validate_file_with_inclusion_should_contains_results() {
    let mut path = PathBuf::from(env!("CARGO_MANIFEST_DIR"));
    path.push("tests");
    path.push("resources");
    path.push("inclusion_rules.yaml");
    let data_guardian = DataRules::new(&path.into_os_string().into_string().unwrap()).unwrap();
    let mut file = PathBuf::from(env!("CARGO_MANIFEST_DIR"));
    file.push("tests");
    file.push("resources");
    file.push("inclusion_violations.txt");
    let category = "INCLUSION";
    let path = file.into_os_string().into_string().unwrap();
    let results = data_guardian.validate_file(&path).unwrap();
    let data_rules = vec![DataRule {
        pattern: "\\b(slave|master|mastership)\\b".to_string(),
        documentation: "\"Master–slave\" is an offensive and exclusionary metaphor that cannot be detached from American\nhistory. Prefer describing a hierarchical relationship between nodes more precisely. Prefer using\nleader/follower, primary/replica or primary/standby.\n".to_string(),
        rule_name: "master".to_string(),
    }];
    assert_eq!(results.len(), 1);
    let result = &results[0];
    assert_eq!(result.category, category);
    assert_eq!(
        result.content,
        "unpaid and unfree workers. Any particular slave may fulfill one, several, or"
    );
    assert_eq!(result.data_rules[0], &data_rules[0]);
}
