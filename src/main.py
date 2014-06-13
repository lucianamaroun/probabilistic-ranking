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
_ITERATIONS = 10


def prob_ranking():
  """ Main function that performs probabilistic ranking.

  Observations:
    - The input files are defined in the parameters of this document.

  Args:
    None.

  Retunrs:
    A ranking object with the probabilistic ranking.
  """  
  references, corpus = pre.get_input(_TRAINING_FILE, labeled=True)
  pred = lear.train(references, corpus)
  references, corpus = pre.get_input(_TEST_FILE)
  probs = lear.test(references, corpus, pred)
  base_world, alt_worlds = part.get_possible_worlds(references, probs,
      _ITERATIONS)
  ranking = prob_rank.rank(references, base_world, alt_worlds)
  return ranking


if __name__ == '__main__':
  import sys
  _ITERATIONS = int(sys.argv[1])

  print prob_ranking()
