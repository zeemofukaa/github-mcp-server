from mcp.server.fastmcp import FastMCP

from github_tools import (
    clone_repo,
    read_file,
    find_file,
)

mcp = FastMCP("GitHub MCP Server")


@mcp.tool()
def clone_repository(repo_url: str) -> str:
    """
    Clone a GitHub repository.
    """

    repo = clone_repo(repo_url)

    return f"Repository cloned to {repo}"


if __name__ == "__main__":
    mcp.run()
    
@mcp.tool()
def explain_file(repo_url: str, filename: str) -> str:
    """
    Read a source file from a GitHub repository.
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

    code = read_file(repo, str(matches[0].relative_to(repo)))

    return code