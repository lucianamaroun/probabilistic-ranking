# Stability metric used: inverse of variance for each position -> average

from math import sqrt

import src.main as main

def stability(rankings):
  n_authors = len(rankings[0].ordering)
  uncertainty = [[] for _ in range(n_authors)]

  for ranking in rankings:
    for author in ranking.ordering:
      uncertainty[author].append(ranking.uncertainty[author])

  sums = [sum(uncs) for uncs in uncertainty]
  variances = [sum([(u - sum(uncs)) ** 2 for u in uncs]) / float(len(uncs))
      for uncs in uncertainty]
  stability = [- sqrt(var) for var in variances]

  return sum(stability) / len(stability)


if __name__ == '__main__':
  random_iterations = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50]
  for it in random_iterations:
    rankings = [main.prob_ranking() for _ in range(10)]
  
    for index, ranking in enumerate(rankings):
      outfile = open('ranking' + str(it) + '-' + str(index) + '.dat', 'w')
      print >> outfile, ranking
      outfile.close()

    print stability(rankings)
