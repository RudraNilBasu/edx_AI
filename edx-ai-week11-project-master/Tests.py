import unittest

from SentimentPredictor import SentimentPredictor
from driver_3 import imdb_data_preprocess


class Reporter:
    def write(self, msg):
        pass


class NullReporter(Reporter):
    def write(self, msg):
        print()


def generate_corpus():
    return []


class TestPredictorBuilderTests(unittest.TestCase):
    def test_can_create_from_default (self):
        sut = SentimentPredictor().build()
        self.assertIsNotNone(sut)

    def test_can_inject_console_reporter(self):
        sut = SentimentPredictor().with_reporter(NullReporter()).build()
        self.assertIsNotNone(sut)

    def test_can_run_on_default_test_data(self):
        sut = SentimentPredictor().with_reporter(NullReporter()).build()
        corpus = generate_corpus()
        sut.fit()
        results = [sut.predict(x) for x in corpus]
        self.assertIsNotNone(results)


class XformerTests(unittest.TestCase):
    def test_run (self):
        imdb_data_preprocess('./')
    def test_run_mixed (self):
        imdb_data_preprocess('./', mix=True)

