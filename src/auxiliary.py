""" Contains common and simple procedures used by several modules. """

import os


def adequate_dir(dirname):
  """ Formats a directory name in order to terminate with '/' if absent and
      creates it if necessary.
  
  Args:
    dirname: the string name of the directory to format.

  Returns:
    A string with the formatted directory name.
  """
  if not os.path.isdir(dirname):
    os.makedirs(dirname)
  return dirname if dirname[-1] == '/' else dirname + '/'
