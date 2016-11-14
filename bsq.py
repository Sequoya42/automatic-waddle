#!/usr/bin/python
import sys

class Bsq:
  def __init__(self, full, obst, empty, nb_line, tab):
    self.full = full
    self.obst = obst
    self.empty = empty
    self.nb_line = nb_line
    self.tab = tab

def get_map(argv):
  with open(argv[1]) as f:
    l = [line.strip() for line in f]
  for line in l[1:]:
    if len(line) is not len(l[1]):
      sys.exit("Bad line length")
  arg_line = l[0][::-1]
  nb_line = l[0][0:-3]
  all = ''.join(l)
  all = all[len(nb_line):len(nb_line) + 2] + all[len(nb_line) + 3:]
  if len(set(all)) is not 2:
    sys.exit("Bad char {}".format(set(all)))
  if (int(nb_line) != int((len(l) - 1))):
    sys.exit('bad number of line [real] : {} [given] : {}'.format(len(l) - 1, nb_line))
  bsq = Bsq(arg_line[0], arg_line[1], arg_line[2], nb_line, l[1:])
  return (bsq)

def check_exist(tab, i, j):
  return(i < len(tab) and j < len(tab[i]))

def get_value(tab, i, j):
  v1 = int(tab[i - 1][j]) if i > 0 else 0
  v3 = int(tab[i][j - 1]) if j > 0 else 0
  v2 = int(tab[i - 1][j - 1]) if j > 0 and i > 0 else 0
  return ((min(v1, v2, v3) + 1))

def solve_map(bsq):
  new_tab = []
  for a in (i.replace(bsq.empty, '1').replace(bsq.obst, '0') for i in bsq.tab): new_tab += [[int(x) for x in a]]
  big = (0, 0, 0)
  for i in range(0, len(new_tab)):
    for j in range(0, len(new_tab[i])):
       if new_tab[i][j] is 1:
          r = get_value(new_tab, i, j)
          new_tab[i] = new_tab[i][0:j] + [r] +  new_tab[i][j + 1:]
          if int(r) > big[2]:
            big = (i + 1, j + 1, r)
  for i in range(big[0] - big[2], big[0]):
    for j in range(big[1] - big[2], big[1]):
      bsq.tab[i] = bsq.tab[i][0:j] + bsq.full + bsq.tab[i][j + 1:]
  for l in bsq.tab: print (l)

def main(argv):
  if len(argv) != 2:
    sys.exit("Need one argument only (file with map, first line is nb line, empty, obst, full then map, example\n" + 
"2.ox\n" + "o...o\n" + "o...o")
  bsq = get_map(argv)
  solved = solve_map(bsq)
if __name__ == '__main__':
  main(sys.argv)