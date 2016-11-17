# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    pr_queue.py                                        :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: rbaum <rbaum@student.42.fr>                +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2016/11/14 02:57:55 by rbaum             #+#    #+#              #
#    Updated: 2016/11/14 02:57:56 by rbaum            ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from heapq import heappop, heappush

# priority queue

class pr:
  def __init__(self):
    self.q = []

    # item being the matrix, f the sum of h + g, c being the cost(aka, g)
  def add(self, f, item, c):
    heappush(self.q, (f, item, c))

  def get(self):
    return heappop(self.q)[1]

  def look(self):
    return (self.q[0])

  def __len__(self):
    return (len(self.q))



