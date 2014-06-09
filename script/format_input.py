""" Creates the test and training files from the original data """

import os
import numpy as np
import math
import random
from src import auxiliary as aux


_RAW_DATA_FILE = 'raw_data'
_TRAINING_RATIO = 0.25
_TEST_FILE = 'data/data.dat'
_TRAINING_FILE = 'data/training.dat'


def get_test_data(input_dir):
  """ Unifies all the data into one file, used as test, and turns the blocking
      into a variable.

  Observations:
    - The font_* and title_* files are merged by adding the title in the end of
      the first one's lines.
    - The blocking consists of a list with the starting id for each block.

  Args:
    input_dir: the name of the directory with the original data, terminating
      with '/'.

  Returns:
    A list of strings with the lines of the test (whole data) and a list of
    integers with the beginning id for each block.
  """
  test_lines = []
  blocks_init = []
  count = 0
  for file_name in os.listdir(input_dir):
    if file_name.startswith("font_"):
      suffix = file_name.split("_")[1]
      font_input_path = input_dir + "font_" + suffix
      title_input_path = input_dir + "title_" + suffix
      font_input_file = open(font_input_path, "r")
      title_input_file = open(title_input_path, "r")
      blocks_init.append(count)
      for font_line in font_input_file:
        title_line = title_input_file.readline()
        title = title_line.strip().split('<>')[1]
        test_lines.append(font_line.strip() + title + '<>')
        count += 1
  blocks_init.append(float('inf')) # terminating information
  return test_lines, blocks_init


def get_training_data(test_lines, test_blocks):
  """ Selects a random sample of the reference lines to be used as test.
  
  Args:
    test_lines: all the lines.

  Returns:
    A list of strings with the selected lines and the blocks by starting index.
  """
  total_amount = len(test_lines)
  training_amount = int(_TRAINING_RATIO * total_amount)
  index_sample = random.sample(range(total_amount), training_amount)
  index_sample.sort()
  blocks = []
  curr_block = -1
  ref_count = 0
  for index in index_sample:
    if index >= test_blocks[curr_block + 1]:
      blocks.append(ref_count)
      curr_block += 1
    ref_count += 1
  blocks.append(float('inf'))
  sample = [test_lines[index] for index in index_sample]
  return sample, blocks


def output_lines(filename, lines, blocks):
  """ Outputs into a file a list of strings as lines.

  Args:
    filename: the name of the output file.
    lines: the list of lines to output.

  Returns:
    None.
  """
  outfile = open(filename, 'w')
  ref_count = 0
  block_count = 0
  for line in lines:
    print >> outfile, line
    ref_count += 1
    if ref_count >= blocks[block_count + 1]:
      block_count += 1
      print >> outfile, ''


def format_data(input_dir):
  """ Formats the original bibliographic data into one test file and one
      training file
  
  Args:
    input_dir: the directory with the original files.

  Returns:
    None.
  """
  input_dir = aux.adequate_dir(input_dir)
  test_lines, test_blocks = get_test_data(input_dir)
  training_lines, training_blocks = get_training_data(test_lines, test_blocks)
  output_lines(_TRAINING_FILE, training_lines, training_blocks)
  output_lines(_TEST_FILE, test_lines, test_blocks)


if __name__ == '__main__':
  format_data(_RAW_DATA_FILE)
