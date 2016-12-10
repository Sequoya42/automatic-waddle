# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Rbfs.py                                            :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: rbaum <rbaum@student.42.fr>                +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2016/12/07 02:16:00 by rbaum             #+#    #+#              #
#    Updated: 2016/12/07 02:16:01 by rbaum            ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import solve, math, time

class Rbfs(solve.Solver):

  def expand(self, mtx, cost, direction = 5):#direction
    n = self.n
    best = []
    pos = mtx.index(0)
    # best += (f, F, mtx, pos, dir)
    if direction != 1 and pos < self.length and (pos + 1) % n: 
      swapped = self.swap(pos, pos + 1, mtx) 
      f = self.h(swapped) + cost
      best += [[f, f, swapped, (pos, pos + 1), 3]]
    if direction != 3 and pos > 0 and pos % n: 
      swapped = self.swap(pos, pos - 1, mtx)
      f = self.h(swapped) + cost
      best += [[f, f, swapped, (pos, pos - 1), 1]]
    if direction != 4 and pos > n - 1: 
      swapped = self.swap(pos, pos - n, mtx) 
      f = self.h(swapped) + cost
      best += [[f, f, swapped, (pos, pos - n), 2]]
    if direction != 2 and pos < self.length - self.n: 
      swapped = self.swap(pos, pos + n, mtx)
      f = self.h(swapped) + cost
      best += [[f, f, swapped, (pos, pos + n), 4]]
    best.sort(key = lambda e : e[0])
    return best

# tuple node_info = (f, F, n)
  def solve(self, node_info, bound, cost = 1, direction = 5):
    # print("solve", bound)
    node = node_info[2]
    # print(node)
    if self.solved == 1:
      print(node)
    if self.h(node) == 0:
      self.solved = 1
    children = self.expand(node, cost)
    if len(children) == 0:
      exit("PROBLEM")
    for c in children: 
      if node_info[0] < node_info[1]:
        c[1] = max(node_info[1], c[0])
    print("LEN", len(children))
    if len(children) < 2:
      print("HERE")
      n2 = (0, 9999999)
    else:
      n2 = children[1]
    n1 = children[0]
    print(n1[1], bound, n2[1], n1[0])
    print(n1[2])
    time.sleep(1)
    while n1[1] <= bound and n1[0] < 99999999 and self.solved == 0: #10 below
      n1 = self.solve(n1, min(bound, n2[1]), cost + 1, n1[4])
    print("AFTERWHILE", bound)
    if self.solved == 1:
      self.print_matrix(node)
    return n1



# --------------------------------------------------
# RBFS(n, B)
# 1. if n is a goal
# 2. solution ← n; exit()
# 3. C ← expand(n)
# 4. if C is empty, return ∞
# 5. for each child ni in C
# 6. if f(n) < F(n) then F(ni) ← max(F(n), f(ni))
# 7. else F(ni) ← f(ni)
# 8. (n1, n2) ← bestF(C)
# 9. while (F(n1) ≤ B and F(n1) < ∞)
# 10. F(n1) ← RBFS(n1, min(B, F(n2)))
# 11. (n1, n2) ← bestF(C)
# 12. return F(n1)
# Figure 3

# --------------------------------------------------
# RBFS (node: N, value: F(N), bound: B)
# IF f(N)>B, return f(N)
# IF N is a goal, EXIT algorithm
# IF N has no children, RETURN infinity 
# FOR each child Ni of N,
# IF f(N)<F(N) THEN F[i] := MAX(F(N),f(Ni))
# ELSE F[i] := f(Ni)
# sort Ni and F[i] in increasing order of F[i]
# IF only one child, F[2] := infinity
# WHILE (F[I] <= B and F[I] < infinity)
# F[I] := RBFS(NI, F[I], MIN(B, F[2]))
# insert N1 and F[I] in sorted order
# return F[I]

# --------------------------------------------------
# class Ilbfs(solve.Solver): 
#   def solve(self):
#     cost = 0
#     self.parents[str(self.start)] = (None, self.dist, 0, 0)
#     open_list = p.pr()
#     open_list.add(self, dist, cost, self.start, self.dist)
#     while open_list:
#       (old_f, cost, current, old_h) = open_list.get()
#       cost += 1
#       if current == self.goal:
#         return self.print_solution(current)
#       parent = self.parents[str(current)]
#       direction = parent[3]
#       for new_state in self.get_next_states(current, direction):
#         hh = self.h(new_state[0])
#         priority = hh + cost # priority is f
#         if str(new_state[0]) not in self.parents:
#           open_list.add(priority, cost, new_state[0], hh)
#           self.parents[str(new_state[0])] = (current, priority, cost, new_state[2])


# RBFS ( node: N ,value: F(N), bound B)
# IF f( N) > B 
  # RETURN f(n)
# IF N is a goal,
   # EXIT algorithm
# IF N has no children, 
  # RETURN infinity FOR each child Ni of N, F[i] := f(Ni)
# IF f(N) < F(N) THEN F[i] := MAX (F(N), f(Ni)) ELSE F[i] := f(Ni)


# ----------------





# function NewF (N, F(N), Bound)
#  if F(N) > Bound then NewF := F(N)
#  else if goal(N) then exit search with success
#  else if N has no children then NewF := infinity – dead end
#  else for each child Nk of N do
# if f(N) < F(N) then F(Nk) := max( F(N), f(Nk))
#  else F(Nk) := f(Nk)
# sort children Nk in increasing order of F-value
# while F(N1) ≤ Bound and F(N1) < infinity do
#  Bound1 := min ( Bound, F-value of sibling N1)
#  F(N1) := NewF (N1, F(N1), Bound1)
#  reorder nodes N1, N2 , … according to new F(N1)
#  end
#  end
# NewF := F(N1)