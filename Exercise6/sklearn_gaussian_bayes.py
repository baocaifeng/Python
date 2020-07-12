from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score

# see README.txt
# map string to value first, generate dataset
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
      [3, 71, 80, 1]
    ]
y = [0, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0]

nv = GaussianNB() # create a classifier
nv.fit(X,y) # fitting the data

GaussianNB(priors=None, var_smoothing=1e-09)

y_pred = nv.predict(X) # store the prediction data
acc = accuracy_score(y, y_pred) # calculate the accuracy

print(acc)

