import pytest
from click.testing import CliRunner

from jrnlmd import jrnlmd


@pytest.fixture()
def config_file(tmp_path):
    return tmp_path / "jrnlmdrc"


def test_journal_read_from_config_file(config_file, journal_multidate_file):
    config_file.write_text(
        f"""
journal = "{str(journal_multidate_file)}"
"""
    )
    runner = CliRunner()

    result = runner.invoke(jrnlmd.cli, ["--config", str(config_file), "cat"])

    assert (
        """# 2021-11-01

## topic2

- first date note

## topic1

- another note

# 2021-11-05

## topic1

- second date note

# 2021-11-10

## topic1

- third date note

"""
        == result.output
    )


def test_cat_option_read_from_config_file(config_file, journal_multidate_file):
    config_file.write_text(
        f"""
journal = "{str(journal_multidate_file)}"
[ cat ]
simplified = True
"""
    )
    runner = CliRunner()

    result = runner.invoke(
        jrnlmd.cli,
        [
            "--config",
            str(config_file),
            "cat",
            "topic1",
        ],
    )

    assert (
        """# topic1

## 2021-11-01

- another note

## 2021-11-05

- second date note

## 2021-11-10

- third date note

"""
        == result.output
    )


def test_cat_filter_read_from_config_file(config_file, journal_multidate_file):
    config_file.write_text(
        f"""
journal = "{str(journal_multidate_file)}"
[ cat ]
filter_ = "2021-11-10:"
"""
    )
    runner = CliRunner()

    result = runner.invoke(
        jrnlmd.cli,
        [
            "--config",
            str(config_file),
            "cat",
        ],
    )

    assert (
        result.output
        == """# 2021-11-10

## topic1

- third date note

"""
    )
