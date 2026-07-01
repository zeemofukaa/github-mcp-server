from git import Repo

def repository_status(repo_path):
    repo = Repo(repo_path)

    # Fetch latest information from remote
    repo.remotes.origin.fetch()

    branch = repo.active_branch

    tracking = branch.tracking_branch()

    if tracking is None:
        return "No remote tracking branch."

    ahead = sum(1 for _ in repo.iter_commits(f"{tracking}..{branch}"))
    behind = sum(1 for _ in repo.iter_commits(f"{branch}..{tracking}"))

    status = []

    if repo.is_dirty(untracked_files=True):
        status.append(repo.git.status())
    else:
        status.append("Working tree clean.")

    if ahead == 0 and behind == 0:
        status.append("Branch is up to date with origin.")

    elif ahead > 0 and behind == 0:
        status.append(f"Branch is ahead by {ahead} commit(s).")

    elif behind > 0 and ahead == 0:
        status.append(f"Branch is behind by {behind} commit(s).")

    else:
        status.append(
            f"Branch has diverged (ahead {ahead}, behind {behind})."
        )

    return "\n".join(status)


def changed_files(repo_path):
    """
    Return a list of modified, added, deleted and untracked files.
    """

    repo = Repo(repo_path)

    changed = []

    # Modified / deleted / staged
    for diff in repo.index.diff(None):
        changed.append(diff.a_path)

    # Untracked
    changed.extend(repo.untracked_files)

    return sorted(set(changed))