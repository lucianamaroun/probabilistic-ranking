""" Simple test case with selected references from dataset. """

import unittest
import time
import os


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
            'architectur talk slide<>mary d brown<>intern redund represent '
            'limit bypass support pipelin adder regist file<>\n\n')
    writetestfile.close()

  def tearDown(self):
    """ Deletes all used files and structures. """
    os.remove(self.testfilename)
