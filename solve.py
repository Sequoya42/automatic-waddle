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
import time
import heapq as hq

class Solver:
  # __slots__ = ['cur', 'goal', 'length', 'n', 'parents', 'start', 'man_goal', 'man_init']
  def __init__(self, goal, initial, n):
    self.goal =  goal
    self.solved = 0
    self.start = initial
    self.path = []
    self.length = len(goal)
    self.n = n
    self.queue = []
    self.parents = {}
    self.man_goal = self.pre_manhatan(goal)

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
      print (cur)
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
      yield (self.swap(pos, pos + 1, mtx),pos, 3)
    if  direction != 2 and pos < self.length - self.n:
      yield (self.swap(pos, pos + n, mtx),pos, 4)
    if  direction != 3 and pos > 0 and pos % n:
     yield (self.swap(pos, pos - 1, mtx),pos, 1)
    if  direction != 4 and pos > n - 1:
     yield (self.swap(pos, pos - n, mtx),pos, 2)

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


class Astar(Solver):

    def solve(self):
      # parents will be the closed list, containing the parent, the priority, the cost, and the direction 
      cost = 0
      tt = self.h(self.start)
      self.parents[str(self.start)] = (None, 0, 0, 0)
      open_list = p.pr()
      open_list.add(tt, cost, self.start)
      while open_list:
        (old_f, cost, current) = open_list.get() 
        cost += 1 
        if current == self.goal: 
          return self.print_solution(current)
        parent = self.parents[str(current)]
        direction = parent[3]
        for new_state in self.get_next_states(current, direction): 
          if str(new_state[0]) not in self.parents:
            priority = self.h(new_state[0]) + cost
            open_list.add(priority, cost, new_state[0])
            self.parents[str(new_state[0])] = (current, priority, cost, new_state[2])


class Idastar(Solver):

  def dfs(self, state, bound, cost):
    new_bound = 99999999
    self.start = state
    if self.h(state) == 0:
      self.path += [state]
      self.solved = 1
      return 0
    cost += 1
    for ns in self.get_next_states(state):
      if cost + self.h(ns[0]) <= bound:
        b = cost + self.dfs(ns[0], bound - cost, cost)
      else:
        b = cost + self.h(ns[0])
      if self.solved:
        print("COST IS ", cost)
        self.path += [state]
        return b
      new_bound = min(new_bound, b)
    return new_bound


  def solve(self):
    cost = 0
    current = self.start
    bound = self.h(self.start)
    print("Initial bound", bound)
    while True:
      print("while", bound)
      r = self.dfs(current, bound, 0)
      if self.solved:
        print("GOAL FOUND", r)
        for i in self.path[::-1]:
          print(i)
        return (0)
      elif r == -1:
        exit("PROBL")
      else:
        bound = r

    pass

