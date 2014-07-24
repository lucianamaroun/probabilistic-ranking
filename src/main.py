""" Main module of the probabilistic ranking of researchers system.

Run as follows, from the project folder:
$ python -m src.main
"""

from sklearn import linear_model
import os
import sys
import pickle as pkl
import time

import src.preprocessing as pre
import src.learning as lear
import src.partitioning as part
import src.auxiliary as aux
import src.modeling as mod
import src.prob_ranking as prob_rank


_TRAINING_FILE = 'data/training.dat'
_TEST_FILE = 'data/data.dat'
_ITERATIONS = 10
_PKL_PROBS = 'pkl/probs.pkl'
_PKL_REFS = 'pkl/refs.pkl'
_TIME_FILE = 'time/time%d.dat'


def probabilistic_disambiguation(print_time=False):
  """ Performs probabilistic disambiguation, including training fase, for a set
      of references.

  Observations:
    - The returned values are serialized since they are the same between
      different iterations.

  Args:
    print_time: whether time elapsed during this function execution should be
    printed.

  Returns:
    A blocked list of references to be ranked and a list of probabilistic
    matrices, one for each block.
  """
  time_i = time.time()
  
  if os.path.isfile(_PKL_PROBS) and os.path.isfile(_PKL_REFS):
    pkl_file = open(_PKL_REFS, 'r')
    references = pkl.load(pkl_file)
    pkl_file.close()
    pkl_file = open(_PKL_PROBS, 'r')
    probs = pkl.load(pkl_file)
    pkl_file.close()
  else:
    references, corpus = pre.get_input(_TRAINING_FILE, labeled=True)
    pred = lear.train(references, corpus)
    references, corpus = pre.get_input(_TEST_FILE)
    pkl_file = open(_PKL_REFS, 'w')
    probs = pkl.dump(references, pkl_file)
    pkl_file.close()
    probs = lear.test(references, corpus, pred)
    pkl_file = open(_PKL_PROBS, 'w')
    probs = pkl.dump(probs, pkl_file)
    pkl_file.close()
  
  time_f = time.time()
  if print_time:
    time_file = open(_TIME_FILE, 'a')
    print >> time_file, 'PROBABILISTIC_DISAMBIGUATION'
    print >> time_file, time_f - time_i
    time_file.close()
    
  return references, probs


def possible_worlds_sampling(references, probs, print_time=False):
  """ Samples the set of possible worlds, discriminating between a base case
      (most probable one) and alternative cases.

  Args:
    references: the blocked list of references to be ranked.
    probs: the list of probability matrices for each block.
  
  Returns:
    The base world and a list with alternative worlds.
  """
  time_i = time.time()
  
  base_world, alt_worlds = part.get_possible_worlds(references, probs,
      _ITERATIONS)

  time_f = time.time()
  if print_time:
    time_file = open(_TIME_FILE, 'a')
    print >> time_file, 'POSSIBLE_WORLDS_SAMPLING'
    print >> time_file, time_f - time_i
    time_file.close()
  
  return base_world, alt_worlds


def probabilistic_ranking(references, base_world, alt_worlds, print_time=False):
  """ Ranks the set of references and calculates uncertainties, composing a
      probabilistic ranking.

  Args:
    references: the blocked list of references to be ranked.
    base_world: the partitioning of blocks in base world.
    alt_worlds: a list of different partitionings in alternative worlds.

  Returns:
    A probabilistic ranking object.
  """
  time_i = time.time()
  
  ranking = prob_rank.rank(references, base_world, alt_worlds)

  time_f = time.time()
  if print_time:
    time_file = open(_TIME_FILE, 'a')
    print >> time_file, 'PROBABILISTIC_RANKING'
    print >> time_file, time_f - time_i
    print >> time_file, ''
    time_file.close()
  
  return ranking

def main(print_time=False):
  """ Main function that outputs a probabilistic ranking.

  Observations:
    - The input files are defined in the parameters of this document.

  Args:
    None.

  Retunrs:
    A ranking object with the probabilistic ranking.
  """
  references, probs = probabilistic_disambiguation(print_time=print_time)
  base_world, alt_worlds = possible_worlds_sampling(references, probs,
      print_time=print_time)
  ranking = probabilistic_ranking(references, base_world, alt_worlds,
      print_time=print_time)

  return ranking


if __name__ == '__main__':
  import sys
  print_time=False
  if (sys.argv[1] == '-t'): # display times
    _ITERATIONS = int(sys.argv[2])
    _TIME_FILE = _TIME_FILE % _ITERATIONS
    print_time = True
  else:
    _ITERATIONS = int(sys.argv[1])

  print main(print_time=print_time)
