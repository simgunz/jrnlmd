from unittest import mock

import git

from jrnlmd.version_control import JournalGitVersionControl


def test_git_version_control_has_none_repo_if_journal_not_in_repo(journal_multidate):
    vc = JournalGitVersionControl(journal_multidate.file_path)

    assert vc._repo is None


def test_git_version_control_detect_repo(journal_multidate):
    git.Repo.init(str(journal_multidate.file_path.parent))

    vc = JournalGitVersionControl(journal_multidate.file_path)

    assert isinstance(vc._repo, git.Repo)


def test_git_commit(journal_multidate, capsys):
    git.Repo.init(str(journal_multidate.file_path.parent))
    vc = JournalGitVersionControl(journal_multidate.file_path)

    result = vc.commit("test commit")

    assert result is True


@mock.patch("jrnlmd.version_control.git.Repo.remote")
def test_git_push(mock_remote, journal_multidate):
    git.Repo.init(str(journal_multidate.file_path.parent))
    vc = JournalGitVersionControl(journal_multidate.file_path)

    result = vc.push("origin")

    assert result is True
    mock_remote.return_value.push.assert_called_once()
