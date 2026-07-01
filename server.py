from gemini_client import ask_gemini
# Auto mode test
from github_tools import (
    clone_repo,
    list_files,
    read_file,
    find_file,
    search_code,
    detect_languages,
)

from git_tools import (
    repository_status,
    changed_files,
    git_diff,
    commit_changes,
    push_changes,
)

from watcher import (
    watch_repository,
    get_watched_repo,
    get_watch_mode,
    check_changes,
)

from dependency_graph import build_dependency_graph
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("GitHub MCP Server")


@mcp.tool()
def clone_repository(repo_url: str) -> str:
    """
    Clone a GitHub repository.
    """

    repo = clone_repo(repo_url)

    return f"Repository cloned to {repo}"
    
@mcp.tool()
def list_repository_files(repo_url: str) -> str:
    """
    List every source file inside a GitHub repository.
    """

    repo = clone_repo(repo_url)

    files = list_files(repo)

    if not files:
        return "Repository contains no files."

    return "\n".join(files)
    
@mcp.tool()
def read_repository_file(repo_url: str, filename: str) -> str:
    """
    Read a file from a GitHub repository.
    """

    repo = clone_repo(repo_url)

    matches = find_file(repo, filename)

    if len(matches) == 0:
        return f"{filename} not found."

    if len(matches) > 1:
        return (
            "Multiple files found:\n\n"
            + "\n".join(str(m.relative_to(repo)) for m in matches)
        )

    return read_file(
        repo,
        str(matches[0].relative_to(repo))
    )
    
@mcp.tool()
def find_symbol(repo_url: str, symbol: str) -> str:
    """
    Find where a class, function or variable is used.
    """

    repo = clone_repo(repo_url)

    results = search_code(repo, symbol)

    if not results:
        return f"No occurrences of '{symbol}' found."

    output = []

    for result in results:

        output.append(
            f"FILE: {result['path']}\n\n"
            f"{result['content'][:1000]}"
        )

    return "\n\n------------------------\n\n".join(output)

@mcp.tool()
def repository_languages(repo_url: str) -> str:
    """
    Detect the programming languages used in a repository.
    """

    repo = clone_repo(repo_url)

    languages = detect_languages(repo)

    return "\n".join(
        f"{k}: {v}"
        for k, v in languages.items()
    )
    
@mcp.tool()
def project_architecture(repo_url: str) -> str:
    """
    Generate the dependency graph of a Python project.
    """

    repo = clone_repo(repo_url)

    return build_dependency_graph(repo)

@mcp.tool()
def git_status(repo_url: str) -> str:
    repo = clone_repo(repo_url)
    return f"Repository path: {repo}\n\n{repository_status(repo)}"

@mcp.tool()
def list_changed_files(repo_url: str) -> str:
    """
    List all changed files in a repository.
    """

    repo = clone_repo(repo_url)

    files = changed_files(repo)

    if not files:
        return "No modified files."

    return "\n".join(files)

@mcp.tool()
def show_diff(repo_path: str) -> str:
    """
    Show the current Git diff.
    """

    return git_diff(repo_path)

@mcp.tool()
def commit_repository(repo_path: str, message: str) -> str:
    """
    Commit all staged and unstaged changes.
    """

    return commit_changes(repo_path, message)

@mcp.tool()
def push_repository(repo_path: str) -> str:
    """
    Push commits to origin.
    """

    return push_changes(repo_path)

@mcp.tool()
def watch_repo(repo_path: str, mode: str = "review") -> str:
    """
    Watch a repository.

    Modes:
    review
    auto
    notify
    """

    return watch_repository(repo_path, mode)

@mcp.tool()
def check_repository() -> str:

    repo, files = check_changes()

    if repo is None:
        return "No repository is being watched."

    if not files:
        return "No changes detected."

    return (
        "Changed files:\n\n"
        + "\n".join(files)
    )
    
@mcp.tool()
def review_changes() -> str:

    repo = get_watched_repo()

    if repo is None:
        return "No watched repository."

    diff = git_diff(repo)

    if diff == "No changes.":
        return diff

    prompt = f"""
Review this git diff.

Return:

1. Summary

2. Suggested commit message

Git diff:

{diff}
"""

    return ask_gemini(prompt)

@mcp.tool()
def auto_commit() -> str:

    repo = get_watched_repo()

    if repo is None:
        return "No watched repository."

    diff = git_diff(repo)

    if diff == "No changes.":
        return diff

    prompt = f"""
Generate ONLY a git commit message.

Git diff:

{diff}
"""

    message = ask_gemini(prompt).strip()

    if message.startswith("[ERROR]"):
        return message

    result = commit_changes(repo, message)

    if get_watch_mode() == "auto":
        result += "\n" + push_changes(repo)

    elif get_watch_mode() == "review":
        result += "\nWaiting for push confirmation."

    return result

@mcp.tool()
def watcher_status() -> str:

    repo = get_watched_repo()

    if repo is None:
        return "No repository being watched."

    return (
        f"Watching:\n"
        f"{repo}\n\n"
        f"Mode: {get_watch_mode()}"
    )

if __name__ == "__main__":
    mcp.run()