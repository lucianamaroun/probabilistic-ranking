# Stability metric used: inverse of variance for each position -> average

from math import sqrt

import src.main as main
from src.models import Ranking
from scipy.stats import kendalltau


def read_rankings(random_iter, repetitions):
  rankings = []
  for r_it in random_iter:
    iter_rankings = []
    for rep in range(repetitions):
      rank_file = open('ranking%d-%d.dat' % (r_it, rep+1), 'r')
      unc = []
      for line in rank_file:
        unc.append(float(line.split('(')[1].split(')')[0]))
      ranking = Ranking()
      ranking.ordering = range(len(unc))
      ranking.uncertainty = unc[:]
      iter_rankings.append(ranking)
    rankings.append(iter_rankings)
  return rankings


def stability_variance(rankings):
  n_authors = len(rankings[0].ordering)

  for ranking in rankings:
    ranking.uncertainty = normalize_uncertainty(ranking.uncertainty)

  uncertainty = [[] for _ in range(n_authors)]

  for ranking in rankings:
    for author in ranking.ordering:
      uncertainty[author].append(ranking.uncertainty[author])

  variances = [sum([(u - sum(uncs)) ** 2 for u in uncs]) / float(len(uncs))
      for uncs in uncertainty]
  stability = [- sqrt(var) for var in variances]

  return sum(stability) / len(stability)


def stability_unc_ranking(rankings):
  score = 0
  p_value = 0
  count = 0

  for ranking in rankings:
    ranking.uncertainty = normalize_uncertainty(ranking.uncertainty)

  for index, ranking_a in enumerate(rankings):
    unc_ranking_a = sorted(ranking_a.ordering, key=lambda x:
        ranking_a.uncertainty[ranking_a.ordering.index(x)])
    for ranking_b in [r for i, r in enumerate(rankings) if i > index]:
      unc_ranking_b = sorted(ranking_b.ordering, key=lambda x:
          ranking_b.uncertainty[ranking_b.ordering.index(x)])
      curr_score, curr_p = kendalltau(unc_ranking_a, unc_ranking_b)
      score += curr_score
      p_value += curr_p
      count += 1.0
  return score / count, p_value / count


def normalize_uncertainty(uncertainty):
  max_unc = len(uncertainty) / 2 + 1
  new_uncertainty = []
  for unc in uncertainty:
    new_uncertainty.append(round(unc/max_unc * 10))
  return new_uncertainty

if __name__ == '__main__':

    random_iter = [10, 20]
    repetitions = 4
    rankings = read_rankings(random_iter, repetitions)
  
    for iter_rankings in rankings:
      print stability_variance(iter_rankings)
      print stability_unc_ranking(iter_rankings)
