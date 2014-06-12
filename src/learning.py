""" Module for learning the probability of correference. """

from src import modeling as mod
from sklearn import linear_model as lm


def train(references, corpus):
  """ Learns a logistic regression.
  
  Args:
    references: the list of references grouped in blocks.
    corpus: the corpus of names.

  Returns:
    A predictor represented by a logistic regression.
  """
  sim_vectors, classes = mod.model(references, corpus, labeled=True)
  pred = lm.LogisticRegression()
  pred.fit(sum(sim_vectors, []), classes)
  return pred


def test(references, corpus, pred):
  """ Applies the logistic regression to a set of references.

  Args:
    references: the list of references grouped in blocks.
    corpus: the corpus of names in the test.
    pred: the predictor object (from sklearn) with the logistic regression.

  Returns:
    A list with the probabilities of correference, i.e., of belonging to class 
      1, grouped in blocks. Each block contains the pair of references built in
      lexicographic ordering.
  """
  sim_vectors = mod.model(references, corpus)
  probs = []
  for block in sim_vectors:
    probs.append(pred.predict_proba(block))
  return [[prob[1] for prob in prob_group] for prob_group in probs]

