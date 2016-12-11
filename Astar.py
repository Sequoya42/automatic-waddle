# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Astar.py                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: rbaum <rbaum@student.42.fr>                +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2016/11/30 18:45:03 by rbaum             #+#    #+#              #
#    Updated: 2016/11/30 18:45:03 by rbaum            ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import solve
import pr_queue as p

class Astar(solve.Solver):

    def solve(self):
      print("Astar")
      # parents will be the closed list, containing the parent, the priority, the cost, and the direction 
      cost = 0
      self.parents[str(self.start)] = (None, self.dist, 0, 0)
      open_list = p.pr()
      open_list.add(self.dist, cost, self.start, self.dist)
      while open_list:
        self.expanded += 1
        (old_f, cost, current, old_h) = open_list.get()
        cost += 1
        if current == self.goal:
          return self.print_solution(current)
        parent = self.parents[str(current)]
        direction = parent[3]
        for new_state in self.get_next_states(current, direction): 
          self.total += 1
          # hh = self.update_manhatan(old_h, new_state, current)
          hh = self.h(new_state[0])
          priority = hh + cost#  + self.linear_conflict(new_state[0])
          # if heuristic precise enough (LC?) can use the and hh <= self.dist
          if str(new_state[0]) not in self.parents:
            open_list.add(priority, cost, new_state[0], hh)
            self.parents[str(new_state[0])] = (current, priority, cost, new_state[2])


