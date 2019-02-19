import pytest

# coding=utf-8
from feedbackcontent.predict.preprocess import Preprocess

__preprocessor = None


@pytest.fixture(scope='module')
def fdt_setup(request):
    global __preprocessor
    stopwords = ['accordingly', 'this']
    __preprocessor = Preprocess('en', True, stopwords)

    def teardown():
        __preprocessor = None
    request.addfinalizer(teardown)


def assert_res(test_text, expected_res):
    actual_res = __preprocessor.process(test_text)
    assert(actual_res == expected_res)


def test_clear_html(fdt_setup):
    test_text = "<p>Hello, <a href='http://earth.google.com/'>world</a>!"
    expected_res = ['hello', 'world']
    assert_res(test_text, expected_res)


def test_remove_emojis(fdt_setup):
    test_text = u"😃 🙁..🙂🙃..🙄😠..😥 "
    expected_res = []
    assert_res(test_text, expected_res)


def test_remove_non_alpha(fdt_setup):
    test_text = 'non alpha222 tokens2'
    expected_res = [u'non']
    assert_res(test_text, expected_res)


def test_remove_stopwords(fdt_setup):
    test_text = 'accordingly remove this'
    # result is stemmed
    expected_res = ['remov']
    assert_res(test_text, expected_res)


def test_stem_tokens(fdt_setup):
    test_text = 'trees bees pages'
    expected_res = [u'tree', u'bee', u'page']
    assert_res(test_text, expected_res)
