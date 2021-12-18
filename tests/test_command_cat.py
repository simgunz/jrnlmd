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


def test_cat_specific_date(journal_multidate, capsys):
    command_cat(journal_multidate, "2021-11-05")
    captured = capsys.readouterr()
    assert (
        """# 2021-11-05

## topic1

- second date note

"""
        == captured.out
    )
