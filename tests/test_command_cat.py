from jrnlmd.jrnlmd import command_cat


def test_cat_empty_journal(journal, capsys):
    command_cat(journal)
    captured = capsys.readouterr()
    assert "" == captured.out


def test_cat_full_journal(dummy_journal, capsys):
    command_cat(dummy_journal)
    captured = capsys.readouterr()
    assert (
        """# 2021-11-12

## topic1

- a note
- second bullet

"""
        == captured.out
    )
