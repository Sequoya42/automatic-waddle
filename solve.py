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

import pr_queue as p
import misc
import time

class Astar:
  __slots__ = ['cur', 'goal', 'length', 'n', 'parents', 'start', 'man_goal', 'man_init']
  def __init__(self, goal, initial, n):
    self.start = initial
    self.goal = goal
    self.length = len(goal)
    self.n = n
    self.parents = {}
    self.man_goal = self.pre_manhatan(goal)
    self.man_init = self.pre_manhatan(initial)

  def solve(self):
    # parents will be the closed list, containing the parent, the priority, the cost, and the direction
    cost = 0
    priority = 0
    self.manhatan_distance(self.start)
    self.parents[str(self.start)] = (None, 0, 0, 0)
    open = p.pr()
    open.add(0, self.start, cost)
    j = 0
    while open:
       j += 1
       current = open.get()
       if current == self.goal:
        return self.print_solution(current)
       parent = self.parents[str(current)]
       cost = self.parents[str(current)][2] + 1
       old_f = parent[1] - parent[2]
       direction = parent[3]
       for new_state in self.get_next_states(current, direction):
         if str(new_state[0]) not in self.parents:# or cost < self.parents[str(new_state[0])][2]:
           priority = self.f(new_state) + cost
           open.add(priority, new_state[0], cost)
           self.parents[str(new_state[0])] = (current, priority, cost, new_state[2])
 
  def swap(self, pos, new, mtx):
    ret = mtx[:]
    ret[pos], ret[new] = ret[new], ret[pos]
    return ret


  def print_solution(self, cur):
    rev = []
    print("SOLUTION")
    z = -1
    while cur != None:
      z += 1
      rev += [cur]
      cur = self.parents[str(cur)][0]
    print("Length of path:", z)

  def print_matrix(self, m):
    n = self.n
    x = (n * n)
    k = len(str(x))
    for i in range(x):
      print("{:{}d}".format(m[i], k), end=' ')
      if not (i + 1) % n and i > 0:
        print ("")
    print("-----------")

  def get_next_states(self, mtx, dir):#direction
    n = self.n
    pos = mtx.index(0)
    if dir != 3 and pos > 0 and pos % n:
     yield (self.swap(pos, pos - 1, mtx),pos, 1)
    if dir != 4 and pos > n:
     yield (self.swap(pos, pos - n, mtx),pos, 2)
    if dir != 1 and pos < self.length and (pos + 1) % n: 
      yield (self.swap(pos, pos + 1, mtx),pos, 3)
    if dir != 2 and pos < self.length - self.n :
      yield (self.swap(pos, pos + n, mtx),pos, 4)

  def f(self, matrix):
    return (self.manhatan_distance(matrix[0]))

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

  def update_manhatan(self, matrix, dist):
      m = self.get_xy(matrix[0].index(matrix[1]))
      f = self.get_xy(self.goal.index(matrix[1]))
      y = abs(m[0] - f[0])
      x = abs(m[1] - f[1])
      dist += x + y
      return (dist)
    
  def manhatan_distance(self, matrix):
    goal = self.goal
    l = len(matrix)
    dist = 0
    for i in range(1, l):
      m = self.get_xy(matrix.index(i))
      goal = self.man_goal[i]
      y = abs(m[0] - goal[0])
      x = abs(m[1] - goal[1])
      dist += x + y
    return (dist)
