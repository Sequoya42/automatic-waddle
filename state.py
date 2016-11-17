# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    state.py                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: rbaum <rbaum@student.42.fr>                +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2016/11/15 05:37:30 by rbaum             #+#    #+#              #
#    Updated: 2016/11/15 05:37:31 by rbaum            ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import pr_queue as p

# class pr:
#   def __init__(self):
#     self.q = []

#   def add(self, item):
#     heappush(self.q, item)

#   def get(self):
#     return heappop(self.q)

#   def look(self):
#     return (self.q[0])

#   def __len__(self):
#     return (len(self.q))

class State:
  def __init__(self, parent=None, matrix):
    self.parent = parent
    self.matrix = matrix
    