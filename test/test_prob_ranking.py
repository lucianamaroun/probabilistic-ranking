import unittest

import test_cases

import src.preprocessing as pre
import src.prob_ranking as rank
from src.models import Ranking 
from src.models import Reference

class RankingSampleTestCase(test_cases.SampleTestCase):

  def setUp(self):
    super(RankingSampleTestCase, self).setUp()
    self.references = pre.read_data(self.testfilename)
    self.base_partitioning = [[0, 0, 1], [0, 1], [0], [0, 0], [0], [0]]
    self.alt_partitionings = [[[0, 1, 1], [1, 0], [0], [0, 0], [0], [0]],
        [[1, 0, 1], [0, 1], [0], [0, 0], [0], [0]]]
  
  def test_get_authors(self):
    truth = ({
        0: [Reference(0, 'm jones', 
          'symbol intersect detect method improv spatial intersect join', 
          ['e rundensteiner', 'y huang'], 'geoinformatica', None),
        Reference(1, 'matthew c jones', 
            'improv spatial intersect join symbol intersect detect', 
            ['e rundensteiner', 'h kuno', 'p marron', 'v taube', 'y ra'], 
            'sigmod intern manag data', None)],
        1: [Reference(2, 'matthew c jones',
            'view materi techniqu complex hirarch object', ['e rundensteiner',
            'y huang'], 'ssd symposium larg spatial databas', None)],
        2: [Reference(3, 'mike w miller', 'domin draw bipartit graph', 
          ['l berg'], 'sigucc special interest group univers comput servic',
          None)],
        3: [Reference(4, 'mike w miller', 'rel compromis statist databas', 
            [], 'sigucc special interest group univers comput servic', None)],
        4: [Reference(5, 'c chen', 'formal approach scenario analysi',
          ['d kung', 'j samuel', 'j gao', 'p hsia', 'y toyoshima'],
          'ieee softwar', None)],
        5: [Reference(6, 'jane j robinson', 'discours code clue context', [], 
          'acl meet the associ comput linguist', None),
          Reference(7, 'jane j robinson', 'diagram grammar dialogu', [],
            'cooper interfac inform system', None)],
        6: [Reference(8, 'a gupta', 'iri h java distanc educ', ['a gonzalez', 
          'a hamid', 'c overstreet', 'h wahab', 'j wild', 'k maly', 's ghanem',
          'x zhu'], 'acm journal educ resourc comput', None)],
        7: [Reference(9, 'mary d brown',
          'intern redund represent limit bypass support pipelin adder regist '
          'file', ['y patt'], 'proceed the th ieee intern symposium high '
          'perform comput architectur hpca intern symposium high perform comput'
          ' architectur talk slide', None)]
        }, [0, 2, 4, 5, 6, 7, float('inf')])
    result = rank.get_authors(self.references, self.base_partitioning)
    self.assertEqual(result, truth)

  def test_get_ranking(self):
    truth = Ranking({
        0: [Reference(0, 'm jones', 
          'symbol intersect detect method improv spatial intersect join', 
          ['e rundensteiner', 'y huang'], 'geoinformatica', None),
        Reference(1, 'matthew c jones', 
            'improv spatial intersect join symbol intersect detect', 
            ['e rundensteiner', 'h kuno', 'p marron', 'v taube', 'y ra'], 
            'sigmod intern manag data', None)],
        1: [Reference(2, 'matthew c jones',
            'view materi techniqu complex hirarch object', ['e rundensteiner',
            'y huang'], 'ssd symposium larg spatial databas', None)],
        2: [Reference(3, 'mike w miller', 'domin draw bipartit graph', 
          ['l berg'], 'sigucc special interest group univers comput servic',
          None)],
        3: [Reference(4, 'mike w miller', 'rel compromis statist databas', 
            [], 'sigucc special interest group univers comput servic', None)],
        4: [Reference(5, 'c chen', 'formal approach scenario analysi',
          ['d kung', 'j samuel', 'j gao', 'p hsia', 'y toyoshima'],
          'ieee softwar', None)],
        5: [Reference(6, 'jane j robinson', 'discours code clue context', [], 
          'acl meet the associ comput linguist', None),
          Reference(7, 'jane j robinson', 'diagram grammar dialogu', [],
            'cooper interfac inform system', None)],
        6: [Reference(8, 'a gupta', 'iri h java distanc educ', ['a gonzalez', 
          'a hamid', 'c overstreet', 'h wahab', 'j wild', 'k maly', 's ghanem',
          'x zhu'], 'acm journal educ resourc comput', None)],
        7: [Reference(9, 'mary d brown',
          'intern redund represent limit bypass support pipelin adder regist '
          'file', ['y patt'], 'proceed the th ieee intern symposium high '
          'perform comput architectur hpca intern symposium high perform comput'
          ' architectur talk slide', None)]
        }, blocks=[0, 2, 4, 5, 6, 7, float('inf')], rank_function=len)
    result = rank.get_ranking(self.references, self.base_partitioning, len)
    self.assertEqual(result, truth)


  def test_get_ranking_alt(self):
    truth = Ranking(authors={
      0: [Reference(0, 'm jones', 
          'symbol intersect detect method improv spatial intersect join', 
          ['e rundensteiner', 'y huang'], 'geoinformatica', None)],
      1: [Reference(1, 'matthew c jones', 
            'improv spatial intersect join symbol intersect detect', 
            ['e rundensteiner', 'h kuno', 'p marron', 'v taube', 'y ra'], 
            'sigmod intern manag data', None),
          Reference(2, 'matthew c jones',
            'view materi techniqu complex hirarch object', ['e rundensteiner',
            'y huang'], 'ssd symposium larg spatial databas', None)],
      2: [Reference(4, 'mike w miller', 'rel compromis statist databas', 
            [], 'sigucc special interest group univers comput servic', None)],
      3: [Reference(3, 'mike w miller', 'domin draw bipartit graph', 
          ['l berg'], 'sigucc special interest group univers comput servic',
          None)],
      4: [Reference(5, 'c chen', 'formal approach scenario analysi',
          ['d kung', 'j samuel', 'j gao', 'p hsia', 'y toyoshima'],
          'ieee softwar', None)],
      5: [Reference(6, 'jane j robinson', 'discours code clue context', [], 
          'acl meet the associ comput linguist', None),
        Reference(7, 'jane j robinson', 'diagram grammar dialogu', [],
            'cooper interfac inform system', None)],
      6: [Reference(8, 'a gupta', 'iri h java distanc educ', ['a gonzalez', 
          'a hamid', 'c overstreet', 'h wahab', 'j wild', 'k maly', 's ghanem',
          'x zhu'], 'acm journal educ resourc comput', None)],
      7: [Reference(9, 'mary d brown',
          'intern redund represent limit bypass support pipelin adder regist '
          'file', ['y patt'], 'proceed the th ieee intern symposium high '
          'perform comput architectur hpca intern symposium high perform comput'
          ' architectur talk slide', None)]
      }, blocks=[0, 2, 4, 5, 6, 7, float('inf')], rank_function=len)

    result = rank.get_ranking(self.references, self.alt_partitionings[0], 
        len)
    self.assertEqual(result, truth)

 
  def test_match_rankings(self):
    truth = [[2, 2], [1, 1], [0, 0], [4, 3], [3, 4], [5, 5], [6, 6], [7, 7]]
    ranking_a = rank.get_ranking(self.references, self.base_partitioning, len)
    rankings_b = []
    for alt_partitioning in self.alt_partitionings:
      ranking_b = rank.get_ranking(self.references, alt_partitioning, len)
      rankings_b.append(ranking_b)
    result = rank.match_rankings(ranking_a, rankings_b)
    self.assertEqual(result, truth)


  def test_calculate_uncertainties(self):
    truth = [0.94, 0., 0.94, 0.47, 0.47, 0., 0., 0.]
    ranking_a = rank.get_ranking(self.references, self.base_partitioning, len)
    rankings_b = []
    for alt_partitioning in self.alt_partitionings:
      ranking_b = rank.get_ranking(self.references, alt_partitioning, len)
      rankings_b.append(ranking_b)
    matchings = rank.match_rankings(ranking_a, rankings_b)
    result = rank.calculate_uncertainties(matchings)
    for i in range(len(result)):
      self.assertAlmostEqual(result[i], truth[i], 2)


  def test_calculate_uncertainties(self):
    ranking_a = rank.get_ranking(self.references, self.base_partitioning, len)
    rankings_b = []
    for alt_partitioning in self.alt_partitionings:
      ranking_b = rank.get_ranking(self.references, alt_partitioning, len)
      rankings_b.append(ranking_b)
    matchings = rank.match_rankings(ranking_a, rankings_b)
    uncertainty = rank.calculate_uncertainties(matchings)
    ranking_a.set_uncertainty(uncertainty)
    truth = ranking_a
    result = rank.rank(self.references, self.base_partitioning,
        self.alt_partitionings)
    self.assertEqual(result, truth)


if __name__ == '__main__':
  unittest.main()
