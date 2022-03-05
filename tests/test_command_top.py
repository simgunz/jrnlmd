from jrnlmd.jrnlmd import command_top


def test_cat_full_journal(journal_multidate, capsys):
    command_top(journal_multidate)
    captured = capsys.readouterr()
    assert (
        """topic1
topic2
"""
        == captured.out
    )
