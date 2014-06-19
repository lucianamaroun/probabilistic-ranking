from munkres import Munkres
from math import sqrt

from src.models import Ranking


def rank(references, base_partitioning, alternative_partitionings):
  """ Ranks authors probabilistically.

  Args:
    references: a list of lists with the blocked references.
    base_partitioning: the base world for composing the deterministic ranking.
    alternative_partitionings: the alternative worlds for calculating the
      uncertainty.

  Returns:
    A probabilistic ranking with the base ranking plus uncertainties.
  """
  base_ranking = get_ranking(references, base_partitioning, len)
  alt_rankings = [get_ranking(references, alt_partitioning, len) for
      alt_partitioning in alternative_partitionings]
  matchings = match_rankings(base_ranking, alt_rankings)
  uncertainty = calculate_uncertainties(matchings)
  base_ranking.set_uncertainty(uncertainty)
  return base_ranking


def get_ranking(references, partitioning, rank_function):
  """ Derives a ranking object.

  Args:
    references: a list of lists with the blocked reference objects.
    partitioning: a list of labels coding a reference author (= cluster).
    rank_function: a function to calculate a ranking score from a list of
      references (which represents an author).

  Returns:
    A ranking object.
  """
  authors, blocks_start = get_authors(references, partitioning)
  ranking = Ranking(authors=authors, blocks=blocks_start,
      rank_function=rank_function) 
  return ranking


def get_authors(references, partitioning):
  """ Gets the authors, as a list of references, from a defined partitioning, as
    a list of labels.

  Args:
    references: a list of lists with the blocked references.
    partitioning: a list of labels for each reference.

  Returns:
    A dictionary of the authors, with keys from 0 to total - 1, and a list of
      the starting key for each block.
  """
  authors = {}
  blocks_start = []
  curr_author = 0
  for i in range(len(references)):
    block_part = partitioning[i]
    blocks_start.append(curr_author)
    curr_cluster = 0
    while curr_cluster in block_part:
      authors[curr_author] = [references[i][j] for j in range(len(block_part))
          if block_part[j] == curr_cluster]
      curr_cluster += 1
      curr_author += 1
  blocks_start.append(float('inf'))
  return authors, blocks_start


def match_rankings(ranking_a, rankings_b):
  """ Match a list of rankings (b) against a base one (a).

  Observations:
    - Applies the Hungarian algorithm (Munkres) in the bipartite graph of
      ranking_a and a ranking_b, only within the same block.
    - The cost for a pair is the symmetric of the number of common references.

  Args:
    ranking_a: the base ranking object.
    rankings_b: a list with alterantive ranking objects.

  Returns:
    A list of lists with the positions in alternative rankings for each position
      in the base ranking.
  """
  n_blocks = len(ranking_a.blocks) - 1
  mapping = [[] for _ in range(len(ranking_a.authors))]

  for ranking_b in rankings_b:
    for i in range(n_blocks):
      blocks_start = ranking_a.blocks
      authors_a = {a:refs for a, refs in ranking_a.authors.items() if a >= 
          blocks_start[i] and a < blocks_start[i+1]} 
      authors_b = {b:refs for b, refs in ranking_b.authors.items() if b >= 
          blocks_start[i] and b < blocks_start[i+1]} 
      k_authors = len(authors_a)
      if k_authors == 1: # no matching necessary, only one author
        author_a = authors_a.keys()[0]
        author_b = authors_b.keys()[0]
        mapping[ranking_a.ordering.index(author_a)] \
            .append(ranking_b.ordering.index(author_b))
        continue
      cost_matrix = [[0] * k_authors for _ in range(k_authors)]
      for a in authors_a:
        for b in authors_b:
          cost_matrix[a - blocks_start[i]][b - blocks_start[i]] = \
              - len([r for r in authors_a[a] if r in authors_b[b]])
      
      m = Munkres()
      block_pairs = m.compute(cost_matrix)
      for a, b in block_pairs:
        mapping[ranking_a.ordering.index(a + blocks_start[i])] \
            .append(ranking_b.ordering.index(b + blocks_start[i]))
  return mapping


def calculate_uncertainties(matchings):
  """ Get the uncertainties for a probabilistic ranking.

  Args:
    matchings: a list of lists with positions in alternative worlds for each
      author.

  Returns:
    A list of uncertainty indexed by the position in the base ranking.
  """
  uncertainty = []
  n_random_iter = len(matchings[0])
  
  for position in range(len(matchings)):
    positions = [position] + matchings[position]
    positions = [pos + 1 for pos in positions]
    sd_pos = sqrt(sum([(p - positions[0]) ** 2 for p in positions]) /
        float(n_random_iter + 1))
    uncertainty.append(sd_pos)
  
  return uncertainty
