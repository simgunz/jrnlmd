from jrnlmd.jrnlmd import main


def test_main_create_new_journal(journal):
    args = [
        "--journal",
        str(journal),
        "add",
        "12nov2021 topic1 . a note , second bullet",
    ]
    main(args)
    result = journal.read_text()
    assert (
        """# 2021-11-12

## topic1

- a note
- second bullet
"""
        == result
    )


def test_main_append_to_journal(dummy_journal):
    args2 = [
        "--journal",
        str(dummy_journal),
        "add",
        "12nov2021 topic2 . appended note",
    ]
    main(args2)
    result = dummy_journal.read_text()
    assert (
        """# 2021-11-12

## topic1

- a note
- second bullet

## topic2

- appended note
"""
        == result
    )
