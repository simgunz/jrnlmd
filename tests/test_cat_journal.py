from jrnlmd.jrnlmd import cat_journal


def test_cat_empty_journal(journal, capsys):
    cat_journal(journal)
    captured = capsys.readouterr()
    assert "" == captured.out


def test_cat_full_journal(dummy_journal, capsys):
    cat_journal(dummy_journal)
    captured = capsys.readouterr()
    assert (
        """# 2021-11-12

## topic1

- a note
- second bullet

"""
        == captured.out
    )
