""" Module containing the models. """

class Reference(object):
  """ Represents a reference for a researcher in a publication. """
  
  def __init__(self, refid, name, title, coauthors, venue, label):
    """ Initializes all the elements which characterizes the reference.

    Args:
      refid: the integer representing the id of the reference.
      name: a string with the author name which denotes the researcher in
        question.
      title: a string with the title of the publication.
      coauthors: a list of strings with the coauthors' names.
      venue: a string with the name of the venue.
      label: a string containing a label for an actual researcher or None if
        unlabeled.

    Returns:
      None.
    """
    self.refid = refid
    self.name = name
    self.title = title
    self.coauthors = coauthors
    self.venue = venue
    self.label = label

  def __eq__(self, other):
    """ Compares two references only by attributes and not by reference. """
    return self.refid == other.refid and self.name == other.name and \
        self.coauthors == other.coauthors and self.venue == other.venue and \
        self.label == other.label

  def __str__(self):
    """ Format the object as a string containing its fields. """
    return ('Reference:\n'
        ' refid: %d\n'
        ' name: %s\n'
        ' title: %s\n'
        ' coauthors: %s\n'
        ' venue: %s\n'
        ' label: %s') % (self.refid, self.name, self.title, self.coauthors,
            self.venue, self.label)


class Ranking(object):
  """ Models a ranking of authros with ordering, uncertainty, authors and blocks
    information.
  """

  def __init__(self, authors=None, blocks=None, rank_function=None):
    """ Initializes the basic information and sorts the authors.
    
    Args:
      authors: the dictionary of authors.
      blocks: a list with the author key starting each block.
      rank_function: the function to be used for the ranking, which receives the
        list of references to calculate the score. The score sorts in reverse
        order,  which means the higher score the lower the position in the
        ranking (i.e., closer to the top).
    """
    self.authors = authors
    self.blocks = blocks
    self.rank_function = rank_function
    self.sort()
    self.uncertainty = None

  def set_uncertainty(self, uncertainty):
    """ Insert uncertainty information. 
    
    Args:
      uncertainty: a vector of uncertainties indexed by the ranking positions
        (ordering).
    """
    self.uncertainty = uncertainty

  def sort(self):
    """ Calculates the ordering of the authors if all the information is
      defined. """
    self.ordering = sorted(self.authors.keys(), key=lambda x: 
        self.rank_function(self.authors[x]), reverse=True) if self.authors and \
        self.rank_function else None

  def __eq__(self, other):
    """ Defines the value equality instead of reference. """
    if self.blocks != other.blocks:
      print self.blocks
      print other.blocks
    return self.authors == other.authors and self.blocks == other.blocks and \
        self.rank_function == other.rank_function and self.uncertainty == \
        other.uncertainty

  def get_name(self, references):
    """ Get the name for a set of reference as the most common one. """
    return max(references, key=lambda x: len(x.name)).name

  def __str__(self):
    """ Prints the ranking. """
    string = ''
    for pos, author in enumerate(self.ordering):
      string += '%d. %s (%.2f)\n' % (pos + 1, self.get_name(self.authors[author]),
          self.uncertainty[author])
    return string[:-1]
