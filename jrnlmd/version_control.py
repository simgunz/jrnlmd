import sys
from pathlib import Path

import git


class JournalGitVersionControl:
    def __init__(self, journal_path: Path):
        self._repo = None
        self._journal_path = str(journal_path)
        self._git_repo_dir = journal_path.parent
        try:
            self._repo = git.Repo(self._git_repo_dir, search_parent_directories=True)
        except git.InvalidGitRepositoryError:
            pass

    def commit(self, message: str) -> bool:
        if self._repo is None:
            print(
                f"ERROR: {self._git_repo_dir} is not a git repository. Skipping"
                " commit.",
                file=sys.stderr,
            )
            return False
        self._repo.index.add(self._journal_path)
        self._repo.index.commit(message)
        return True

    def push(self, remote_name: str) -> bool:
        push_status = False
        try:
            if self._repo is not None:
                self._repo.remote(name=remote_name).push()
                push_status = True
        except ValueError:
            pass
        if push_status is False:
            print("ERROR: remote repository not found. Skipping push.", file=sys.stderr)
        return push_status
