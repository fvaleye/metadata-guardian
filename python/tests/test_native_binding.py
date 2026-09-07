import pytest

from metadata_guardian import metadata_guardian as native


def test_native_module_exports_exception_type():
    assert isinstance(native.MetadataGuardianError, type)
    assert issubclass(native.MetadataGuardianError, Exception)


def test_invalid_regex_raises_metadata_guardian_error():
    invalid_rule = native.RawDataRule("unclosed", "(", "invalid pattern")
    with pytest.raises(native.MetadataGuardianError):
        native.RawDataRules("category", [invalid_rule])


@pytest.mark.parametrize("content", [b"\xff", b"master\n\xff\nmaster\n"])
def test_invalid_utf8_file_raises_metadata_guardian_error(tmp_path, content):
    path = tmp_path / "invalid.txt"
    path.write_bytes(content)
    data_rules = native.RawDataRules(
        "category", [native.RawDataRule("master", "master", "test rule")]
    )

    with pytest.raises(native.MetadataGuardianError):
        data_rules.validate_file(str(path))
