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
    self.total = 0
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
    print("Expanded: ", self.expanded)
    print("Total: ", len(self.parents))
    z = -1
    while cur != None:
      z += 1
      rev += [cur]
      cur = self.parents[str(cur)][0]
    print("Length of path:", z)
    for i in rev[::]:
      self.print_matrix(i)

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
    return (value // self.n, value % self.n)
    
  # heuristique

  def pre_manhatan(self, matrix):
   # create dictionary key is tile number and value is pos (y, x)
    dict = {}
    l = len(matrix)
    for i in range(1, l):
      m = self.get_xy(matrix.index(i))
      dict[i] = (m[0], m[1])
    return (dict)


  def update_manhatan(self, dist, state, parent_state):
    matrix, pos, direction = state
    goal = self.man_goal[matrix[pos[0]]] # value updated
    # dist += self.linear_conflict(matrix)
    m = self.get_xy(pos[0])
    m2 = self.get_xy(pos[1])
    y, x = abs(m[0] - goal[0]), abs(m[1] - goal[1])
    y2, x2 = abs(m2[0] - goal[0]), abs(m2[1] - goal[1])
    dist -= (x2 + y2)
    dist += (x + y)
    return (dist)

  def manhatan_distance(self, matrix):
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
    return (dist)

  def check_column(self, c, x, y, matrix): #x does not change
    m = self.man_goal[c]
    rr = 0
    for i in range(y + 1, self.n):
      gg = matrix[(i * self.n) + x]
      if gg == 0: continue
      cm = self.man_goal[gg]
      if cm[1] == x and m[0] > cm[0]:
        rr += 2
    return rr

  def check_line(self, c, x, y, matrix): # y does not change
    m = self.man_goal[c]
    rr = 0
    for i in range(x + 1, self.n):
      gg = matrix[(y * self.n) + i]
      if gg == 0: continue
      cm = self.man_goal[gg]
      if cm[0] == y and m[1] > cm[1]:
        rr += 2
    return rr

  def linear_conflict(self, matrix):
    rr = 0
    for y in range(self.n):
      for x in range(self.n):
        c = matrix[(y * self.n) + x]
        if c == 0: continue
        if y < self.n - 1 and self.man_goal[c][1] == x:
          rr += self.check_column(c, x, y, matrix)
        if x < self.n -1 and self.man_goal[c][0] == y:
          rr += self.check_line(c, x, y, matrix)
    return rr

#