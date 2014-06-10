""" Module for references partitioning into researchers' clusters. """

from sklearn.cluster.dbscan_ import dbscan
import numpy as np

from src.lib.kmedoids import kmedoids


def get_possible_worlds(references, probs, n_alternatives):
  """ Gets possible worlds divided into base and alternative partitionings.
  
  Observations:
    - The base world is obtained from DBScan algorithm on the complement
      of probabilities from logistic regression. The alternative worlds 
      are obtained from random experiments for all pair of references'
      probabilities and applying kmedoids with k defined from the base.

  Args:
    references: the list of references grouped in blocks.
    probs: a list with the probabilities matrices for each block.
    n_alternatives: the number of alternatives partitionings to be derived.

  Returns:
    A tuples (base_world, alternative_world), where each world is modeled as a
      list of list of integers, each coding a different cluster, grouped by
      blocks.
  """
  probability_matrices = get_probability_matrices(references, probs)
  base_partitioning = []
  alternative_partitionings = []
  k_block = []
  for pm in probability_matrices:
    distance_matrix = transform_distance_matrix(pm)
    b_part_block, k = get_base_partitioning(distance_matrix)
    k_block.append(k)
    base_partitioning.append(b_part_block)
  for _ in range(n_alternatives):
    alternative_partitioning = []
    for i, pm in enumerate(probability_matrices):
      distance_matrix = transform_distance_matrix(pm)
      a_part_block = get_alternative_partitioning(distance_matrix, k_block[i])
      alternative_partitioning.append(a_part_block)
    alternative_partitionings.append(alternative_partitioning)
  return base_partitioning, alternative_partitionings


def get_probability_matrices(references, probs):
  """ Derives probability matrices from a list of probabilities.

  Observations:
    - The probabilities as well as the matrices are divided by block.
    - The order of the probabilities in each block is predefined, being sorted
      by lexicographical order on the tuple of references' ids.
  
  Args:
    references: the list of reference objects grouped by block.
    probs: the list of probabilities of correferences for pair of references.

  Returns:
    A list with matrices (three-depth nested lists), containing the
      probability of correference for each block.
  """
  prob_matrices = []
  for i in range(len(references)):
    block = references[i]
    prob_matrix = [len(block) * [1.] for reference in block]
    pair_count = 0
    for j in range(len(block)):
      reference_a = block[j]
      for k in range(j+1, len(block)):
        prob_matrix[j][k] = probs[i][pair_count]
        prob_matrix[k][j] = probs[i][pair_count]
        pair_count += 1
    prob_matrices.append(prob_matrix)
  return prob_matrices


def transform_distance_matrix(similarity_matrix):
  """ Transforms a similarity matrix into a distance one by applying the
  complement of each cell.

  Args:
    similarity_matrix: a list of lists with the similarities.

  Returns:
    A list of lists with representing the distance matrix.
  """
  distance_matrix = [[0.0] * len(row) for row in similarity_matrix]
  for i in range(len(similarity_matrix)):
    for j in range(len(similarity_matrix[i])):
      distance_matrix[i][j] = 1 - similarity_matrix[i][j]
  return distance_matrix


def get_base_partitioning(distance_matrix):
  """ Gets the base partitioning from the distance matrix using DBScan
    algorithm.

  Args:
    distance_matrix: a list of lists with the distances of references.

  Returns:
    A list of integers from 0 to k - 1, each one representing a block for the
      reference represented by the index.
  """
  labels = dbscan(np.array(distance_matrix), metric='precomputed', eps=0.15, 
      min_samples=2)
  next_label = max(labels[1]) + 1
  for i in range(len(labels[1])):
    if labels[1][i] == -1:
      labels[1][i] = next_label
      next_label += 1
  return labels[1].tolist(), number_of_clusters(labels[1])


def number_of_clusters(labels):
    """ Gets the number of cluster from a list of labels. """
    return len(set(labels))


def get_random_matrix(probability_matrix):
  """ Gets a random matrix for a probability matrix.

  Observations:
    - For each cell in the matrix, a bernoulli experiment is performed
      considering the respective probability.

  Args:
    probability_matrix: a list of lists with the probabilites of correference.
  
  Returns:
    A list of lists representing a random matrix, with a binary number in each
      cell.
  """
  random_matrix = [len(row) * [0.] for row in probability_matrix]
  for i in range(len(probability_matrix)):
    for j in range(len(probability_matrix[i])):
      random_matrix[i][j] = np.random.binomial(n=1, p=probability_matrix[i][j])
  return random_matrix


def get_alternative_partitioning(distance_matrix, k_clusters):
  """ Get an alternative partitioning from a distance matrix with given number
    of clusters, using kmedoids algorithm.

  Args:
    distance_matrix: a list of lists with the matrix of distances between
      references.
    k_clusters: the number of clusters.

  Returns:
    A list of integers, each represeting a differente cluster for the given
      reference coded by the index.
  """
  labels = kmedoids(distance_matrix, k_clusters)
  return labels
