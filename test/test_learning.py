""" Unit testing for the learning module.

    Run in the project folder as follows:
    python -m test.test_learning
"""

import unittest

from src import learning as lear
from src import modeling as mod
from src import preprocessing as pre
from test.test_cases import SampleTestCase

class SampleTestCaseLearning(SampleTestCase):
  """ Using the sample test case for testing the learning module. """

  def test_training(self):
    """ Tests the training phase. 
    
      Observations:
        - Considers that there is no error in the training, which is not
          always the case. However, it works for small inputs and is a
          reasonable approximation test.
    """
    references, corpus = pre.get_input(self.testfilename, labeled=True)
    references = [references[0], references[1], references[3]] + [references[2] 
        + references[4] + references[5]]
    pred = lear.training(references, corpus)
    sim_vectors, classes = mod.model(references, corpus, labeled=True)
    self.assertEqual(pred.predict(sum(sim_vectors, [])).tolist(), classes)

  def test_testing(self):
    """ Tests the test phase.

    Observations:
      - Considers that the error in the training set is zero, which is used in
        testing fase.
    """
    references, corpus = pre.get_input(self.testfilename, labeled=True)
    references = [references[0], references[1], references[3]] + [references[2] 
        + references[4] + references[5]]
    pred = lear.training(references, corpus)
    sim_vectors, classes = mod.model(references, corpus, labeled=True)
    self.assertEqual([round(prob) for prob in 
        sum(lear.testing(references, corpus, pred), [])], classes)


if __name__ == '__main__':
  unittest.main()
