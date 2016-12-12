# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    main.py                                            :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: rbaum <rbaum@student.42.fr>                +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2016/11/05 23:28:27 by rbaum             #+#    #+#              #
#    Updated: 2016/11/23 01:13:41 by rbaum            ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import argparse, verify, Astar, Idastar, Rbfs

def get_map(argv):
  try: 
    with open(argv) as f: 
      l = [line.strip() for line in f if line[0] is not '#']
    return (l)
  except Exception as error:
    exit("Invalid file")

# should be possible to use string, and still use index, in much the same
# way as list

def matrix_validity(m, n):
  new = []
  for i in m:
    if i == "": continue
    k = i.find('#')
    if k == -1: new += [i]
    else: new += [i[:k]]
  verif = (i.replace(" ",  "") for i in new)
  for i in verif:
    if not i.isdigit():
      exit("Digits only")
  return new

def main():
  parser = argparse.ArgumentParser(description='Npuzzle solver.')
  parser.add_argument('file', help="Please specify a file containing a npuzzle map")
  parser.add_argument('-a', '--algo', help="Please specify which algorithm to use", choices = ['idastar', 'astar', 'rbfs'], default ='astar')
  args = parser.parse_args()
  given = get_map(args.file)
  n = int(given[0])
  given = given[1:]
  given = matrix_validity(given, n)
  matrix = [int(x) for l in given for x in l.split()]
  if len(matrix) is not (n*n):
    exit("Bad file, should be n by n")
  spiral = verify.spiral_matrix(n)
  print("After check, go to resolve")
  verify.check_validity(matrix, spiral, n)
  if args.algo == 'astar':
    astar = Astar.Astar(matrix, spiral, n)
    astar.solve()
  elif args.algo == 'idastar':
    ida = Idastar.Idastar(matrix, spiral, n)
    ida.solve()
  elif args.algo == 'rbfs':
    print("RBFS [half done, not working correctly] \n=======")
    rbfs = Rbfs.Rbfs(matrix, spiral, n)
    rbfs.solve((rbfs.dist, rbfs.dist, rbfs.start), 99999999)
    print("Length: ", rbfs.expanded - 1, "\n==========")

  # matrix = [4, 15, 1, 2, 0, 14, 8, 13, 10, 12, 3, 9, 11, 5, 7, 6]
  # matrix = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0]

if __name__ == '__main__':
  main()


