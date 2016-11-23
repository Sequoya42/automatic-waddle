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

import sys, verify, solve

def get_map(argv):
  try: 
    with open(argv[1]) as f: 
      l = [line.strip() for line in f if line[0] is not '#']
    return (l)
  except Exception as error:
    exit("Invalid file")


# should be possible to use string, and still use index, in much the same
# way as list

def matrix_validity(m, n):
  new = []
  for i in m:
    k = i.find('#')
    if k == -1:
      new += [i]
    else:
      new += [i[:k]]
  verif = [i.replace(" ",  "") for i in new]
  for i in verif:
    if not i.isdigit():
      exit("Digits only")
  return new



def main(argv):
  given = get_map(argv)
  n = int(given[0])
  given = given[1:]
  given = matrix_validity(given, n)
  matrix = [int(x) for l in given for x in l.split()]
  if len(matrix) is not (n*n):
    exit("Bad file, should be n by n")
  spiral = verify.spiral_matrix(n)
  verify.check_validity(matrix, spiral, n)
  print("After check, go to resolve")
  astar = solve.Astar(spiral, matrix, n)
  astar.solve()
  astar = solve.Astar(matrix, spiral, n)
  astar.solve()


if __name__ == '__main__':
  main(sys.argv)

#todo
  # efficient manhatan with lookup table instead of computing every time
