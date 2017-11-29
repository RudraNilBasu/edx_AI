from sklearn.linear_model import SGDClassifier

class SentimentPredictorImpl:
    def __init__(self, training_data, test_data, training_labels, test_labels, reporter, classifier:SGDClassifier):
        self.classifier = classifier
        self.reporter = reporter
        self.test_labels = test_labels
        self.training_labels = training_labels
        self.test_data = test_data
        self.training_data = training_data

    def fit(self):
        self.classifier.fit(self.training_data, self.training_labels)

    def predict(self, text):
        v = self.to_vector(text)
        pass

    def to_vector(self, text):
        pass