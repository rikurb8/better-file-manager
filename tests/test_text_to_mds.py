from pathlib import Path
from unittest.mock import patch

import pytest

from better_file_manager.text_to_mds import (
    create_markdown_files,
    get_output_directory,
    parse_markdown_sections,
)

# Constants for test data
EXPECTED_SECTION_COUNT = 2
DEFAULT_OUTPUT_DIR = "markdown_docs"
CUSTOM_OUTPUT_DIR = "custom_dir"

TEST_CONTENT = """`test1.md`:
```markdown
# Test 1
Content 1
```

`test2.md`:
```markdown
# Test 2
Content 2
```"""

TEST_SECTIONS = [
    ("test1.md", "# Test 1\nContent 1"),
    ("test2.md", "# Test 2\nContent 2"),
]


def test_parse_markdown_sections():
    sections = parse_markdown_sections(TEST_CONTENT)
    assert len(sections) == EXPECTED_SECTION_COUNT
    assert sections[0] == TEST_SECTIONS[0]
    assert sections[1] == TEST_SECTIONS[1]


def test_parse_markdown_sections_empty():
    content = "No markdown sections here"
    sections = parse_markdown_sections(content)
    assert len(sections) == 0


@patch("builtins.input")
def test_get_output_directory_default(mock_input):
    mock_input.return_value = ""
    with patch("pathlib.Path.mkdir") as mock_mkdir:
        output_dir = get_output_directory()
        assert output_dir == Path(DEFAULT_OUTPUT_DIR)
        mock_mkdir.assert_called_once_with(exist_ok=True)


@patch("builtins.input")
def test_get_output_directory_custom(mock_input):
    mock_input.return_value = CUSTOM_OUTPUT_DIR
    with patch("pathlib.Path.mkdir") as mock_mkdir:
        output_dir = get_output_directory()
        assert output_dir == Path(CUSTOM_OUTPUT_DIR)
        mock_mkdir.assert_called_once_with(exist_ok=True)


def test_create_markdown_files(tmp_path):
    create_markdown_files(TEST_SECTIONS, tmp_path)

    # Verify files were created with correct content
    for filename, content in TEST_SECTIONS:
        file_path = tmp_path / filename
        assert file_path.exists()
        assert file_path.read_text() == content


if __name__ == "__main__":
    pytest.main([__file__])
