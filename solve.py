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
  __slots__ = ['cur', 'goal', 'length', 'n', 'parents', 'start']
  def __init__(self, goal, initial, n):
    self.start = initial
    self.cur = initial
    self.goal = goal
    self.length = len(goal)
    self.n = n
    self.parents = {}

  def solve(self):
    # parents will be the closed list, containing the parent, and the cost
    cost = 0
    priority = 0
    self.parents[str(self.cur)] = (None, 0, 0)
    open = p.pr()
    open.add(0, self.cur, cost)
    print ("Beginning")
    print(self.f(self.cur))
    misc.print_matrix(self.cur, self.n)
    print("------")
    j = 0
    while open:
      # print("LEN:\t", len(open))
      # for i in open.q:
      #   print(i[0])
      j += 1
      # print(j)
      current = open.get()
      # print(current)
      # misc.print_matrix(current, self.n)
      if current == self.goal:
        return self.print_solution(current)

      cost = self.parents[str(current)][2] + 1
      for new_state in self.get_next_states(current):
        priority = self.f(new_state) + cost
        if str(new_state) not in self.parents or cost < self.parents[str(new_state)][2]:
          # print("adding : ", new_state)
          open.add(priority, new_state, cost)
          self.parents[str(new_state)] = (current, priority, cost)
 
  def get_swapped(self, pos, new, mtx):
    ret = mtx[:]
    ret[pos], ret[new] = ret[new], ret[pos]
    return (ret)


  def print_solution(self, cur):
    rev = []
    print("SOLUTION")
    z = -1
    self.print_matrix(cur)
    while cur:
      z += 1
      rev += [[cur]]
      cur = self.parents[str(cur)][0]
    self.print_matrix(self.start)
    print(z)
    # for i in rev:
      # print(i)
      # self.print_matrix(i)
    exit(0)
    pass




  def print_matrix(self, m):
    n = self.n
    x = (n * n)
    k = len(str(x))
    for i in range(x):
      print("{:{}d}".format(m[i], k), end=' ')
      if not (i + 1) % n and i > 0:
        print ("")
    print("-----------")

  def get_next_states(self, mtx):
    n = self.n
    pos = mtx.index(0)
    if pos > 0 and pos % n: yield self.get_swapped(pos, pos - 1, mtx)
    if pos > n: yield self.get_swapped(pos, pos - n, mtx)
    if pos < self.length and (pos + 1) % n: yield self.get_swapped(pos, pos + 1, mtx)
    if pos < self.length - self.n : yield self.get_swapped(pos, pos + n, mtx)
    return next

  def f(self, matrix):
    return (self.cost() + self.manhatan_distance(matrix))

  def get_xy(self, value):
    y = value // self.n
    x = value % self.n
    return (y, x)
    
  # heuristique
  def manhatan_distance(self, matrix):
    goal = self.goal
    l = len(matrix)
    dist = 0
    for i in range(0, l):
      m = self.get_xy(matrix[i])
      f = self.get_xy(goal[i])
      y = abs(m[0] - f[0])
      x = abs(m[1] - f[1])
      dist += x + y
    # print("DIST MAN: ", dist, self.cur)
    return (dist)

  # g
  def cost(self):
    return 1
