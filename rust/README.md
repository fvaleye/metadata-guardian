## Overview

Metadata Guardian is a Python package that provides an easy way to protect your data source by searching in its metadata.
By searching with regex and data rules, it will detect what you are looking to protect.
Using Rust, it makes blazing fast multi-regex matching.

## Usage

Using multiple regular expressions simultaneously with [regex](https://github.com/rust-lang/regex) and parrallelize it with [rayon](https://github.com/rayon-rs/rayon), this crate provides an easy way of creating the data rules for scanning the metadata.

## Rust Development

Install Rust:
```sh
curl https://sh.rustup.rs -sSf | sh -s -- -y
```

Build:
```sh
cargo build
```

Launch the tests:
```sh
cargo test
```
