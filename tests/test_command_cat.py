from jrnlmd.jrnlmd import command_cat


def test_cat_new_journal_file(new_journal_file, capsys):
    command_cat(new_journal_file)
    captured = capsys.readouterr()
    assert "" == captured.out


def test_cat_full_journal(journal_multidate_file, capsys):
    command_cat(journal_multidate_file)
    captured = capsys.readouterr()
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
        == captured.out
    )


def test_cat_specific_date(journal_multidate_file, capsys):
    command_cat(journal_multidate_file, "2021-11-05:")
    captured = capsys.readouterr()
    assert (
        """# 2021-11-05

## topic1

- second date note

"""
        == captured.out
    )


def test_cat_specific_topic(journal_multidate_file, capsys):
    command_cat(journal_multidate_file, "topic2")
    captured = capsys.readouterr()
    assert (
        """# 2021-11-01

## topic2

- first date note

"""
        == captured.out
    )


def test_cat_specific_date_and_topic(journal_multidate_file, capsys):
    command_cat(journal_multidate_file, "1 11 2021: topic1")
    captured = capsys.readouterr()
    assert (
        """# 2021-11-01

## topic1

- another note

"""
        == captured.out
    )


def test_cat_specific_topic_simplified(journal_multidate_file, capsys):
    command_cat(journal_multidate_file, "topic1", simplified=True)
    captured = capsys.readouterr()
    assert (
        """# 2021-11-01

- another note

# 2021-11-05

- second date note

# 2021-11-10

- third date note

"""
        == captured.out
    )
