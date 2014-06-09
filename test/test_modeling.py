""" Unit testing for the modeling module.

    Run in the project folder as follows:
    python -m test.test_modeling
"""

import unittest
import time
import os
import math
import Levenshtein

from src import modeling as mod
from src import preprocessing as pre


class SampleTestCase(unittest.TestCase):
  """ Class with a sample test case from the used data. """

  def setUp(self):
    """ Creates the file containing the references sample. """
    self.testfilename = 'test/testfile%d' % time.time()
    writetestfile = open(self.testfilename, 'w')
    writetestfile.write(
        '0<>81_0<>e rundensteiner:y huang<>geoinformatica<>m jones<>symbol '
            'intersect detect method improv spatial intersect join<>\n'
        '1<>81_1<>e rundensteiner:h kuno:p marron:v taube:y ra<>sigmod intern '
            'manag data<>matthew c jones<>improv spatial intersect join symbol '
            'intersect detect<>\n'
        '2<>81_2<>e rundensteiner:y huang<>ssd symposium larg spatial '
            'databas<>matthew c jones<>view materi techniqu complex hierarch '
            'object<>\n\n'

        '0<>185_0<>l berg<>sigucc special interest group univers comput '
            'servic<>mike w miller<>domin draw bipartit graph<>\n'
        '1<>185_1<>undefined<>sigucc special interest group univers comput '
            'servic<>mike w miller<>rel compromis statist databas<>\n\n'

        '0<>94_0<>d kung:j samuel:j gao:p hsia:y toyoshima<>ieee softwar<>c '
            'chen<>formal approach scenario analysi<>\n\n'

        '0<>69_0<>undefined<>acl meet the associ comput linguist<>jane j '
            'robinson<>discours code clue context<>\n'
        '1<>69_1<>undefined<>cooper interfac inform system<>jane j robinson<>'
            'diagram grammar dialogu<>\n\n'

        '0<>0_0<>a gonzalez:a hamid:c overstreet:h wahab:j wild:k maly:s ghanem'
            ':x zhu<>acm journal educ resourc comput<>a gupta<>iri h java '
            'distanc educ<>\n\n'

        '4<>43_1<>y patt<>proceed the th ieee intern symposium high perform '
            'comput architectur hpca intern symposium high perform comput '
            'architectur talk slide<>mary d brown<>intern redund remod.ent '
            'limit bypass support pipelin adder regist file<>\n\n')
    writetestfile.close()

  def tearDown(self):
    """ Deletes all used files and structures. """
    os.remove(self.testfilename)

  def test_get_coauthorship_transactions(self):
    """ Tests the function get_coauthorship_transactions. """
    references = pre.read_data(self.testfilename)
    truth = [[
      ['m jones', 'e rundensteiner', 'y huang'],
        ['matthew c jones', 'e rundensteiner', 'h kuno', 'p marron', 'v taube', 
            'y ra'],
        ['matthew c jones', 'e rundensteiner', 'y huang']],
      [['mike w miller', 'l berg'],
        ['mike w miller']],
      [['c chen', 'd kung', 'j samuel', 'j gao', 'p hsia', 'y toyoshima']], 
      [['jane j robinson'],
        ['jane j robinson']],
      [['a gupta', 'a gonzalez', 'a hamid', 'c overstreet', 'h wahab',
            'j wild', 'k maly', 's ghanem', 'x zhu']],
      [['mary d brown', 'y patt']]]
    for i in range(len(references)):
      transactions = mod.get_coauthorship_transactions(references[i])
      self.assertEquals(transactions, truth[i])

  def test_get_coauthorship_rules(self):
    """ Tests the function get_coauthorship_rules. """
    references = pre.read_data(self.testfilename)
    truth = [{'m jones': {'e rundensteiner': 1.0, 
        'y huang': 1.0},
      'e rundensteiner': {'m jones': 1.0/3,
        'y huang': 2.0/3,
        'matthew c jones': 2.0/3, 
        'h kuno': 1.0/3,
        'p marron': 1.0/3,
        'v taube': 1.0/3, 
        'y ra': 1.0/3
      },
      'y huang': {'m jones': 1.0/2,
        'e rundensteiner': 1.0,
        'matthew c jones': 1.0/2
      },
      'matthew c jones': {'e rundensteiner': 1.0,
        'y huang': 1.0/2, 
        'h kuno': 1.0/2,
        'p marron': 1.0/2,
        'v taube': 1.0/2, 
        'y ra': 1.0/2
      },
      'h kuno': {'e rundensteiner': 1.0,
        'matthew c jones': 1.0,
        'p marron': 1.0,
        'v taube': 1.0, 
        'y ra': 1.0
      },
      'p marron': {'e rundensteiner': 1.0,
        'matthew c jones': 1.0,
        'h kuno': 1.0,
        'v taube': 1.0, 
        'y ra': 1.0
      },
      'v taube': {'e rundensteiner': 1.0,
        'matthew c jones': 1.0,
        'h kuno': 1.0,
        'p marron': 1.0, 
        'y ra': 1.0
      },
      'y ra': {'e rundensteiner': 1.0,
        'matthew c jones': 1.0,
        'h kuno': 1.0,
        'p marron': 1.0, 
        'v taube': 1.0
      }},
      {'mike w miller': {'l berg': 1.0/2},
      'l berg': {'mike w miller': 1.0}},
      {'c chen': {'d kung': 1.0,
        'j samuel': 1.0,
        'j gao': 1.0,
        'p hsia': 1.0,
        'y toyoshima': 1.0
      },
      'd kung': {'c chen': 1.0,
        'j samuel': 1.0,
        'j gao': 1.0,
        'p hsia': 1.0,
        'y toyoshima': 1.0
      },
      'j samuel': {'c chen': 1.0,
        'd kung': 1.0,
        'j gao': 1.0,
        'p hsia': 1.0,
        'y toyoshima': 1.0
      },
      'j gao': {'c chen': 1.0,
        'd kung': 1.0,
        'j samuel': 1.0,
        'p hsia': 1.0,
        'y toyoshima': 1.0
      },
      'p hsia': {'c chen': 1.0,
        'd kung': 1.0,
        'j samuel': 1.0,
        'j gao': 1.0,
        'y toyoshima': 1.0
      },
      'y toyoshima': {'c chen': 1.0,
        'd kung': 1.0,
        'j samuel': 1.0,
        'j gao': 1.0,
        'p hsia': 1.0
      }},
      {},
      {'a gupta': {'a gonzalez': 1.0,
        'a hamid': 1.0, 
        'c overstreet': 1.0,
        'h wahab': 1.0,
        'j wild': 1.0,
        'k maly': 1.0,
        's ghanem': 1.0,
        'x zhu': 1.0
      },
      'a gonzalez': {'a gupta': 1.0,
        'a hamid': 1.0, 
        'c overstreet': 1.0,
        'h wahab': 1.0,
        'j wild': 1.0,
        'k maly': 1.0,
        's ghanem': 1.0,
        'x zhu': 1.0
      },
      'a hamid': {'a gupta': 1.0,
        'a gonzalez': 1.0, 
        'c overstreet': 1.0,
        'h wahab': 1.0,
        'j wild': 1.0,
        'k maly': 1.0,
        's ghanem': 1.0,
        'x zhu': 1.0
      },
      'c overstreet': {'a gupta': 1.0,
        'a gonzalez': 1.0, 
        'a hamid': 1.0,
        'h wahab': 1.0,
        'j wild': 1.0,
        'k maly': 1.0,
        's ghanem': 1.0,
        'x zhu': 1.0
      },
      'h wahab': {'a gupta': 1.0,
        'a gonzalez': 1.0, 
        'a hamid': 1.0,
        'c overstreet': 1.0,
        'j wild': 1.0,
        'k maly': 1.0,
        's ghanem': 1.0,
        'x zhu': 1.0
      },
      'j wild': {'a gupta': 1.0,
        'a gonzalez': 1.0, 
        'a hamid': 1.0,
        'c overstreet': 1.0,
        'h wahab': 1.0,
        'k maly': 1.0,
        's ghanem': 1.0,
        'x zhu': 1.0
      },
      'k maly': {'a gupta': 1.0,
        'a gonzalez': 1.0, 
        'a hamid': 1.0,
        'c overstreet': 1.0,
        'h wahab': 1.0,
        'j wild': 1.0,
        's ghanem': 1.0,
        'x zhu': 1.0
      },
      's ghanem': {'a gupta': 1.0,
        'a gonzalez': 1.0, 
        'a hamid': 1.0,
        'c overstreet': 1.0,
        'h wahab': 1.0,
        'j wild': 1.0,
        'k maly': 1.0,
        'x zhu': 1.0
      },
      'x zhu': {'a gupta': 1.0,
        'a gonzalez': 1.0, 
        'a hamid': 1.0,
        'c overstreet': 1.0,
        'h wahab': 1.0,
        'j wild': 1.0,
        'k maly': 1.0,
        's ghanem': 1.0
      }},
      {'mary d brown': {'y patt': 1.0},
      'y patt': {'mary d brown': 1.0}} 
    ]
    for i in range(len(references)):
      rules = mod.get_coauthorship_rules(references[i])
      for author_a in rules:
        for author_b in rules[author_a]:
          self.assertEquals(round(rules[author_a][author_b], 4), 
            round(truth[i][author_a][author_b], 4))
      for author_a in truth[i]:
        for author_b in truth[i][author_a]:
          self.assertEquals(round(rules[author_a][author_b], 4), 
              round(truth[i][author_a][author_b], 4))

  def test_modeling_unlabeled(self):
    """ Tests the correct composition of the result in modeling function, 
        since the singular functions are tested. For unlabeled case. """
    references, corpus = pre.get_input(self.testfilename)
    sim_vectors = mod.model([references[0]], corpus)
    truth = [[(0.6506800700017669, 2.5, 1, 0.8571428571428571, 0),
        (0.6506800700017669, 3.5, 2, 0.0, 0),
        (1.0, 4.5, 1, 0.0, 0)]]
    self.assertEquals(sim_vectors, truth)    

  def test_modeling_labeled(self):
    """ Tests the correct composition of the result in modeling function, 
        since the singular functions are tested. For labeled case. """
    references, corpus = pre.get_input(self.testfilename, labeled=True)
    result = mod.model([references[0] + references[2]], corpus, 
        labeled=True)
    truth = ([[(0.6506800700017669, 2.5, 1, 0.8571428571428571, 0),
        (0.6506800700017669, 3.5, 2, 0.0, 0),
        (0.0, 0, 0, 0.0, 0),
        (1.0, 4.5, 1, 0.0, 0),
        (0.0, 0, 0, 0.0, 0),
        (0.0, 0, 0, 0.0, 0)]], 
        [1, 1, 0, 1, 0, 0])
    self.assertEquals(result, truth)
  
  def test_close(self):
    """ Tests the close function. """
    close = mod.close(mod._STFIDF_THRESHOLD,
        mod.get_words('matt carl jacob jones c david steward'), 
        mod.get_words('matthew colb jones stewrd smith davi'))
    truth = ['matt', 'jones', 'steward', 'david']
    self.assertEquals(set(close), set(truth))

  def test_most_similar(self):
    """ Tests the most similar function. """
    sim = mod.most_similar('matthew', 
        mod.get_words('matt carl jacob jones c david steward'))
    truth = 'matt'
    self.assertEquals(sim, truth)

  def test_tfidf(self):
    """ Tests the tfidf function. """
    references = pre.read_data(self.testfilename)
    corpus = pre.get_corpus(references) + ['matt']
    idf = mod.get_idf(corpus)
    tfidf = mod.tfidf('matt',
        mod.get_words('matt matt huang kuno jones c marron brown'),
        idf)
    truth = idf['matt'] * 2
    self.assertEquals(tfidf, truth)

  def test_norm_tfidf(self):
    """ Tests the normalized tfidf. """
    references = pre.read_data(self.testfilename)
    corpus = pre.get_corpus(references) + ['matt']
    idf = mod.get_idf(corpus)
    words = mod.get_words('matt matt huang kuno jones c marron brown')
    n_tfidf = mod.norm_tfidf('matt', words, idf)
    truth = mod.tfidf('matt', words, idf)
    denom = 0
    for word in words:
      denom += mod.tfidf(word, words, idf) ** 2
    denom = math.sqrt(denom)
    truth /= denom
    self.assertEquals(n_tfidf, truth)

  def test_soft_tfidf(self):
    """ Tests the soft tfidf. """
    references = pre.read_data(self.testfilename)
    corpus = pre.get_corpus(references) + ['matt', 'brow']
    idf = mod.get_idf(corpus)
    name_a = 'matt huang kuno jones brow'
    words_a = mod.get_words(name_a)
    name_b = 'matthew jones c marron brown'
    words_b = mod.get_words(name_b)
    s_tfidf = mod.soft_tfidf(name_a, name_b, idf)
    close = ['matt', 'jones', 'brow']
    truth = \
      mod.norm_tfidf('matt', words_a, idf) * \
          mod.norm_tfidf('matthew', words_b, idf) * \
          Levenshtein.ratio('matt', 'matthew') + \
      mod.norm_tfidf('jones', words_a, idf) * \
          mod.norm_tfidf('jones', words_b, idf) * \
          Levenshtein.ratio('jones', 'jones') + \
      mod.norm_tfidf('brow', words_a, idf) * \
          mod.norm_tfidf('brown', words_b, idf) * \
          Levenshtein.ratio('brow', 'brown')
    self.assertEquals(s_tfidf, truth)


if __name__ == '__main__':
  unittest.main()
