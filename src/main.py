""" Main module of the probabilistic ranking of researchers system.

Run as follows, from the project folder:
$ python -m src.main
"""

from sklearn import linear_model
import os
import sys
import pickle as pkl

import src.preprocessing as pre
import src.learning as lear
import src.partitioning as part
import src.auxiliary as aux
import src.modeling as mod
import src.prob_ranking as prob_rank


_TRAINING_FILE = 'data/training.dat'
_TEST_FILE = 'data/data.dat'
_LAB_COAUT_DIR = 'coaut_lab'
_COAUT_DIR = 'coaut'
_DUMP_DIR = 'dump'
_PRED_DUMP_FILE = 'logreg.pkl'
_ITERATIONS = 1


def prob_ranking():
  """ Main function that performs probabilistic ranking.

  Observations:
    - The input files are defined in the parameters of this document.

  Args:
    None.

  Retunrs:
    A ranking object with the probabilistic ranking.
  """  
  print 'Reading the training'
  references, corpus = pre.get_input(_TRAINING_FILE, labeled=True)
  print 'Learning the training'
  pred = lear.train(references, corpus)
  print pred.coef_
  print 'Reading the testing'
  references, corpus = pre.get_input(_TEST_FILE)
  print 'Fitting the test'
  probs = lear.test(references, corpus, pred)
  print 'Getting possible worlds'
  base_world, alt_worlds = part.get_possible_worlds(references, probs,
      _ITERATIONS)
  print 'Probabilistic ranking'
  ranking = prob_rank.rank(references, base_world, alt_worlds)
  return ranking


if __name__ == '__main__':
  print prob_ranking()
