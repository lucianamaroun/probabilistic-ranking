""" Unit testing for the partitioning module.

    Run in the project folder as follows:
    python -m test.test_partitioning
"""

import unittest

from src import learning as lear
from src import modeling as mod
from src import partitioning as part
from src import preprocessing as pre
from test.test_cases import SampleTestCase

class SampleTestCasePartitioning(SampleTestCase):
  """ Using the sample test case for testing the partitioning module. """

  def test_get_probability_matrix(self):
    """ Tests the get_probability_matrix function. """
    references, corpus = pre.get_input(self.testfilename, labeled=True)
    references = [references[0], references[1], references[3]] + \
        [references[2] + references[4] + references[5]]
    pred = lear.training(references, corpus)
    probs = lear.testing(references, corpus, pred)
    self.assertEqual(part.get_probability_matrices(references, probs),[
        [[1.0, 0.89441830645266462, 0.95097107828998639],
         [0.89441830645266462, 1.0, 0.97565300931621723],
         [0.95097107828998639, 0.97565300931621723, 1.0]],
        [[1.0, 0.73429831405564638],
         [0.73429831405564638, 1.0]],
        [[1.0, 0.60153464586560224],
         [0.60153464586560224, 1.0]],
        [[1.0, 0.4067916074419064, 0.4067916074419064],
         [0.4067916074419064, 1.0, 0.4067916074419064],
         [0.4067916074419064, 0.4067916074419064, 1.0]]])

  def test_transform_distance_matrix(self):
    """ Tests the transform_distance_matrix function. """
    self.assertEqual([[round(el, 1) for el in row] for row in 
      part.transform_distance_matrix(
      [[0.0, 0.1, 0.7], [1.0, 0.3, 0.4], [0.5, 0.6, 0.8]])],
      [[1.0, 0.9, 0.3], [0.0, 0.7, 0.6], [0.5, 0.4, 0.2]])

  def test_get_base_partitioning(self):
    """ Tests the get_base_partitioning function. """
    references, corpus = pre.get_input(self.testfilename, labeled=True)
    references = [references[0], references[1], references[3]] + \
        [references[2] + references[4] + references[5]]
    pred = lear.training(references, corpus)
    probs = lear.testing(references, corpus, pred)
    matrices = part.get_probability_matrices(references, probs)
    distances = [part.transform_distance_matrix(matrix) for matrix in matrices]
    self.assertEqual(part.get_base_partitioning(distances[0]), ([0, 0, 0], 1))

  def test_number_of_clusters(self):
    """ Tests the number_of_clusters function. 
    
    Observations:
      - This is a syntax test. The random matrix should have either 0 or 1
        value.
    """
    self.assertEqual(part.number_of_clusters([0, 1, 2, 3, 2, 1, -1, -1, 0]), 6)

  def test_get_random_matrix(self):
    """ Tests the get_random_matrix function."""
    similarity_matrix = \
       [[1.0, 0.89441830645266462, 0.95097107828998639],
        [0.89441830645266462, 1.0, 0.97565300931621723],
        [0.95097107828998639, 0.97565300931621723, 1.0]]
    random_matrix = part.get_random_matrix(similarity_matrix)
    for row in random_matrix:
      for element in row:
        self.assertTrue(element == 0 or element == 1)

  def test_get_alternative_partitioning(self):
    """ Tests the get_alternative_partitioning function. """
    distance = \
        [[0, 1, 1],
         [1, 0, 0],
         [1, 0, 0]]
    self.assertIn(part.get_alternative_partitioning(distance, 2), [[0, 1, 1],
      [1, 0, 0]])

if __name__ == '__main__':
  unittest.main()      
