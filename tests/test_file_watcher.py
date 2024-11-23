from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from watchdog.events import FileSystemEvent

from better_file_manager.main import FileChangeHandler, FileWatcher

# Constants for test values
INITIAL_TIME = 0.0
DEBOUNCE_TIME = 0.1
LATER_TIME = 2.0


@patch("time.time")
def test_file_change_handler_init(mock_time):
    mock_time.return_value = INITIAL_TIME
    handler = FileChangeHandler()
    assert handler.last_event_time == INITIAL_TIME
    assert handler.debounce_seconds == DEBOUNCE_TIME
    assert len(handler.ignored_patterns) > 0


@patch("time.time")
def test_should_handle_event(mock_time):
    mock_time.return_value = INITIAL_TIME
    handler = FileChangeHandler()
    event = MagicMock(spec=FileSystemEvent)

    # Test hidden file
    event.src_path = ".hidden_file"
    assert not handler._should_handle_event(event)

    # Test temp file
    event.src_path = "file.tmp"
    assert not handler._should_handle_event(event)

    # Test normal file with sufficient time passed
    mock_time.return_value = LATER_TIME  # More than debounce_seconds
    event.src_path = "normal_file.txt"
    assert handler._should_handle_event(event)


def test_file_watcher_init():
    path = Path("/test/path")
    watcher = FileWatcher(path)
    assert watcher.path == path
    assert watcher.observer is None
    assert not watcher.running


@patch("better_file_manager.main.Observer")
def test_file_watcher_start_stop(mock_observer):
    path = Path("/test/path")
    watcher = FileWatcher(path)

    # Mock the observer's methods
    mock_observer_instance = mock_observer.return_value

    # Start the watcher in a way that allows us to check the running state
    watcher.observer = mock_observer_instance
    watcher.start()

    # Check that the observer was properly set up
    mock_observer_instance.schedule.assert_called_once()
    mock_observer_instance.start.assert_called_once()
    assert watcher.running

    # Test stop
    watcher.stop()
    mock_observer_instance.stop.assert_called_once()
    mock_observer_instance.join.assert_called_once()
    assert not watcher.running


if __name__ == "__main__":
    pytest.main([__file__])
