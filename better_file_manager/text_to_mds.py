import re
import sys
from pathlib import Path


def get_output_directory() -> Path:
    """
    Ask user for output directory name, suggesting a default.
    Returns Path object for the chosen directory.
    """
    default_dir = "markdown_docs"
    print(
        f"\nEnter directory name for markdown files [default: {default_dir}]: ",
        end="",
        flush=True,
    )
    dir_name = input().strip()

    # Use default if user just pressed enter
    if not dir_name:
        dir_name = default_dir

    # Create directory path
    dir_path = Path(dir_name)

    # Create directory if it doesn't exist
    dir_path.mkdir(exist_ok=True)

    return dir_path


def parse_markdown_sections(content: str) -> list[tuple[str, str]]:
    """
    Parse input string to extract filename and content pairs.
    Expected format: Content with embedded filenames marked by `filename.md`:
    Returns list of (filename, content) tuples.
    """
    # Split content into sections based on markdown filename indicators
    sections = []

    # Updated regex pattern to match `filename.md`:
    pattern = r"`([^`]+\.md)`:\s*```markdown(.*?)```"

    # Find all matches in the content using regex
    matches = re.finditer(pattern, content, re.DOTALL)

    for match in matches:
        filename = match.group(1)
        content = match.group(2).strip()
        sections.append((filename, content))

    return sections


def create_markdown_files(sections: list[tuple[str, str]], output_dir: Path) -> None:
    """Create markdown files from the parsed sections in the specified directory."""
    for filename, content in sections:
        # Create file in the specified directory
        file_path = output_dir / filename

        # Write content to file
        file_path.write_text(content)
        print(f"Created file: {file_path}")


def main() -> None:
    """
    Main function that reads input and creates markdown files.
    Input format example:
    `example1.md`:
    ```markdown
    Content for first file
    ```
    `example2.md`:
    ```markdown
    Content for second file
    ```
    """
    print("Paste your markdown content (press Ctrl+D when finished):")

    try:
        # Read all input until EOF (Ctrl+D)
        content = sys.stdin.read()

        # Parse sections
        sections = parse_markdown_sections(content)

        if not sections:
            print("No valid markdown sections found in input.")
            return

        # Get output directory from user
        output_dir = get_output_directory()

        # Create files in the specified directory
        create_markdown_files(sections, output_dir)

        print(f"\nAll files created in directory: {output_dir}")

    except KeyboardInterrupt:
        print("\nOperation cancelled.")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
