from math import sqrt

import src.main as main
from src.models import Ranking
from scipy.stats import kendalltau, spearmanr


_RANKING_DIR = 'rankings/'

def normalize_uncertainty(uncertainty):
  max_unc = len(uncertainty) - 1
  new_uncertainty = []
  for unc in uncertainty:
    new_uncertainty.append(round(unc/max_unc * 10))
  return new_uncertainty

def read_rankings(r_its, repetitions):
  rankings = []
  for r_it in r_its:
    iter_rankings = []
    for rep in range(repetitions):
      rank_file = open(_RANKING_DIR + 'ranking%d-%d.dat' % (r_it, rep+1), 'r')
      unc = []
      for line in rank_file:
        if len(line.split(' ')) == 1:
          continue
        unc.append(float(line.split('(')[1].split(')')[0]))
      ranking = Ranking()
      ranking.ordering = range(len(unc))
      ranking.uncertainty = normalize_uncertainty(unc)
      iter_rankings.append(ranking)
    rankings.append(iter_rankings)
  return rankings


def stability_sd(rankings):
  n_authors = len(rankings[0].ordering)

  uncertainty = [[] for _ in range(n_authors)]

  for ranking in rankings:
    for author in ranking.ordering:
      uncertainty[author].append(ranking.uncertainty[author])

  variances = [sum([(u - author_uncs[0]) ** 2 for u in author_uncs[1:]]) / \
      float(len(author_uncs) - 1) for author_uncs in uncertainty]
  sds = [sqrt(var) for var in variances]

  return sum(sds) / len(sds)


def stability_kendall(rankings):
  score = 0
  p_value = 0
  count = 0

  for index, ranking_a in enumerate(rankings):
    unc_ranking_a = sorted(ranking_a.ordering, key=lambda x:
        (ranking_a.uncertainty[ranking_a.ordering.index(x)], x))
    for ranking_b in [r for i, r in enumerate(rankings) if i > index]:
      unc_ranking_b = sorted(ranking_b.ordering, key=lambda x:
          (ranking_b.uncertainty[ranking_b.ordering.index(x)], x))
      curr_score, curr_p = kendalltau(unc_ranking_a, unc_ranking_b)
      score += curr_score
      p_value += curr_p
      count += 1.0
  return score / count, p_value / count


def stability_spearman(rankings):
  score = 0
  p_value = 0
  count = 0
  scores = []

  for index, ranking_a in enumerate(rankings):
    unc_ranking_a = sorted(ranking_a.ordering, key=lambda x:
        (ranking_a.uncertainty[ranking_a.ordering.index(x)], x))
    for ranking_b in [r for i, r in enumerate(rankings) if i > index]:
      unc_ranking_b = sorted(ranking_b.ordering, key=lambda x:
          (ranking_b.uncertainty[ranking_b.ordering.index(x)], x))
      curr_score, curr_p = spearmanr(unc_ranking_a, unc_ranking_b)
      score += curr_score
      scores.append(curr_score)
      p_value += curr_p
      count += 1.0
  return score / count, p_value / count, scores

if __name__ == '__main__':

  #random_iters = [1, 2, 5, 10, 22, 46, 100, 215, 464, 1000]
  random_iters = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
  repetitions = 5
  rankings = read_rankings(random_iters, repetitions)
 

  print "Standard deviation metric"
  for iter_rankings in rankings:
    print stability_sd(iter_rankings)
  print "Kendall tau metric"
  for iter_rankings in rankings:
    print stability_kendall(iter_rankings)[0]
  print "Spearman metric"
  for iter_rankings in rankings:
    print stability_spearman(iter_rankings)[0]
#  for r_iter in random_iters:
#    rankings = read_rankings([r_iter], repetitions)
#    for iter_rankings in rankings:
#      _, _, scores = stability_spearman(iter_rankings)
#      for score in scores:
#        print '%d,%f' % (r_iter, score)
