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

  folds = []
  fold_sizes = [len(sim_vectors) / _FOLDS for _ in range(_FOLDS)]
  rest = len(sim_vectors) % _FOLDS
  for i in range(rest):
    fold_sizes[i] += 1
  indices = range(len(sim_vectors))
  rd.shuffle(indices)
  for i in range(_FOLDS):
    folds.append(indices[:fold_sizes[i]])
    indices = indices[fold_sizes[i]:]
  
  pred = lm.LogisticRegression()
  brier = []
  for index, fold in enumerate(folds):
    train_indices = set(range(len(sim_vectors))) - set(fold)
    train = [sim_vectors[i] for i in train_indices]
    train_target = [labels[i] for i in train_indices]
    pred.fit(train, train_target)
    test = np.array([list(sim_vectors[i]) for i in fold])
    test_target = [labels[i] for i in fold]
    test_pred = [p[1] for p in pred.predict_proba(test)]
    brier.append(1.0/len(test) * sum([(test_target[i] - test_pred[i]) ** 2 for i
        in range(len(test))]))
  print 'Brier score'
  print brier
  print sum(brier) / len(brier)

  data = np.array(sim_vectors)
  classes = np.array(labels)
  pred = lm.LogisticRegression()

  scores = cross_validation.cross_val_score(pred, data, classes, 'accuracy', 
      cv=5)
  print 'Accuracy'
  print scores
  print sum(scores) / len(scores)

  scores = cross_validation.cross_val_score(pred, data, classes, 'precision',
      cv=5)
  print 'Precision'
  print scores
  print sum(scores) / len(scores)

  scores = cross_validation.cross_val_score(pred, data, classes, 'recall', 
      cv=5)
  print 'Recall'
  print scores
  print sum(scores) / len(scores)

  scores = cross_validation.cross_val_score(pred, data, classes, 'f1', cv=5)
  print 'f1'
  print scores
  print sum(scores) / len(scores)



if __name__ == '__main__':
  cross_validate()
