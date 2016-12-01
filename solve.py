# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    solve.py                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: rbaum <rbaum@student.42.fr>                +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2016/11/15 02:11:53 by rbaum             #+#    #+#              #
#    Updated: 2016/11/15 02:11:54 by rbaum            ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import time

class Solver:
  # __slots__ = ['cur', 'goal', 'length', 'n', 'parents', 'start', 'man_goal', 'man_init']
  def __init__(self, goal, initial, n):
    self.expanded = 0
    self.goal =  goal
    self.solved = 0
    self.start = initial
    self.path = []
    self.length = len(goal)
    self.n = n
    self.queue = []
    self.parents = {}
    self.col  = [[self.goal[i + (j * self.n)] for j in range(self.n)] for i in range(self.n)]
    self.line = [[self.goal[j + (i * self.n)] for j in range(self.n)] for i in range(self.n)]
    self.man_goal = self.pre_manhatan(goal)
    self.dist = self.manhatan_distance(initial)

  def swap(self, pos, new, mtx):
    ret = mtx[:]
    ret[pos], ret[new] = ret[new], ret[pos]
    return ret

  def print_solution(self, cur):
    rev = []
    print("SOLUTION")
    print("Nb of states in memory: ", len(self.parents))
    print("Nb of nodes expanded: ", self.expanded)
    z = -1
    while cur != None:
      z += 1
      rev += [cur]
      cur = self.parents[str(cur)][0]
    print("Length of path:", z)
    # for i in rev[::]:
      # self.print_matrix(i)

  def print_matrix(self, m):
    n = self.n
    x = (n * n)
    k = len(str(x))
    for i in range(x):
      print("{:{}d}".format(m[i], k), end=' ')
      if not (i + 1) % n and i > 0:
        print ("")
    print("-----------")

  def get_next_states(self, mtx, direction = 5):#direction
    n = self.n
    pos = mtx.index(0)
    if  direction != 1 and pos < self.length and (pos + 1) % n: 
      yield (self.swap(pos, pos + 1, mtx), (pos, pos + 1), 3)
    if  direction != 3 and pos > 0 and pos % n:
     yield (self.swap(pos, pos - 1, mtx), (pos, pos - 1), 1)
    if  direction != 4 and pos > n - 1:
     yield (self.swap(pos, pos - n, mtx), (pos, pos - n), 2)
    if  direction != 2 and pos < self.length - self.n:
      yield (self.swap(pos, pos + n, mtx), (pos, pos + n), 4)

  def h(self, matrix):
    return (self.manhatan_distance(matrix))

  def get_xy(self, value):
    y = value // self.n
    x = value % self.n
    return (y, x)
    
  # heuristique

  def pre_manhatan(self, matrix):
    dict = {}
    l = len(matrix)
    for i in range(1, l):
      m = self.get_xy(matrix.index(i))
      dict[i] = (m[0], m[1])
    return (dict)


  def update_manhatan(self, dist, state, parent_state):
    # print("\33[94m")
    matrix, pos, direction = state
    goal = self.man_goal[matrix[pos[0]]]
    m = self.get_xy(pos[0])
    m2 = self.get_xy(pos[1])
    y, x = abs(m[0] - goal[0]), abs(m[1] - goal[1])
    y2, x2 = abs(m2[0] - goal[0]), abs(m2[1] - goal[1])
    dist -= (x2 + y2)
    dist += (x + y)
    # dist += self.update_conflict(matrix, pos[0], direction, dist, parent_state)
    return (dist)
    # pass

  #   pass
  def manhatan_distance(self, matrix):
    # print("\33[92m")
    l = len(matrix)
    dist = 0
    lin = 0
    lin = self.linear_conflict(matrix)
    for i in range(1, l):
      m = self.get_xy(matrix.index(i))
      goal = self.man_goal[i]
      y = abs(m[0] - goal[0])
      x = abs(m[1] - goal[1])
      dist += x + y
    dist += lin
    # print("REGULAR\t\t", dist, lin, dist + lin)
    return (dist)

#RANGE SHIT
  def update_conflict(self, matrix, pos, direction, dist, parent_state):
    (y, x) = self.get_xy(pos)
    if direction == 1:
      i1, i2 = x - 1, x + 1
      cur_col  = [[matrix[j + (i * self.n)]for i in range(self.n)] for j in range(i1, i2)] 
      old_col = [[parent_state[j + (i * self.n)]for i in range(self.n)] for j in range(i1, i2)]
    elif direction == 3:
      i1, i2 = x , x + 2
      cur_col  = [[matrix[j + (i * self.n)]for i in range(self.n)] for j in range(i1, i2)] 
      old_col = [[parent_state[j + (i * self.n)]for i in range(self.n)] for j in range(i1, i2)] 
    elif direction == 2:
      i1, i2 = y - 1, y + 1
      cur_col  = [[matrix[j + (i * self.n)] for j in range(self.n)] for i in range(i1, i2)]
      old_col  = [[parent_state[j + (i * self.n)] for j in range(self.n)] for i in range(i1, i2)]
    elif direction == 4:
      i1, i2 = y, y + 2
      cur_col  = [[matrix[j + (i * self.n)] for j in range(self.n)] for i in range(i1, i2)]
      old_col  = [[parent_state[j + (i * self.n)] for j in range(self.n)] for i in range(i1, i2)]
      # ------------
    if direction == 2 or direction == 4:
      lin = self.conflict(cur_col, self.line)
      lin2= self.conflict(old_col, self.line)
    else:
      lin = self.conflict(cur_col, self.col)
      lin2= self.conflict(old_col, self.col)
    return (lin - lin2)



  def count_conf(self, cur):
    rr = 0
    for i in cur:
      for j in cur[i:]:
        if (self.goal.index(i) > self.goal.index(j)): 
          rr += 1
    return rr

  def conflict(self,cur_col, vs):
    rr = 0
    res = []
    for i in range(len(cur_col)):
      for cc in cur_col[i]:
        if cc in vs[i] and cc is not 0:
          res += [cc]
      rr += self.count_conf(res)
      res = []
    return rr

  # def linear_conflict(self, matrix):
  #   cur_col  = [[matrix[i + (j * self.n)] for j in range(self.n)] for i in range(self.n)]
  #   cur_row  = [[matrix[j + (i * self.n)] for j in range(self.n)] for i in range(self.n)]
  #   return self.conflict(cur_col, self.col) + self.conflict(cur_row, self.line)

#TODO

  def check_column(self, c, x, y, matrix):
    for i in range(y, self.n):
      if matrix[(y * self.n) + x]
    pass

  def check_line(self, c, x, y, matrix):
    pass

  def linear_conflict(self, matrix):
    rr = 
    for y in range(self.n):
      for x in range(self.n):
        c = matrix[(y * self.n) + x]
        rr += check_column(c, x, y, matrix)
        rr += check_line(c, x, y, matrix)
  # # def update_conflict(self, matrix):
      # pos = self.get_xy(matrix.index(0))


