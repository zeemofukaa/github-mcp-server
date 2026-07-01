from pathlib import Path
from git import Repo

BASE_DIR = Path(__file__).resolve().parent

REPOS_DIR = BASE_DIR / "repos"
REPOS_DIR.mkdir(parents=True, exist_ok=True)


def clone_repo(repo_url: str):
    repo_name = repo_url.rstrip("/").split("/")[-1]
    repo_path = REPOS_DIR / repo_name

    if repo_path.exists():
        print(f"Repository already exists: {repo_path}")
        return repo_path

    print(f"Cloning {repo_url}...")

    Repo.clone_from(repo_url, repo_path)

    print("Repository cloned.")

    return repo_path

def read_file(repo_path, file_path):

    path = repo_path / file_path

    if not path.exists():
        return None

    return path.read_text(
        encoding="utf-8",
        errors="ignore"
    )

def find_file(repo_path, filename):

    matches = []

    for file in repo_path.rglob("*"):

        if file.is_file():

            if file.name.lower() == filename.lower():

                matches.append(file)

    return matches