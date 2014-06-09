import unittest

import kmedoids

class FourElementsTestCase(unittest.TestCase):

  def setUp(self):
    self.dist = [[0, 1, 0, 0],
                 [1, 0, 0, 0],
                 [0, 0, 0, 1],
                 [0, 0, 1, 0]]
    self.elements = range(4)
    self.medoids = [0, 2]

  def test_initial_medoids(self):
    truth_set = [[0, 1], [0, 2], [0, 3], [1, 2], [1, 3], [2, 3]]
    self.assertIn(kmedoids.initial_medoids(self.dist, 2, max_combinations=2), truth_set)

  def test_assign_medoids(self):
    truth = [0, 2, 2, 0]
    self.assertEqual(kmedoids.assign_medoids(self.dist, self.elements,
        self.medoids), truth)

  def test_calculate_cost(self):
    self.assertEqual(kmedoids.calculate_cost(self.dist, self.elements,
        0, kmedoids.assign_medoids(self.dist, self.elements,
        self.medoids)), 0)
    assoc_medoid = [0, 0, 3, 3]
    self.assertEqual(kmedoids.calculate_cost(self.dist, self.elements,
        0, assoc_medoid), 1)

  def test_update_medoids(self):
    medoids = [1, 2]
    assoc_medoid = [2, 1, 2, 2]
    converg, new_medoids = kmedoids.update_medoids(self.dist, self.elements,
        medoids, assoc_medoid)
    new_assoc_medoid = kmedoids.assign_medoids(self.dist, self.elements,
        new_medoids)
    self.assertEqual(converg, False)
    self.assertItemsEqual(new_medoids, [1, 0])
    self.assertEqual(kmedoids.calculate_cost(self.dist, self.elements, 0,
        new_assoc_medoid), 0)
    self.assertEqual(kmedoids.calculate_cost(self.dist, self.elements, 1,
        new_assoc_medoid), 0)

  def test_get_labels(self):
    truth_set = [[0, 1, 1, 0], [1, 0, 0, 1]]
    self.assertIn(kmedoids.get_labels([0, 2, 2, 0]), truth_set)

class TenElementsTestCase(unittest.TestCase):

  def setUp(self):
    self.dist = [[0, 1, 0, 0, 0, 1, 1, 1, 0, 0],
                 [1, 0, 0, 0, 0, 1, 1, 1, 1, 1],
                 [0, 0, 0, 1, 0, 0, 1, 1, 1, 1],
                 [0, 0, 1, 0, 0, 0, 1, 1, 0, 1],
                 [0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
                 [1, 1, 0, 0, 1, 0, 0, 0, 1, 0],
                 [1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
                 [1, 1, 1, 1, 1, 0, 0, 0, 0, 1],
                 [0, 1, 1, 0, 1, 1, 0, 0, 0, 0],
                 [0, 1, 1, 1, 1, 0, 0, 1, 0, 0]]
    self.elements = range(10)
    self.medoids = [1, 7]
    self.assoc_medoid = [1, 1, 1, 1, 1, 7, 7, 7, 7, 7]

  def test_assign_medoids(self):
    truth_set = [[1, 1, 1, 1, 1, 7, 7, 7, 7, 7],
                 [7, 1, 1, 1, 1, 7, 7, 7, 7, 7],
                 [1, 1, 1, 1, 1, 7, 7, 7, 7, 1],
                 [7, 1, 1, 1, 1, 7, 7, 7, 7, 1]]
    self.assertIn(kmedoids.assign_medoids(self.dist, self.elements,
        self.medoids), truth_set)

  def test_calculate_cost(self):
    self.assertEqual(kmedoids.calculate_cost(self.dist, self.elements,
        1, self.assoc_medoid), 1)

  def test_update_medoids(self):
    converg, new_medoids = kmedoids.update_medoids(self.dist, self.elements,
        self.medoids, self.assoc_medoid)
    new_assoc_medoid = kmedoids.assign_medoids(self.dist, self.elements,
        new_medoids)
    self.assertEqual(converg, False)
    self.assertItemsEqual(new_medoids, [4, 6])
    self.assertEqual(kmedoids.calculate_cost(self.dist, self.elements, 4,
        new_assoc_medoid), 0)
    self.assertEqual(kmedoids.calculate_cost(self.dist, self.elements, 6,
        new_assoc_medoid), 0)

  def test_get_labels(self):
    truth_set = [[0, 0, 0, 0, 0, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 0, 0, 0, 0, 0]]
    self.assertIn(kmedoids.get_labels(self.assoc_medoid), truth_set)

  def test_kmedoids(self):
    truth_set = [[0, 0, 0, 0, 0, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 1, 1, 1, 1, 1], [1, 0, 1, 1, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 1, 0, 1, 1], [1, 1, 1, 1, 1, 0, 0, 1, 0, 0],
        [0, 1, 0, 0, 0, 1, 1, 0, 1, 1], [1, 0, 1, 1, 1, 0, 0, 1, 0, 0]]
    self.assertIn(kmedoids.kmedoids(self.dist, 2), truth_set)


if __name__ == '__main__':
  unittest.main()
