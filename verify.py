# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    verify.py                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: rbaum <rbaum@student.42.fr>                +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2016/11/05 23:28:53 by rbaum             #+#    #+#              #
#    Updated: 2016/11/05 23:28:53 by rbaum            ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from merge import merge_sort

def count_inversions(matrix, n):
  ind = matrix.index(0)
  rowmat = n - (ind // n)
  m = matrix[:ind] + matrix[ind + 1:]
  inv_matrix = merge_sort(m, 0)[1]
  ss = inv_matrix + rowmat
  if n % 2:
    if inv_matrix % 2 == 0: return("identity", inv_matrix, rowmat)
    else: return ("other-half", inv_matrix, rowmat)
  if ss % 2: return ("other-half", inv_matrix, rowmat)
  else: return ("identity", inv_matrix, rowmat)

def check_validity(matrix, spiral, n):
  mi = count_inversions(matrix, n)
  si = count_inversions(spiral, n)
  if mi[0] is si[0]:
    print ("SOLVABLE: ",mi, si)
  else:
    exit(("NOT SOLVABLE", mi, si))

def print_2by2_matrix(m, n):
  k = len(str(n*n))
  for l in m:
    for i in l:
      print("{:{}d}".format(i, k), end=' ')
    print()
  print("------------------")


def spiral_matrix(n):
    m = [[0] * n for i in range(n)]
    dy, dx = [0, 1, 0, -1], [1, 0, -1, 0]
    y, x, c = 0, -1, 1
    for i in range(n + n - 1):
        for j in range((n + n - i) // 2):
            x += dx[i % 4]
            y += dy[i % 4]
            m[y][x] = int(c) 
            c += 1
    spiral = [x if x is not n*n else 0 for y in m for x in y]
    return spiral

