Metadata Guardian
=================

[![PyPI](https://img.shields.io/pypi/v/metadata_guardian.svg?style=flat-square)](https://pypi.org/project/metadata-guardian/)
[![userdoc](https://img.shields.io/badge/docs-user-blue)](https://fvaleye.github.io/metadata-guardian/python/)
[![apidoc](https://img.shields.io/badge/docs-api-blue)](https://fvaleye.github.io/metadata-guardian/python/api_reference.html)

## Overview

Metadata Guardian is a Python package that provides an easy way to protect your data sources by searching its metadata.
By searching with data rules, it will detect what you are looking to protect.
Using Rust, it makes blazing fast multi-regex matching.

## Usage

Benefit from data sources available of the Python ecosystem while Rust provides fast multi-regex processing with [regex](https://github.com/rust-lang/regex) and parallelizes the process with [rayon](https://github.com/rayon-rs/rayon).

## Data Rules
- [PII](https://github.com/fvaleye/metadata-guardian/blob/main/python/metadata_guardian/rules/pii_rules.yaml)
- [INCLUSION](https://github.com/fvaleye/metadata-guardian/blob/main/python/metadata_guardian/rules/inclusion_rules.yaml)

## Python Development

Install virtualenv:
```sh
make setup-venv
```

Development mode with the library installed in virtualenv:
```sh
make develop
```

Launch the tests:
```sh
make unit-test
```

Format and Runs checks:
```sh
make format
make check-rust
make check-python
```

Build the documentation locally:
```sh
make build-documentation
```
