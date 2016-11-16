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
# class pr:
# 	def __init__(self):
# 		self.q = []

# 	def add(self, item):
# 		heappush(self.q, item)

# 	def get(self):
# 		return heappop(self.q)

# 	def look(self):
# 		return (self.q[0])

# 	def __len__(self):
# 		return (len(self.q))


# Use strings instead list
class State:
	def __init__(self, matrix, n, cost = 0, parent = None):
		self.mtx = matrix
		self.n = n
		self.length = (n*n) - 1
		self.parent = parent
		self.cost = cost

	def get_xy(self, value):
		y = value // self.n
		x = value % self.n
		return (y, x)

	def get_swapped(self, pos, new):
		ret = self.mtx[:]
		ret[pos], ret[new] = ret[new], ret[pos]
		return (ret)

	def get_next_states(self):
		mtx = self.mtx
		n = self.n
		pos = mtx.index(0)
		if pos > 0: yield self.get_swapped(pos, pos - 1)
		if pos > n: yield self.get_swapped(pos, pos - n)
		if pos < self.length: yield self.get_swapped(pos, pos + 1)
		if pos <= self.length - self.n + 1: yield self.get_swapped(pos, pos + n)
		return next
		

class Astar:
	def __init__(self, goal, initial, n):
		self.cur = initial
		self.goal = goal
		self.length = len(goal)
		self.n = n
		self.closed = set()


	def solve(self):
		open = p.pr()
		open.add((0, str(self.cur.mtx)))

		# while open:
		# 	current = open.get()
		# 	for i in current.get_next_states():
		# 		f = 1
		# 		# open.add((f, i))
		# 		misc.print_matrix(i, self.n)
		# print("and initial was:")
		# misc.print_matrix(self.cur.mtx, self.n)



	def f(self):
		f = self.g() + self.h()
		pass

	def get_xy(self, value):
		y = value // self.n
		x = value % self.n
		return (y, x)
		
	# heuristique
	def manhatan_distance(self):
		matrix = self.current
		goal = self.goal
		l = len(matrix)
		dist = 0
		for i in range(0, l):
			m = get_xy(matrix, i)
			f = get_xy(goal, i)
			y = abs(m[0] - f[0])
			x = abs(m[1] - f[1])
			dist += x + y
		return (dist)

	# g
	def cost(self):
		self.cost += 1