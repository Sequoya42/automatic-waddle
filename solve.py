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


1 2 3
4 9 6 -> -1 | + 1 | -n | + n
7 8 5

1 2 3 4
5 6 7 8
9 1 2 3
4 5 6 1

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
		ret = mtx[:]
		ret[pos], ret[new] = ret[new], ret[pos]
		return (ret)

	def get_next_states(self):
		next = []
		mtx = self.mtx
		n = self.n
		pos = mtx.find(0)
		if pos > 0: next += get_swapped(pos, pos - 1)
		if pos > n: next += get_swapped(pos, pos - n)
		if pos < self.length: next += get_swapped(pos, pos + 1)
		if pos <= self.length - self.n + 1: next += get_swapped(pos, pos + n)
		return next
		

class Astar:
	def __init__(self, goal, initial, n):
		self.state = initial
		self.goal = goal
		self.length = len(goal)
		self.n = n
		self.open = p.pr()
		self.closed = set()

	def add_states(self):
		pass
		# new_states = []
		# (y, x) = self.get_xy(0)


	def solve(self):
		self.open.add(self.cur)
		self.parent[self.cur] = None

		while open:
			current = open.get()
			add_states()


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