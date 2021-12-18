from jrnlmd.jrnlmd import cat_journal_since


def test_cat_journal_since(journal_multidate, capsys):
    cat_journal_since(journal_multidate, "2021-11-05")
    captured = capsys.readouterr()
    assert (
        """# 2021-11-05

## topic1

- second date note

# 2021-11-10

## topic1

- third date note

"""
        == captured.out
    )
