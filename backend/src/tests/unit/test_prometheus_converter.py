"""Tests for the prometheus_converter module."""

from backend.src.utils.prometheus_converter import make_prometheus_conform


def test_make_prometheus_conform():
    """Test the make_prometheus_conform function."""
    # Test 1: Empty string (first if condition)
    try:
        make_prometheus_conform("")
    except ValueError as e:
        assert str(e) == "Input string must not be empty."
    else:
        assert False, "ValueError was not raised for an empty string."

    # Test 2: Non-empty string (first if condition not triggered)
    result = make_prometheus_conform("valid_string")
    assert result == "valid_string", f"Expected 'valid_string', got: {result}"

    # Test 3: String starting with a number (second if condition)
    result = make_prometheus_conform("123start_with_number")
    assert result == "_123start_with_number", f"Expected '_123start_with_number', got: {result}"

    # Test 4: Too long string (third if condition)
    long_string = "a" * 120
    result = make_prometheus_conform(long_string, max_length=100)
    assert len(result) == 100, f"Expected length 100, got: {len(result)}"
    assert result == "a" * 100, f"Expected 'a'*100, got: {result}"


# Run the tests
test_make_prometheus_conform()
print("All tests passed successfully!")
