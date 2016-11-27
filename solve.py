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
    self.col  = [[self.goal[i + (j * self.n)] for j in range(self.n)] for i in range(self.n)]
    self.man_goal = self.pre_manhatan(goal)
    self.dist = self.manhatan_distance(initial)

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


  def update_manhatan(self, state, dist):
    matrix, pos, direction = state
    value = matrix[pos[0]]
    print("Value, pos[0], pos[1] : ", value, pos[0], pos[1])
    goal = self.man_goal[value]
    m = self.get_xy(pos[0])
    m2 = self.get_xy(pos[1])
    print("m and m2: ", m , m2)
    y = abs(m[0] - goal[0])
    x = abs(m[1] - goal[1])
    y2 = abs(m2[0] - goal[0])
    x2 = abs(m2[1] - goal[1])
    dist -= (x2 + y2)
    dist += (x + y)
    return (dist)
    # pass


  #   pass
  def manhatan_distance(self, matrix):
    l = len(matrix)
    dist = 0
    # dist = self.linear_conflict(matrix)
    for i in range(1, l):
      m = self.get_xy(matrix.index(i))
      goal = self.man_goal[i]
      y = abs(m[0] - goal[0])
      x = abs(m[1] - goal[1])
      dist += x + y
    return (dist)

  def count_conf(self, cur):
    rr = 0
    for i in cur:
      for j in cur[i:]:
        if (self.goal.index(i) > self.goal.index(j)): 
          rr += 2
    return rr

  def col_conflict(self, cur_col):
    rr = 0
    res = []
    for i in range(self.n):
      for cc in cur_col[i]:
        if cc in self.col[i]:
          res += [cc]
      rr += self.count_conf(res)
      res = []
    return rr

  def linear_conflict(self, matrix):
    cur_col  = [[matrix[i + (j * self.n)] for j in range(self.n)] for i in range(self.n)]
    # cur_row  = [[matrix[j + (i * self.n)] for j in range(self.n)] for i in range(self.n)]
    return self.col_conflict(cur_col)# + self.col_conflict(cur_row)


class Astar(Solver):

    def solve(self):
      # parents will be the closed list, containing the parent, the priority, the cost, and the direction 
      cost = 0
      tt = self.h(self.start)
      self.parents[str(self.start)] = (None, 0, 0, 0)
      open_list = p.pr()
      open_list.add(tt, cost, self.start, tt)
      while open_list:
        (old_f, cost, current, old_h) = open_list.get()
        cost += 1 
        if current == self.goal: 
          return self.print_solution(current)
        parent = self.parents[str(current)]
        direction = parent[3]
        for new_state in self.get_next_states(current, direction):
          hht = self.update_manhatan(new_state, old_h)
          hh = self.h(new_state[0])
          print("man and update: \t", hh, hht)
          self.print_matrix(new_state[0])
          time.sleep(0.1)
          priority = hh + cost
          if str(new_state[0]) not in self.parents:# and hh <= old_h + 2:
            # print(priority)
            open_list.add(priority, cost, new_state[0], hh)
            self.parents[str(new_state[0])] = (current, priority, cost, new_state[2])


class Idastar(Solver):
  def dfs(self, state, bound, cost = 0, direction = 5):
    new_bound = 99999999
    self.start = state
    b = 0
    if self.h(state) == 0:
      self.path += [state]
      self.solved = 1
      return 0
    cost += 1
    for ns in self.get_states(state, direction):
      if cost + self.h(ns[0]) <= bound:
        b = cost +  self.dfs(ns[0], bound - cost, cost, ns[2])
      else:
        b = cost + self.h(ns[0])
      if self.solved:
        self.path += [state]
        return b
      new_bound = min(new_bound, b)
    return new_bound


  def get_states(self, mtx, direction = 5):#direction
    n = self.n
    pos = mtx.index(0)
    if direction == 1 or direction == 3:
      if  direction != 4 and pos > n - 1:
       yield (self.swap(pos, pos - n, mtx),pos, 2)
      if  direction != 2 and pos < self.length - self.n:
        yield (self.swap(pos, pos + n, mtx),pos, 4)
      if  direction != 1 and pos < self.length and (pos + 1) % n: 
        yield (self.swap(pos, pos + 1, mtx),pos, 3)
      if  direction != 3 and pos > 0 and pos % n:
       yield (self.swap(pos, pos - 1, mtx),pos, 1)
    else:
      if  direction != 1 and pos < self.length and (pos + 1) % n: 
        yield (self.swap(pos, pos + 1, mtx),pos, 3)
      if  direction != 3 and pos > 0 and pos % n:
       yield (self.swap(pos, pos - 1, mtx),pos, 1)
      if  direction != 4 and pos > n - 1:
       yield (self.swap(pos, pos - n, mtx),pos, 2)
      if  direction != 2 and pos < self.length - self.n:
        yield (self.swap(pos, pos + n, mtx),pos, 4)


  # def it_dfs(self, state, bound, cost = 0, direction = 5):#iterative dfs, not fully implemented yet
  #   open_list = []
  #   new_bound = 99999999
  #   open_list.append(state)
  #   while open_list:
  #     state = open_list[-1]
  #     cost += 1
  #     for ns in self.get_next_states(state, direction):
  #       new_bound = min(new_bound, f)
  #       f = self.h(ns[0]) + cost
  #       if f <= bound:
  #         open_list.append(ns[0])
  #       if self.h(ns[0]) == 0:
  #         print("found a solution")
  #         for i in open_list:
  #           print(i)
  #         exit("")


  def solve(self):
    cost = 0
    current = self.start
    bound = self.h(self.start)
    print("Initial bound", bound)
    while True:
      r = self.dfs(current, bound)
      if self.solved:
        print("GOAL FOUND", r)
        jj = 0
        for i in self.path[::-1]:
          jj += 1
        print(jj - 1)
        return (0)
      elif r == -1:
        exit("PROBL")
      else:
        bound = r

    pass

