import pytest

from metadata_guardian import metadata_guardian as native


def test_native_module_exports_exception_type():
    assert isinstance(native.MetadataGuardianError, type)
    assert issubclass(native.MetadataGuardianError, Exception)


def test_invalid_regex_raises_metadata_guardian_error():
    invalid_rule = native.RawDataRule("unclosed", "(", "invalid pattern")
    with pytest.raises(native.MetadataGuardianError):
        native.RawDataRules("category", [invalid_rule])
