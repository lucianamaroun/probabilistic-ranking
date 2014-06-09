from sklearn import linear_model as lm
from sklearn import cross_validation
from sklearn import metrics
import random as rd
import numpy as np

import src.main as main
import src.modeling as mod
import src.preprocessing as pre

_FOLDS = 5

def cross_validate():
  references, corpus = pre.get_input(main._TEST_FILE, labeled=True)
  sim_vectors, labels = mod.model(references, corpus, labeled=True)
  sim_vectors = sum(sim_vectors, [])
  data = []
  for vec in sim_vectors:
      data.append(list(vec))
  data = np.array(data)
  classes = np.array(labels)
  
  folds = []
  fold_sizes = [len(sim_vectors) / _FOLDS for _ in range(_FOLDS)]
  rest = len(sim_vectors) % _FOLDS
  for i in range(rest):
    fold_sizes[i] += 1
  available_indexes = range(len(sim_vectors))
  for i in range(_FOLDS):
    folds.append(rd.sample(available_indexes, fold_sizes[i]))
    for index in folds[-1]:
      available_indexes.remove(index)

  pred = lm.LogisticRegression()
  precision = []
  recall = []
  f1 = []
  print [len(f) for f in folds]
  for fold in folds:
    training = [d for i, d in enumerate(sim_vectors) if i not in fold]
    train_target = [c for i, c in enumerate(labels) if i not in fold]
    pred.fit(training, train_target)
    test = np.array([list(sim_vectors[i]) for i in fold])
    print test.shape
    test_target = np.array([labels[i] for i in fold])
    print test_target.shape
    test_pred = pred.predict(test)
    precision.append(metrics.precision_score(test_target, test_pred))
    recall.append(metrics.recall_score(test_target, test_pred))
    f1.append(metrics.f1_score(test_target, test_pred))
  scores = cross_validation.cross_val_score(pred, data, classes, cv=5)
  print scores
  print sum(scores) / len(scores)
  print precision
  print recall
  print f1

if __name__ == '__main__':
  cross_validate()
