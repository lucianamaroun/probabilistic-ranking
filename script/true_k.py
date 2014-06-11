_FILE = 'data/training3.dat'

input_file = open(_FILE, 'r')
entities = set()
for line in input_file:
  line = line.strip()
  if not line:
    continue
  entity = line.split('<>')[1].split('_')[0]
  entities.add(entity)
print len(entities)
