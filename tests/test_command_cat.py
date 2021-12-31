from jrnlmd.jrnlmd import command_cat


def test_cat_empty_journal(journal, capsys):
    command_cat(journal)
    captured = capsys.readouterr()
    assert "" == captured.out


def test_cat_full_journal(journal_multidate, capsys):
    command_cat(journal_multidate)
    captured = capsys.readouterr()
    assert (
        """# 2021-11-01

## topic1

- first date note

# 2021-11-05

## topic1

- second date note

# 2021-11-10

## topic1

- third date note

"""
        == captured.out
    )


def test_cat_specific_date(journal_multidate, capsys):
    command_cat(journal_multidate, "2021-11-05:")
    captured = capsys.readouterr()
    assert (
        """# 2021-11-05

## topic1

- second date note

"""
        == captured.out
    )
