import json
from pathlib import Path

MEMORY_FILE = Path("memory.json")


def load_memory():
    if MEMORY_FILE.exists():
        return json.loads(MEMORY_FILE.read_text())

    return {}


def save_memory(memory):
    MEMORY_FILE.write_text(
        json.dumps(memory, indent=4)
    )


def save_analysis(repo_url, analysis):

    memory = load_memory()

    memory[repo_url] = analysis

    save_memory(memory)


def recall_analysis(repo_url):

    memory = load_memory()

    return memory.get(repo_url)