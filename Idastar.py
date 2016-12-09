# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Idastar.py                                         :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: rbaum <rbaum@student.42.fr>                +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2016/11/30 18:44:59 by rbaum             #+#    #+#              #
#    Updated: 2016/11/30 18:44:59 by rbaum            ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import solve
from functools import lru_cache

class Idastar(solve.Solver):

  # def swap(self, pos, new, tmtx):
  #   mtx = list(tmtx) 
  #   ret = mtx[:]
  #   ret[pos], ret[new] = ret[new], ret[pos]
  #   return tuple(ret)


  # @lru_cache(maxsize=None)
  def dfs(self, state, bound, cost, direction):
    self.expanded += 1
    new_bound = 99999999
    if self.h(state) == 0:
      self.path += [state]
      self.solved = 1
      return 0
    for ns in self.get_next_states(state, direction):
      self.total += 1
      hh = self.h(ns[0])
      if cost + hh <= bound:
        b = self.dfs(ns[0], bound, cost + 1, ns[2])
      else: 
        b = cost + hh + 1
      if self.solved:
        self.path += [state]
        return b
      new_bound = min(new_bound, b)
    return new_bound


  def solve(self):
    print("Idastar")
    cost = 0
    current = self.start
    bound = self.h(self.start)
    print("Initial bound", bound)
    while True:
      r = self.dfs(current, bound, 0, 5)
      bound = r
      if self.solved:
        # print("GOAL FOUND", bound)
        jj = 0
        for i in self.path[::-1]:
          jj += 1
          # self.print_matrix(i)
        print("Length", jj - 1)
        print("Expanded:\t", self.expanded)
        print("Total : \t", self.total)
        return (0)

  # def it_dfs(self, state, bound, cost = 0, direction = 5):
  #   open_list = []
  #   new_bound = 99999999
  #   open_list.append(state)
  #   while open_list:
  #     pass

 
