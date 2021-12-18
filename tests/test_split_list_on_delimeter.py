from jrnlmd.jrnlmd import split_list_on_delimiter


def test_split_with_no_delimiter():
    tokens = ["word1", "word2", "word3"]
    result = split_list_on_delimiter(tokens, delimiter=".")
    assert (["word1", "word2", "word3"],) == result


def test_split_with_one_delimiter():
    tokens = ["word1", ".", "word2", "word3"]
    result = split_list_on_delimiter(tokens, delimiter=".")
    assert (["word1"], ["word2", "word3"]) == result
