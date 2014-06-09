import itertools
import random

def kmedoids(dist, k, max_iterations=10000):
  """ Performs a kmedoids clustering from precomputed distances.

  Args:
    dist: a list of lists with the elements' distances.
    k: the number of clusters.
    max_iterations: the maximum number of iterations to try convergence.

  Returns:
    A list of labels, coding clusters from 0 to k - 1.
  """
  elements = range(len(dist))
  medoids = initial_medoids(dist, k)

  converg = False
  iterations = 0
  while not converg and iterations < max_iterations:
    iterations += 1
    assoc_medoid = assign_medoids(dist, elements, medoids)
    converg, medoids = update_medoids(dist, elements, medoids,
        assoc_medoid)
  return get_labels(assoc_medoid)


def hamming(vec_a, vec_b):
  """ Calculates hamming distance between a pair of vectors.
  
  Args:
    vec_a: a list with the first vector.
    vec_b: a list with the second vector.

  Returns:
    An integer with the distance of None if it is not defined.
  """
  if len(vec_a) != len(vec_b):
    return None
  dist = 0
  for i in range(len(vec_a)):
    if vec_a[i] != vec_b[i]:
      dist += 1
  return dist


def n_combinations(size, group):
  """ Calculates the number of combinations of <size> grouped in <group>
    amounts.

  Args:
    size: the size of elements.
    group: the size of the groups.

  Returns:
    An integer with the amount of combinations or infinity in case of overflow.
  """
  amount = 1
  for i in range(1, group + 1):
    prev_amount = amount
    amount *= size/i
    size -= 1
    if amount <= prev_amount:
      return float('inf')
  return amount


def initial_medoids(dist, k, max_combinations=100):
  """ Uses a heuristic to obtain the initial medoids.

  Observations:
    - The heuristic calculates all the combinations of kmedoids if it does not
      surpass max_combinations or max_combinations otherwise.
    - For each combination, the cost is the symmetric of the hamming distance of
      pairwise medoids. The configuration with the least cost is chosen.

  Args:
    dist: the matrix with distance between points.
    k: the number of clusters and, thus, medoids.
    max_combinations: the maximum number of configurations to be analyzed.

  Returns:
    A list of medoids, represented as indexes.
  """
  n_el = len(dist)
  comb = None
  if n_combinations(n_el, k) < max_combinations:
    comb = itertools.combinations(xrange(n_el), k)
    max_combinations = n_combinations(n_el, k)

  min_cost = float('inf')
  sel_medoids = None
  seen_samples = []
  for i in range(max_combinations):
    cost = 0
    if comb:
      medoids = comb.next()
    else:
      medoids = random.sample(range(n_el), k)
      seen_samples.append(medoids)
    for m1 in medoids:
      for m2 in medoids:
        cost += - hamming(dist[m1], dist[m2])
    if cost < min_cost:
      min_cost = cost
      sel_medoids = list(medoids)
  
  return sel_medoids


def assign_medoids(dist, elements, medoids):
  """ Assigns the closest medoid for each element.

  Args:
    dist: a list of lists with the distance matrix.
    elements: the elements, which are just the range of indexes.
    medoids: the list of medoids' indices.

  Returns:
    A list with the associated medoid for each element.
  """
  assoc_medoid = [0] * len(elements)
  
  for medoid in medoids:
    assoc_medoid[medoid] = medoid
  for element in [e for e in elements if e not in medoids]:
    min_dist = float('inf')
    close_medoid = None
    random.shuffle(medoids) # avoids favoring the first listed
    for medoid in medoids:
      if dist[element][medoid] < min_dist:
        close_medoid = medoid
        min_dist = dist[element][medoid]
    assoc_medoid[element] = close_medoid

  return assoc_medoid


def calculate_cost(dist, elements, medoid, assoc_medoid):
  """ Calculates the cost of a clustering.

  Observations:
    - The cost is defined as the sum over all the distances to the associated
      medoid.

  Args:
    dist: the distance matrix.
    elements: the elements range of indices.
    medoid: the medoids' indices.
    assoc_medoids: the list with the associated medoid for each element.

  Returns:
    An integer with the total cost of the configuration.
  """
  return sum([dist[medoid][e] for e in elements if assoc_medoid[e] == medoid])


def update_medoids(dist, elements, medoids, assoc_medoid):
  """ Updates the medoids.

  Observations:
    - An update is performed if a non-medoid from a cluster is switched with the
      medoid and reduces the total cost.

  Args:
    dist: a list of lists with the distance matrix.
    elements: the range of elements' indices.
    medoids: the current medoids' indices.
    assoc_medoids: the list with the associated medoid for each element.

  Returns:
    A tuple (converg, medoids), where converg is a binary indicating convergence
      occurence and medoids is the, possibly new, list of medoids' indices.
  """
  converg = True

  for medoid in medoids:
    min_cost = calculate_cost(dist, elements, medoid, assoc_medoid) 
    new_medoid = None
    random.shuffle(elements)
    for element in [e for e in elements if e not in medoids and assoc_medoid[e]
        == medoid]:
      new_cost = calculate_cost(dist, elements, element, [m if m != medoid else
        element for m in assoc_medoid])
      if new_cost < min_cost:
        min_cost = new_cost
        new_medoid = element
    if new_medoid != None:
      converg = False
      medoids = [m if m != medoid else new_medoid for m in medoids]

  return converg, medoids


def get_labels(assoc_medoid):
  """ Performs a standardization over the labels, from medoids' indices to
    integers from 0 to k - 1.

  Args:
    assoc_medoid: the list with the associated medoids for each element.

  Returns:
    A new list with cluster labels coded from 0 to k - 1.
  """
  curr = 0
  labels = assoc_medoid[:]
  for medoid in sorted(set(assoc_medoid)):
    labels = [l if l != medoid else curr for l in labels]
    curr += 1
  return labels
