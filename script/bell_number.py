import src.preprocessing as pre
import math

BELL_NUMBERS = {}


def choose(n, k):
  """
  A fast way to calculate binomial coefficients by Andrew Dalke
  (contrib).
  """
  if 0 <= k <= n:
    ntok = 1
    ktok = 1
    for t in xrange(1, min(k, n - k) + 1):
      ntok *= n
      ktok *= t
      n -= 1
    return ntok // ktok
  else:
    return 0


def bell_number(n):
  if n == 1:
    return 1
  elif n in BELL_NUMBERS:
    return BELL_NUMBERS[n]
  else:
    bell = 0
    for i in range(n):
      bell += choose(n-1, i) * bell_number(n-1)
    BELL_NUMBERS[n] = bell
    return bell

if __name__ == '__main__':
  blocks, _ = pre.get_input('data/data.dat')
  blocks_bells = []
  for block in blocks:
    blocks_bells.append(bell_number(len(block)))
  #print [len(block) for block in blocks]
  #print blocks_bells
  print math.log10(sum(blocks_bells))
