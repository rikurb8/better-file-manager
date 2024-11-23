import logging
import signal
import sys
import time
from pathlib import Path
from typing import Any, NoReturn

from watchdog.events import FileSystemEvent, FileSystemEventHandler
from watchdog.observers import Observer

# Type alias for Observer
type WatchdogObserver = Any

# Configure logging with more detailed format
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("file_changes.log"), logging.StreamHandler()],
)


class FileChangeHandler(FileSystemEventHandler):
    """Handler for file system events."""

    def __init__(self) -> None:
        super().__init__()
        self.last_event_time = 0.0
        self.debounce_seconds = 0.1  # Debounce window to avoid duplicate events
        # Define patterns to ignore
        self.ignored_patterns = [
            str(Path.home() / "Library"),  # Ignore macOS Library folder
        ]

    def _should_handle_event(self, event: FileSystemEvent) -> bool:
        """
        Determine if an event should be handled based on debouncing and filters.
        """
        current_time = time.time()

        # Basic debouncing
        if current_time - self.last_event_time < self.debounce_seconds:
            return False

        # Update last event time
        self.last_event_time = current_time

        # Skip hidden files and directories
        if any(part.startswith(".") for part in Path(str(event.src_path)).parts):
            return False

        # Skip common temp files
        if str(event.src_path).endswith(("~", ".tmp", ".temp")):
            return False

        # Skip ignored patterns
        for pattern in self.ignored_patterns:
            if str(event.src_path).startswith(pattern):
                return False

        return True

    def on_created(self, event: FileSystemEvent) -> None:
        """Called when a file or directory is created."""
        if not event.is_directory and self._should_handle_event(event):
            logging.info(f"Created: {event.src_path!s}")

    def on_modified(self, event: FileSystemEvent) -> None:
        """Called when a file or directory is modified."""
        if not event.is_directory and self._should_handle_event(event):
            logging.info(f"Modified: {event.src_path!s}")

    def on_deleted(self, event: FileSystemEvent) -> None:
        """Called when a file or directory is deleted."""
        if not event.is_directory and self._should_handle_event(event):
            logging.info(f"Deleted: {event.src_path!s}")

    def on_moved(self, event: FileSystemEvent) -> None:
        """Called when a file or directory is moved or renamed."""
        if not event.is_directory and self._should_handle_event(event):
            logging.info(
                f"Moved/Renamed: from {event.src_path!s} to {event.dest_path!s}"
            )


class FileWatcher:
    """File system watcher class."""

    def __init__(self, path: Path) -> None:
        self.path = path
        self.observer: WatchdogObserver | None = None
        self.running = False

        # Set up signal handlers
        signal.signal(signal.SIGINT, self.handle_signal)
        signal.signal(signal.SIGTERM, self.handle_signal)

    def start(self) -> None:
        """Start watching the file system."""
        if self.running:
            return

        try:
            self.observer = Observer()
            event_handler = FileChangeHandler()
            self.observer.schedule(event_handler, str(self.path), recursive=True)
            self.observer.start()
            self.running = True

            logging.info(f"Started watching directory: {self.path}")

            # In production, this keeps the watcher running
            # In tests, this section can be skipped
            if not self._is_test_environment():
                while self.running:
                    time.sleep(1)

        except Exception as e:
            logging.error(f"Error occurred: {e}")
            self.stop()
            raise

    def stop(self) -> None:
        """Stop watching the file system."""
        if not self.running:
            return

        self.running = False
        if self.observer:
            self.observer.stop()
            self.observer.join()
            self.observer = None
            logging.info("Stopped watching directory")

    def handle_signal(self, signum: int, frame: Any) -> NoReturn:
        """Handle system signals."""
        logging.info(f"Received signal {signum}, shutting down...")
        self.stop()
        sys.exit(0)

    def _is_test_environment(self) -> bool:
        """Check if we're running in a test environment."""
        return "pytest" in sys.modules


def main() -> None:
    """Main entry point."""
    try:
        home_dir = Path.home()
        watcher = FileWatcher(home_dir)
        watcher.start()
    except Exception as e:
        logging.error(f"Failed to start file watcher: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
