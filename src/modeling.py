""" Modeling of pair of references as similarity vectors to be used in the
    logistic regression. """

from lib import apriori

import re
import math
import Levenshtein


_MIN_SUPPORT_LEVEL_1 = 0.01
_MIN_SUPPORT_LEVEL_2 = 0.01
_MIN_CONFIDENCE = 0.01
_MAX_LEVEL = 2
_STFIDF_THRESHOLD = 0.7


def model(references, corpus, labeled=False):
  """ Constructs a similarity vector for all pair of references.
  
  Args:
    references: list of references objects of grouped in blocks, which are going
      to be compared for correference.
    labeled: if the list of references are labeled, and thus, can be classified
      from the input.

  Returns:
    A list of lists with the format [stfidf, simcoaut, overlap, simtitle,
      eqvenue], where:
        - stfidf is the soft-TFIDF between the names.
        - simcoaut is the coauthorship similarity defined as the sum of the 
          confidences of rules in which a implies a coauthor of b and vice versa.
        - overlap is the number of coauthors' names in common.
        - simtitle is the jaccard similarity between titles.
        - eqvenue is a boolean indicating equal or different venues.
      If labeled, a tuple (sim_vectors, classes) is returned instead, in which
      sim_vector is the previous list of tuples and classes is a list of
      classes of the vectors, which can be 1, indicating they represent a
      correference pair, or 0 otherwise.
  """
  idf = get_idf(corpus)
  sim_vectors = []
  classes = []
  for block in references:
    sim_vector_block = []
    coaut_rules = get_coauthorship_rules(block)
    for reference_a in block:
      for reference_b in [r for r in block if r.refid > reference_a.refid]:
        sim_vector = (soft_tfidf(reference_a.name, reference_b.name, idf),
          coauthorship_similarity(reference_a, reference_b, coaut_rules),
          overlap(reference_a.coauthors, reference_b.coauthors),
          jaccard(reference_a.title, reference_b.title),
          int(reference_a.venue == reference_b.venue))
        if labeled:
          vector_class = 1 if reference_a.label == reference_b.label else 0
          classes.append(vector_class)
        sim_vector_block.append(sim_vector)
    sim_vectors.append(sim_vector_block)
  if labeled:
    return sim_vectors, classes
  else:
    return sim_vectors


def get_coauthorship_transactions(references):
  """ Generates coauthorship transactions for the references in the same block.

  Observations:
    - A coauthorship transaction consists of a set of authors that appears in
      the same publication.
    - Coauthorship transactions are only generated within the same block as it 
      is going to be used for disambiguation purposes.

  Args:
    references: a list with the references objects.
  
  Returns:
    A list of transactions. Each transaction is represented by a list of strings
      containing names.
  """
  transactions = []
  for ref in references:
    authors = [ref.name]
    for coaut in ref.coauthors:
      authors.append(coaut)
    transactions.append(authors)
  return transactions


def get_coauthorship_rules(references):
  """ Runs apriori algorithm to obtain association rules, here defined as
      coauthorship rules, only of the form A -> B, as well as their confidences.
      
  Args:
    references: the list of references objects.
  
  Returns:
    A nested dictionary of coauthorship rules indexed by reference_a.name and, 
      then, by reference_b.name and with confidences as values.
  """
  transactions = get_coauthorship_transactions(references)
  return apriori.run_apriori(transactions, [_MIN_SUPPORT_LEVEL_1, 
      _MIN_SUPPORT_LEVEL_2], _MIN_CONFIDENCE, _MAX_LEVEL)


def coauthorship_similarity(reference_a, reference_b, coaut_rules):
  """ Calculates coauthorship similarity between a pair of references.
  
  Args:
    reference_a: the first reference object.
    reference_b: the second reference object.
    coaut_rules: a nested dictionary with coauthorship rules.

  Returns:
    A real value representing the similarity.
  """
  sim = 0
  if reference_b.name in coaut_rules:
    for coauthor_a in reference_a.coauthors:
      for coauthor_b in coaut_rules[reference_b.name]:
        if coauthor_a == coauthor_b:
          sim += coaut_rules[reference_b.name][coauthor_b]
  if reference_a.name in coaut_rules:
    for coauthor_b in reference_b.coauthors:
      for coauthor_a in coaut_rules[reference_a.name]:
        if coauthor_a == coauthor_b:
          sim += coaut_rules[reference_a.name][coauthor_a]
  return sim


def overlap(list_a, list_b):
  """ Finds the overlap of elements of two lists.
  
  Observations:
    - The lists must contain unique elements.

  Args:
    list_a: the first list.
    list_b: the second list.

  Returns:
   An integer with the total count of common elements.
  """
  overlap = 0
  for element_a in list_a:
    for element_b in list_b:
      if element_a == element_b:
        overlap += 1
  return overlap


def jaccard(string_a, string_b):
  """ Computes the jaccard coefficient between two strings.

  Observations:
    - The strings are turned into sets by the splitting into words and unity
      reinforcement.

  Args:
    string_a: first string.
    string_b: second string.

  Returns:
    A real value between 0 and 1 with the jaccard similarity.
  """
  words_a = set(get_words(string_a))
  words_b = set(get_words(string_b))
  intersection = overlap(words_a, words_b)
  union = len(words_a) + len(words_b) - intersection
  return float(intersection) / float(union)


def get_words(string):
  """ Obtains all the words within a sentence.

  Args:
    string: the string with the sentence.

  Returns:
    A list of strings with the words.
  """
  return [w for w in re.sub("[^\w]", " ",  string).split() if len(w) > 1]


def get_idf(collection):
  """ Gets the inverse document frequence of a collection of documents.

  Observations:
    - Also includes two special entries with values @max_idf, with the word of
      max idf, and @min_idf, with the minimum.

  Args:
    collection: a list of strings.

  Returns:
    A dictionary with the inversed frequency as values and words as keys.
  """
  
  idf = dict()
  collectionSize = len(collection)
  for s in collection:
    words = set(get_words(s))
    for w in words:
      if w in idf:
        idf[w] += 1
      else:
        idf[w] = 1
  
  for w in idf:
    ratio = float(collectionSize) / float(idf[w])
    idf[w] = math.log(ratio)
  
  max_idf = 0.0
  min_idf = float('inf')
  for w in idf:
    if idf[w] > max_idf:
      max_idf = idf[w]
    if idf[w] < min_idf:
      min_idf = idf[w]
  idf["@max_idf"] = max_idf
  idf["@min_idf"] = min_idf
  
  return idf


def close(threshold, words_a, words_b):
  """ Gets the close list of words in two list of words.

  Observations:
    - The normalized edit distance was used as similarity metric.
    - The close words are obtained only from the first set of words.

  Args:
    threshold: a minimum edit distance ratio for two words to be considered
      close, varying from 0 to 1.
    words_a: the first list of words.
    words_b: the second list of words.

  Returns:
    A list of words (strings).
  """
  close = []
  for word_a in words_a:
    for word_b in words_b:
      if Levenshtein.ratio(word_a, word_b) > threshold:
        close.append(word_a)
  return close


def most_similar(word, other_words):
  """ Returns the maximum similarity between one word and all the words of a
      list.

  Observations:
    - Uses the normalized edit distance as similarity metric.

  Args:
    word: the word demanding comparisson.
    other_words: the list of words to compare with.

  Returns:
    A value between 0 and 1 with the maximum similarity.
  """
  return max(other_words, key=lambda x: Levenshtein.ratio(word, x))


def tfidf(word, words, idf):
  """ Calculates the tfidf similarity between a word and a list of words.

  Args:
    word: the word demanding comparisson.
    words: the list of words to compare with.
    idf: a dictionary with the inversed frequency as values and words as keys.

  Returns:
    A value with the tfidf.
  """
  count = [1 if w == word else 0 for w in words]
  
  tf = sum(count)
  return float(tf) * idf[word]


def norm_tfidf(word, words, idf):
  """ A normalized version of the tfidf.

  Args:
    word: the word demanding comparisson.
    words: the list of words to compare with.
    idf: a dictionary with the inversed frequency as values and words as keys.

  Returns:
    A value between 0 and 1 with the normalized tfidf.
  """
  return tfidf(word, words, idf) / math.sqrt(sum([tfidf(w, words, idf) ** 2 
      for w in words]))


def soft_tfidf(string_a, string_b, idf):
  """ Soft tfidf similarity between two sentences.

  Args:
    string_a: the first sentence.
    string_b: the second sentence.
    idf: a dictionary with the inversed frequency as values and words as keys.

  Returns:
    A real value with the soft tfidf.
  """
  words_a = get_words(string_a)
  words_b = get_words(string_b)
  if len(words_a) < len(words_b):
    words_a, words_b = words_b, words_a
  soft = 0.0
  for word in close(_STFIDF_THRESHOLD, words_a, words_b):
    w_sim = most_similar(word, words_b)
    soft += norm_tfidf(word, words_a, idf) * norm_tfidf(w_sim, words_b, idf) * \
        Levenshtein.ratio(word, w_sim)
  return soft
