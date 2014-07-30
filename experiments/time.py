_TIME_DIR = 'time/'

def time_avg(random_iters, repetitions):
  time_avgs = []
  for it in random_iter:
    time_file = open(_TIME_DIR + 'time%d.dat' % it, 'r')
    disamb_time = 0
    worlds_time = 0
    rank_time = 0
    for rep in range(repetitions):
      time_file.readline()
      disamb_time += float(time_file.readline().strip())
      time_file.readline()
      worlds_time += float(time_file.readline().strip())
      time_file.readline()
      rank_time += float(time_file.readline().strip())
      time_file.readline()
    time_avgs.append((disamb_time / rep, worlds_time / rep, rank_time / rep))
  return time_avgs

def time_measure(random_iters, repetitions):
  time_measures = []
  for it in random_iter:
    time_file = open(_TIME_DIR + 'time%d.dat' % it, 'r')
    for rep in range(repetitions):
      time_file.readline()
      disamb_time = float(time_file.readline().strip())
      time_file.readline()
      worlds_time = float(time_file.readline().strip())
      time_file.readline()
      rank_time = float(time_file.readline().strip())
      time_file.readline()
      time_measures.append((it, (disamb_time, worlds_time, rank_time)))
  return time_measures

if __name__ == '__main__':

    random_iter = [1, 2, 5, 10, 22, 46, 100, 215, 464, 1000]
    repetitions = 5

    time_measures = time_measure(random_iter, repetitions)
    for it, time in time_measures:
      print '%d,%d,%d,%d' % (it, time[0], time[1], time[2])
