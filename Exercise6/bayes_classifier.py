import numpy as np
from scipy.stats import norm

class Bayes_Classifier(object):

    def train (self, X, y):
        # Population mean and standard deviation
        self.classes = set(y)
        self.mean = np.mean(X, axis=0)
        self.std = np.std(X, axis=0)

        # Class mean and standard deviation
        self.c_mean = np.zeros((len(self.classes), X.shape[1]))
        self.c_std = np.zeros((len(self.classes), X.shape[1]))
        self.prior = np.zeros((len(self.classes),))

        for c in self.classes:
            indices = np.where(y == c)
            self.prior[c] = indices[0].shape[0] / float(y.shape[0])
            self.c_mean[c] = np.mean(X[indices], axis=0)
            self.c_std[c] = np.std(X[indices], axis=0)

        return

    def predict (self, X):
        p = []
        for obs in X:
            tiled = np.repeat([obs], len(self.classes), axis=0)
            # Probability of observation in population
            evidence = norm.pdf((self.mean - obs) / self.std)
            evidence = np.prod(evidence)
            # Probability of observation in each class
            likelihood = norm.pdf((tiled - self.c_mean) / self.c_std)
            likelihood = np.prod(likelihood, axis=1)
            # Probability of each class given observation
            posterior = self.prior * likelihood / evidence
            p.append(np.argmax(posterior))

        return p

if __name__ == "__main__":

    # data, see README.txt
    X = [ [1, 85, 85, 0],
      [1, 80, 90, 1],
      [2, 83, 78, 0],
      [3, 70, 96, 0],
      [3, 68, 80, 0],
      [3, 65, 70, 1],
      [2, 64, 65, 1],
      [1, 72, 95, 0],
      [1, 69, 70, 0],
      [3, 75, 80, 0],
      [1, 75, 70, 1],
      [2, 72, 90, 1],
      [2, 81, 75, 0],
      [3, 71, 80, 1]]

    y = [0, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0]

    y = np.array(y)
    X = np.array(X)

    # Train and predict
    model = Bayes_Classifier()
    model.train(X, y)
    p = model.predict(X)
    
    print("---{ X }---{ y }---{ y predict }---")
    for x, prediction, actual in zip(X, p, y):
        print(x, actual, prediction)
        pass