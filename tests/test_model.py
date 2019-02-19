import os
import pytest
from random import randint

from random import random, randint, choice

import numpy as np
from faker import Faker

from feedbackcontent.predict.model import Loader, Model

__model = None
__generator = None

@pytest.fixture(scope='module')

def fdt_setup(request):
    global __model, __generator
    # create a temp model
    __generator = Faker()
    vocab = list(set(__generator.words(500)))
    model = {
        "vocab": vocab,
        "stop_words": list(set(__generator.words(10))),
        "intercept": [1],
        "idf_": [randint(1, 15) for i in range(len(vocab))],
        "lr": [random() for i in range(len(vocab))],
    }
    np.savez('/tmp/model', **model)

    __model = Loader('/tmp').load_model('model')

    def teardown():
        __model = None
        __generator = None
        # delete model file
        os.remove("/tmp/model.npz")
    request.addfinalizer(teardown)


def test_load_model(fdt_setup):
    pass

def test_tokenize(fdt_setup):
    text = __generator.paragraph()
    # ensure that no error is raised
    __model.tokenize(text)

def test_predict(fdt_setup):
    text = __generator.paragraph()
    result = __model.predict(text)
    assert((len(result) == 1 and
            result[0] >= 0 and
            result[0] <= 1))