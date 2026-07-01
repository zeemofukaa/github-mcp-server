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

def list_files(repo_path: Path):
    files = []

    for file in repo_path.rglob("*"):
        if file.is_file():
            try:
                relative = file.relative_to(repo_path)

                # Ignore git internals
                if ".git" not in relative.parts:
                    files.append(str(relative))

            except Exception:
                pass

    return sorted(files)

def detect_languages(repo_path: Path):

    languages = {}

    for file in repo_path.rglob("*"):

        if file.is_file():

            ext = file.suffix.lower()

            if ext:

                languages[ext] = languages.get(ext, 0) + 1

    return dict(
        sorted(
            languages.items(),
            key=lambda x: x[1],
            reverse=True,
        )
    )

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

def search_code(repo_path, keyword):

    matches = []

    for file in repo_path.rglob("*"):

        if not file.is_file():
            continue

        if ".git" in str(file):
            continue

        try:
            text = file.read_text(
                encoding="utf-8",
                errors="ignore"
            )

            if keyword.lower() in text.lower():

                matches.append({
                    "path": str(file.relative_to(repo_path)),
                    "content": text
                })

        except Exception:
            pass

    return matches