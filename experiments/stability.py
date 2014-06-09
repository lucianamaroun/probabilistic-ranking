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
  rankings = [main.prob_ranking() for _ in range(3)]
  
  for index, ranking in enumerate(rankings):
    outfile = open('ranking' + str(index) + '.dat', 'w')
    print >> outfile, ranking
    outfile.close()

  print stability(rankings)
