""" Module that handles the data, serving as a preprocessing for other modules'
    methods.
"""

from models import Reference


def get_input(filename, labeled=False):
  """ Gets the input data divided in blocks, as test or training, as well as the
    corpus.

  Args:
    filename: filename with the references.
    labeled: if true, the data is for training; otherwise, it is for testing.

  Returns:
    A triple (references, corpus, blocks) containing, respectively, a dictionary
      of reference objects, a list represeting the superset of names and the
      references' ids divided in blocks.
  """
  references = read_data(filename, labeled=labeled)
  corpus = get_corpus(references)
  return references, corpus


def read_data(filename, labeled=False):
  """ Reads the input file of references and creates a blocked list of
      reference objects.

  Args:
    filename: the name of the file with the references.
    labeled: if the reference should be labeled to an entitiy or not.

  Returns:
    A list of lists of reference objects grouped by block.
  """
  references = []
  curr_block = []
  count = 0
  input_file = open(filename, 'r')
  for line in input_file:
    line = line.strip()
    if not line:
      references.append(curr_block)
      curr_block = []
      continue
    attrs = line.split('<>')
    reference = Reference(refid=count,
      name=attrs[4],
      title=attrs[5],
      coauthors=attrs[2].split(':') if attrs[2] != 'undefined' else [],
      venue=attrs[3],
      label=attrs[1].split('_')[0] if labeled else None)
    curr_block.append(reference)
    count += 1
  if curr_block:
    references.append(curr_block)
  input_file.close()
  return references


def get_corpus(references):
  """ Obtains the corpus, i. e., the superset of author names in the references.

  Observations:
    - The corpus contains both authors and coauthors names.

  Args:
    references: a list of lists with the blocked references objects.

  Returns:
    A list of strings with names.
  """
  corpus = []
  for block in references:
    for ref in block:
      corpus.append(ref.name)
      corpus += ref.coauthors
  return corpus
