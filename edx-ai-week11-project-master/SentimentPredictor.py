from sklearn.linear_model import SGDClassifier

from SentimentPredictorImpl import SentimentPredictorImpl


class SentimentPredictor:
    def __init__(self):
        self.reporter = None
        self.test_labels = None
        self.training_labels = None
        self.test_data = None
        self.training_data = None
        self.cls = SGDClassifier()

    def with_training_data(self, td):
        return self

    def with_training_labels(self, tl):
        return self

    def with_test_data(self, td):
        return self

    def with_test_labels(self, tl):
        return self

    def build(self) -> SentimentPredictorImpl:
        return SentimentPredictorImpl(
            self.training_data,
            self.test_data,
            self.training_labels,
            self.test_labels,
            self.reporter,
            self.cls)

    def with_reporter(self, reporter):
        self.reporter = reporter
        return self


