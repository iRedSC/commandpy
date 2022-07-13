from compy import Parser


def test_parse_single_arg():

    assert Parser().clean("hello") == ["hello"]
    assert Parser().clean("greeting") == ["greeting"]


def test_parse_multiple_args():

    assert Parser().clean("hello world") == ["hello", "world"]
    assert Parser().clean("what, is this?") == ["what,", "is", "this?"]


def test_parse_string():

    assert Parser().clean('hello "world that is amazing"') == [
        "hello",
        "world that is amazing",
    ]
    assert Parser().clean('hello " world that is amazing "') == [
        "hello",
        " world that is amazing ",
    ]
