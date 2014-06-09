""" Unit testing for the preprocessing models.le.

    Run in the project folder as follows:
    python -m test.test_preprocessing
"""

import unittest
import time
import os

from src import preprocessing as pre
from src.models import Reference


class SampleTestCase(unittest.TestCase):
  """ Class with a sample test case from the main data set. """

  def setUp(self):
    """ Creates the file containing the references sample. """
    self.testfilename = 'test/testfile%d' % time.time()
    writetestfile = open(self.testfilename, 'w')
    writetestfile.write(
        '0<>81_0<>e rundensteiner:y huang<>geoinformatica<>m jones<>symbol '
            'intersect detect method improv spatial intersect join<>\n'
        '1<>81_1<>e rundensteiner:h kuno:p marron:v taube:y ra<>sigmodels.intern '
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
            'architectur talk slide<>mary d brown<>intern redund represent '
            'limit bypass support pipelin adder regist file<>\n\n')
    writetestfile.close()

  def tearDown(self):
    """ Deletes all used files and structures. """
    os.remove(self.testfilename)

  def test_read_data_labeled(self):
    """ Tests the function read_data for labeled data. """
    references = pre.read_data(self.testfilename, labeled=True)
    truth = [
      [Reference(0, 'm jones', 
          'symbol intersect detect method improv spatial intersect join', 
          ['e rundensteiner', 'y huang'], 'geoinformatica', '81'),
        Reference(1, 'matthew c jones', 
            'improv spatial intersect join symbol intersect detect', 
            ['e rundensteiner', 'h kuno', 'p marron', 'v taube', 'y ra'], 
            'sigmodels.intern manag data', '81'),
        Reference(2, 'matthew c jones',
            'view materi techniqu complex hirarch object', ['e rundensteiner',
            'y huang'], 'ssd symposium larg spatial databas', '81')],
      [Reference(3, 'mike w miller', 'domin draw bipartit graph', 
          ['l berg'], 'sigucc special interest group univers comput servic',
          '185'),
        Reference(4, 'mike w miller', 'rel compromis statist databas', 
            [], 'sigucc special interest group univers comput servic', '185')],
      [Reference(5, 'c chen', 'formal approach scenario analysi',
          ['d kung', 'j samuel', 'j gao', 'p hsia', 'y toyoshima'],
          'ieee softwar', '94')],
      [Reference(6, 'jane j robinson', 'discours code clue context', [], 
          'acl meet the associ comput linguist', '69'),
        Reference(7, 'jane j robinson', 'diagram grammar dialogu', [],
            'cooper interfac inform system', '69')],
      [Reference(8, 'a gupta', 'iri h java distanc educ', ['a gonzalez', 
          'a hamid', 'c overstreet', 'h wahab', 'j wild', 'k maly', 's ghanem',
          'x zhu'], 'acm journal educ resourc comput', '0')],
      [Reference(9, 'mary d brown',
          'intern redund represent limit bypass support pipelin adder regist '
          'file', ['y patt'], 'proceed the th ieee intern symposium high '
          'perform comput architectur hpca intern symposium high perform comput'
          ' architectur talk slide', '43')]]
    self.assertEquals(references, truth)

  def test_read_data_unlabeled(self):
    """ Tests the function read_data for unlabeled data. """
    references = pre.read_data(self.testfilename)
    truth = [
      [Reference(0, 'm jones', 
          'symbol intersect detect method improv spatial intersect join', 
          ['e rundensteiner', 'y huang'], 'geoinformatica', None),
        Reference(1, 'matthew c jones', 
            'improv spatial intersect join symbol intersect detect', 
            ['e rundensteiner', 'h kuno', 'p marron', 'v taube', 'y ra'], 
            'sigmodels.intern manag data', None),
        Reference(2, 'matthew c jones',
            'view materi techniqu complex hirarch object', ['e rundensteiner',
            'y huang'], 'ssd symposium larg spatial databas', None)],
      [Reference(3, 'mike w miller', 'domin draw bipartit graph', 
          ['l berg'], 'sigucc special interest group univers comput servic',
          None),
        Reference(4, 'mike w miller', 'rel compromis statist databas', 
            [], 'sigucc special interest group univers comput servic', None)],
      [Reference(5, 'c chen', 'formal approach scenario analysi',
          ['d kung', 'j samuel', 'j gao', 'p hsia', 'y toyoshima'],
          'ieee softwar', None)],
      [Reference(6, 'jane j robinson', 'discours code clue context', [], 
          'acl meet the associ comput linguist', None),
        Reference(7, 'jane j robinson', 'diagram grammar dialogu', [],
            'cooper interfac inform system', None)],
      [Reference(8, 'a gupta', 'iri h java distanc educ', ['a gonzalez', 
          'a hamid', 'c overstreet', 'h wahab', 'j wild', 'k maly', 's ghanem',
          'x zhu'], 'acm journal educ resourc comput', None)],
      [Reference(9, 'mary d brown',
          'intern redund represent limit bypass support pipelin adder regist'
          'file', ['y patt'], 'proceed the th ieee intern symposium high '
          'perform comput architectur hpca intern symposium high perform '
          'comput architectur talk slide', None)]]
    self.assertEquals(references, truth)

  def test_get_corpus(self):
    """ Tests the function get_corpus. """
    references = pre.read_data(self.testfilename)
    corpus = pre.get_corpus(references)
    truth = ['m jones', 'e rundensteiner', 'y huang', 'matthew c jones', 
        'e rundensteiner', 'h kuno', 'p marron', 'v taube', 'y ra', 
        'matthew c jones', 'e rundensteiner', 'y huang', 'mike w miller',
        'l berg', 'mike w miller', 'c chen', 'd kung', 'j samuel', 'j gao',
        'p hsia', 'y toyoshima', 'jane j robinson', 'jane j robinson',
        'a gupta', 'a gonzalez', 'a hamid', 'c overstreet', 'h wahab', 'j wild',
        'k maly', 's ghanem', 'x zhu', 'mary d brown', 'y patt']
    self.assertEquals(corpus, truth) 

  def test_get_input_labeled(self):
    """ Tests function get_input for labeled case. """
    result = pre.get_input(self.testfilename, labeled=True)
    truth = (
      [[Reference(0, 'm jones', 
          'symbol intersect detect method improv spatial intersect join', 
          ['e rundensteiner', 'y huang'], 'geoinformatica', '81'),
        Reference(1, 'matthew c jones', 
            'improv spatial intersect join symbol intersect detect', 
            ['e rundensteiner', 'h kuno', 'p marron', 'v taube', 'y ra'], 
            'sigmodels.intern manag data', '81'),
        Reference(2, 'matthew c jones',
            'view materi techniqu complex hirarch object', ['e rundensteiner',
            'y huang'], 'ssd symposium larg spatial databas', '81')],
      [Reference(3, 'mike w miller', 'domin draw bipartit graph', 
          ['l berg'], 'sigucc special interest group univers comput servic',
          '185'),
        Reference(4, 'mike w miller', 'rel compromis statist databas', 
            [], 'sigucc special interest group univers comput servic', '185')],
      [Reference(5, 'c chen', 'formal approach scenario analysi',
          ['d kung', 'j samuel', 'j gao', 'p hsia', 'y toyoshima'],
          'ieee softwar', '94')],
      [Reference(6, 'jane j robinson', 'discours code clue context', [], 
          'acl meet the associ comput linguist', '69'),
        Reference(7, 'jane j robinson', 'diagram grammar dialogu', [],
            'cooper interfac inform system', '69')],
      [Reference(8, 'a gupta', 'iri h java distanc educ', ['a gonzalez', 
          'a hamid', 'c overstreet', 'h wahab', 'j wild', 'k maly', 's ghanem',
          'x zhu'], 'acm journal educ resourc comput', '0')],
      [Reference(9, 'mary d brown',
          'intern redund represent limit bypass support pipelin adder regist '
          'file', ['y patt'], 'proceed the th ieee intern symposium high '
          'perform comput architectur hpca intern symposium high perform comput'
          ' architectur talk slide', '43')]],

    ['m jones', 'e rundensteiner', 'y huang', 'matthew c jones', 
        'e rundensteiner', 'h kuno', 'p marron', 'v taube', 'y ra', 
        'matthew c jones', 'e rundensteiner', 'y huang', 'mike w miller',
        'l berg', 'mike w miller', 'c chen', 'd kung', 'j samuel', 'j gao',
        'p hsia', 'y toyoshima', 'jane j robinson', 'jane j robinson',
        'a gupta', 'a gonzalez', 'a hamid', 'c overstreet', 'h wahab', 'j wild',
        'k maly', 's ghanem', 'x zhu', 'mary d brown', 'y patt'])
    self.assertEquals(result, truth)

  def test_get_input_unlabeled(self):
    """ Tests function get_input for unlabeled case. """
    result = pre.get_input(self.testfilename)
    truth = (
      [[Reference(0, 'm jones', 
          'symbol intersect detect method improv spatial intersect join', 
          ['e rundensteiner', 'y huang'], 'geoinformatica', None),
        Reference(1, 'matthew c jones', 
            'improv spatial intersect join symbol intersect detect', 
            ['e rundensteiner', 'h kuno', 'p marron', 'v taube', 'y ra'], 
            'sigmodels.intern manag data', None),
        Reference(2, 'matthew c jones',
            'view materi techniqu complex hirarch object', ['e rundensteiner',
            'y huang'], 'ssd symposium larg spatial databas', None)],
      [Reference(3, 'mike w miller', 'domin draw bipartit graph', 
          ['l berg'], 'sigucc special interest group univers comput servic',
          None),
        Reference(4, 'mike w miller', 'rel compromis statist databas', 
            [], 'sigucc special interest group univers comput servic', None)],
      [Reference(5, 'c chen', 'formal approach scenario analysi',
          ['d kung', 'j samuel', 'j gao', 'p hsia', 'y toyoshima'],
          'ieee softwar', None)],
      [Reference(6, 'jane j robinson', 'discours code clue context', [], 
          'acl meet the associ comput linguist', None),
        Reference(7, 'jane j robinson', 'diagram grammar dialogu', [],
            'cooper interfac inform system', None)],
      [Reference(8, 'a gupta', 'iri h java distanc educ', ['a gonzalez', 
          'a hamid', 'c overstreet', 'h wahab', 'j wild', 'k maly', 's ghanem',
          'x zhu'], 'acm journal educ resourc comput', None)],
      [Reference(9, 'mary d brown',
          'intern redund represent limit bypass support pipelin adder regist'
          'file', ['y patt'], 'proceed the th ieee intern symposium high '
          'perform comput architectur hpca intern symposium high perform '
          'comput architectur talk slide', None)]],

    ['m jones', 'e rundensteiner', 'y huang', 'matthew c jones', 
        'e rundensteiner', 'h kuno', 'p marron', 'v taube', 'y ra', 
        'matthew c jones', 'e rundensteiner', 'y huang', 'mike w miller',
        'l berg', 'mike w miller', 'c chen', 'd kung', 'j samuel', 'j gao',
        'p hsia', 'y toyoshima', 'jane j robinson', 'jane j robinson',
        'a gupta', 'a gonzalez', 'a hamid', 'c overstreet', 'h wahab', 'j wild',
        'k maly', 's ghanem', 'x zhu', 'mary d brown', 'y patt'])
    self.assertEquals(result, truth)


if __name__ == '__main__':
  unittest.main()
