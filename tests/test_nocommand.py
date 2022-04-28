from click.testing import CliRunner

from jrnlmd import jrnlmd


def test_nocommand_and_no_arguments_invoke_cat(mocker, journal_multidate_file):
    mock_cat = mocker.patch("jrnlmd.jrnlmd.cat")
    runner = CliRunner()

    runner.invoke(jrnlmd.cli, ["-j", str(journal_multidate_file)])

    mock_cat.assert_called_with(filter_="")
