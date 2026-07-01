from pathlib import Path
from git_tools import changed_files

WATCHED_REPO = None
WATCH_MODE = "review"


def watch_repository(repo_path, mode="review"):
    global WATCHED_REPO
    global WATCH_MODE

    WATCHED_REPO = Path(repo_path)
    WATCH_MODE = mode

    return f"Watching {WATCHED_REPO} ({WATCH_MODE})"


def get_watched_repo():
    return WATCHED_REPO


def get_watch_mode():
    return WATCH_MODE


def check_changes():

    repo = get_watched_repo()

    if repo is None:
        return None, []

    files = changed_files(repo)

    return repo, files