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
    dist += self.update_conflict(matrix, pos[0], direction, dist, parent_state)
    # ll1 = self.linear_conflict(matrix)
    # ll2 = self.linear_conflict(parent_state)
    # print(ll1, ll2)
    # print("UPDATES\t\t", dist, lin, dist+lin, direction)
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
      # dist += lin
    else:
      lin = self.conflict(cur_col, self.col)
      lin2= self.conflict(old_col, self.col)
      # dist += lin
    # print("qeg3", lin, lin2)
    # self.print_matrix(matrix)
    # self.print_matrix(parent_state)
    # print("AND CUR COL AND OLD_COL")      
    # print(cur_col)
    # print(old_col)
    # exit(0)
    return (lin - lin2)



  def count_conf(self, cur):
    rr = 0
    # print(cur)
    for i in cur:
      for j in cur[i:]:
        if (self.goal.index(i) > self.goal.index(j)): 
          # print("Plus one", i, j)
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
    # print("RR IS ", rr)
    # if rr > 0:
    #   print(cur_col)
    return rr

  def linear_conflict(self, matrix):
    cur_col  = [[matrix[i + (j * self.n)] for j in range(self.n)] for i in range(self.n)]
    cur_row  = [[matrix[j + (i * self.n)] for j in range(self.n)] for i in range(self.n)]
    # self.print_matrix(self.start)
    # self.print_matrix(self.goal)
    # print(cur_col)
    # print(self.col)
    # x = self.conflict(cur_col, self.col)
    # print(x)
    # print(cur_row)
    # print(self.line)
    # y = self.conflict(cur_row, self.line)
    # print(y)
    # exit(0)
    return self.conflict(cur_col, self.col) + self.conflict(cur_row, self.line)

  # def linear_conflict(self, matrix):
  #   cur_row  = [[matrix[j + (i * self.n)] for j in range(self.n)] for i in range(self.n)]
  #   for i in cur_row:
  #     for j in cur_row[i]:
  #       if cur_row[i][j]

class Astar(Solver):

    def solve(self):
      # parents will be the closed list, containing the parent, the priority, the cost, and the direction 
      cost = 0
      self.parents[str(self.start)] = (None, 0, 0, 0)
      open_list = p.pr()
      open_list.add(self.dist, cost, self.start, self.dist)
      while open_list:
        (old_f, cost, current, old_h) = open_list.get()
        self.expanded += 1
        cost += 1 
        if current == self.goal:
          print("Len parent", len(self.parents))
          print("Len open:", self.expanded)
          return self.print_solution(current)
        parent = self.parents[str(current)]
        direction = parent[3]
        for new_state in self.get_next_states(current, direction):
          # print("\t\t\t\t\t\t\tfFOR", self.linear_conflict(current))
          hh = self.h(new_state[0])
          # hh = self.update_manhatan(old_h, new_state, current)
          # print(hh, hht)
          # time.sleep(0.1)
          priority = hh + cost
          if str(new_state[0]) not in self.parents:
            open_list.add(priority, cost, new_state[0], hh)
            self.parents[str(new_state[0])] = (current, priority, cost, new_state[2])


class Idastar(Solver):

  def get_states(self, mtx, direction = 5):#direction
    n = self.n
    pos = mtx.index(0)
    if direction == 1 or direction == 3:
      if  direction != 4 and pos > n - 1:
       yield (self.swap(pos, pos - n, mtx), (pos, pos - n), 2)
      if  direction != 2 and pos < self.length - self.n:
        yield (self.swap(pos, pos + n, mtx), (pos, pos + n), 4)
      if  direction != 1 and pos < self.length and (pos + 1) % n: 
        yield (self.swap(pos, pos + 1, mtx), (pos, pos + 1), 3)
      if  direction != 3 and pos > 0 and pos % n:
       yield (self.swap(pos, pos - 1, mtx), (pos, pos - 1), 1)
    else:
      if  direction != 1 and pos < self.length and (pos + 1) % n: 
        yield (self.swap(pos, pos + 1, mtx), (pos, pos + 1), 3)
      if  direction != 3 and pos > 0 and pos % n:
       yield (self.swap(pos, pos - 1, mtx), (pos, pos - 1), 1)
      if  direction != 4 and pos > n - 1:
       yield (self.swap(pos, pos - n, mtx), (pos, pos - n), 2)
      if  direction != 2 and pos < self.length - self.n:
        yield (self.swap(pos, pos + n, mtx), (pos, pos + n), 4)

  def dfs(self, state, bound, cost, direction, old_h):
    new_bound = 99999999
    self.start = state
    b = 0
    if self.h(state) == 0:
      self.path += [state]
      self.solved = 1
      return 0
    cost += 1
    for ns in self.get_states(state, direction):
      hh = self.update_manhatan(ns, old_h)
      if cost + hh <= bound:
        b = cost + self.dfs(ns[0], bound - cost, cost, ns[2], hh)
      else:
        b = cost + hh
      if self.solved:
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
      r = self.dfs(current, bound, 0, 5, self.dist)
      if self.solved:
        print("GOAL FOUND", r)
        jj = 0
        for i in self.path[::-1]:
          jj += 1
        print(jj - 1)
        return (0)
      elif r < 0:
        exit("PROBL")
      else:
        bound = r


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


class Nope(Solver):
      def solve(self):
        # parents will be the closed list, containing the parent, the priority, the cost, and the direction 
        cost = 0
        self.parents[str(self.start)] = (None, 0, 0, 0)
        open_list = p.pr()
        open_list.add(self.dist, cost, self.start, self.dist)
        while open_list:
          (old_f, cost, current, old_h) = open_list.get()
          self.expanded += 1
          cost += 1 
          if current == self.goal:
            print("Len parent", len(self.parents))
            print("Len open:", self.expanded)
            return self.print_solution(current)
          parent = self.parents[str(current)]
          direction = parent[3]
          for new_state in self.get_next_states(current, direction):
            # print("\t\t\t\t\t\t\tfFOR", self.linear_conflict(current))
            # hh = self.h(new_state[0])
            hh = self.update_manhatan(old_h, new_state, current)
            # print(hh, hht)
            # time.sleep(0.1)
            priority = hh + cost
            if str(new_state[0]) not in self.parents:
              open_list.add(priority, cost, new_state[0], hh)
              self.parents[str(new_state[0])] = (current, priority, cost, new_state[2])



class Bidira(Solver):
  pass