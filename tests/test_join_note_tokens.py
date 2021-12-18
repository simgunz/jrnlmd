from jrnlmd.jrnlmd import join_notes_tokens


def test_join_notes_tokens():
    notes_tokens = [["word1"], ["word2", "word3"]]
    result = join_notes_tokens(notes_tokens)
    assert "- word1\n- word2 word3\n" == result
