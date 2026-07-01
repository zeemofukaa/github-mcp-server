import threading
import time
from pathlib import Path

from git_tools import (
    changed_files,
    git_diff,
    commit_changes,
    push_changes,
)
from gemini_client import ask_gemini


WATCHED_REPO = None
WATCH_MODE = "review"

watching = False


def watch_repository(repo_path, mode="review"):
    global WATCHED_REPO
    global WATCH_MODE
    global watching

    WATCHED_REPO = Path(repo_path)
    WATCH_MODE = mode

    if not watching:
        watching = True

        thread = threading.Thread(
            target=watch_loop,
            daemon=True,
        )

        thread.start()

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


def watch_loop():

    global watching

    while watching:

        repo, files = check_changes()

        if repo is not None and files:

            process_changes(repo)

        time.sleep(10)
        
def process_changes(repo):

    diff = git_diff(repo)

    if diff == "No changes.":
        return

    prompt = f"""
Return ONLY a git commit message.

One line.

Git diff:

{diff}
"""

    message = ask_gemini(prompt).strip()

    if message.startswith("[ERROR]"):
        return

    commit_changes(repo, message)

    if get_watch_mode() == "auto":
        push_changes(repo)