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

def time_measure_iterations(random_iters, repetitions):
  time_measures = []
  for it in random_iter:
    time_file = open(_TIME_DIR + 'time_iterations_%d.dat' % it, 'r')
    for rep in range(repetitions):
      time_file.readline()
      disamb_time = float(time_file.readline().strip())
      time_file.readline()
      worlds_time = float(time_file.readline().strip())
      time_file.readline()
      rank_time = float(time_file.readline().strip())
      time_file.readline()
      time_measures.append((it, (disamb_time, worlds_time, rank_time)))
    time_file.close()
  return time_measures

def time_measure_input_size(sizes, repetitions):
  time_measures = []
  for size in sizes:
    time_file = open(_TIME_DIR + 'time_input_size_%d.dat' % size, 'r')
    for rep in range(repetitions):
      time_file.readline()
      disamb_time = float(time_file.readline().strip())
      time_file.readline()
      worlds_time = float(time_file.readline().strip())
      time_file.readline()
      rank_time = float(time_file.readline().strip())
      time_file.readline()
      time_measures.append((size, (disamb_time, worlds_time, rank_time)))
    time_file.close()
  return time_measures


if __name__ == '__main__':
    random_iter = [1, 2, 5, 10, 22, 46, 100, 215, 464, 1000]
    input_size = [429, 857, 1286, 1715, 2144, 2572, 3001, 3430, 3858, 4287]
    repetitions = 10

    time_measures_iterations = time_measure_iterations(random_iter, repetitions)
    time_measures_input_size = time_measure_input_size(input_size, repetitions)
    output_file = open('time_iterations.csv', 'w')
    for it, time in time_measures_iterations:
      print >> output_file, '%d,%d,%d,%d' % (it, time[0], time[1], time[2])
    output_file.close()
    output_file = open('time_input.csv', 'w')
    for it, time in time_measures_input_size:
      print >> output_file, '%d,%d,%d,%d' % (it, time[0], time[1], time[2])
    output_file.close()
