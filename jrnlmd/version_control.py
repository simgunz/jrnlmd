from pathlib import Path

import git


class JournalGitVersionControl:
    def __init__(self, journal_path: Path):
        self._repo = None
        git_repo_dir = journal_path.parent
        try:
            self._repo = git.Repo(git_repo_dir, search_parent_directories=True)
        except git.InvalidGitRepositoryError:
            pass
