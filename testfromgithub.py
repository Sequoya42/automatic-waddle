import sys
import heapq
import verify

def manhattan_distance(current, goal, s):
  distance = 0
  
  for i in current:
    if i is not 0:
      g_i = goal.index(i)
      c_i = current.index(i)
      res_x = abs(g_i % s.size - c_i % s.size)
      res_y = abs(g_i / s.size - c_i / s.size)
      distance += res_x + res_y

  return distance

class search_algorithm:

  def __init__(self, initial, goal, size):
    self.initial = initial
    self.previous = initial
    self.current = initial
    self.goal = goal
    self.size = size
    self.solution = []
    self.h = manhattan_distance
    self.total_set = 0
    self.max_set = 0

  def is_goal(self, state):
    for i in range(self.size * self.size):
      if self.goal[i] != -1 and self.goal[i] != state[i]:
        return False
    return True 

  def get_next_states(self, current_state, size):
    def get_moves():
      x = i % size
      y = i / size
      moves = []
      if (x + 1 < size):
        moves.append((x + 1) + ((y) * size))
      if (y + 1 < size):
        moves.append((x) + ((y + 1) * size))
      if (x > (0)):
        moves.append((x - 1) + ((y) * size))
      if (y > (0)):
        moves.append((x) + ((y - 1) * size))
      return moves

    def get_states(moves):
      states = []
      for move in moves:
        states.append(current_state[:])
        states[-1][move], states[-1][i] = states[-1][i], states[-1][move]
        if states[-1] == self.previous:
          del states[-1]
      return states

    def prioritize_states(states):
      def by_heuristic(state):
        return self.h(state, self.goal, self)

      return sorted(states, key=by_heuristic)

    i = self.current.index(0)
    moves = get_moves()
    states = get_states(moves)
    return prioritize_states(states)

class PriorityQueue:

  def __init__(self):
    self.elements = []
  
  def empty(self):
      return len(self.elements) == 0
  
  def put(self, item, priority):
      heapq.heappush(self.elements, (priority, item))

  def get(self):
      return heapq.heappop(self.elements)[1]

class A_star(search_algorithm):
    #   self.initial = initial
    # self.previous = initial
    # self.current = initial
    # self.goal = goal
    # self.size = size
    # self.solution = []
    # self.h = manhattan_distance
    # self.total_set = 0
    # self.max_set = 0

  def solve(self):
      opened = PriorityQueue()
      opened.put(self.initial, 0)
      came_from = {}
      cost_so_far = {}
      came_from[str(self.initial)] = None
      cost_so_far[str(self.initial)] = 0

      while not opened.empty():
          current = self.current = opened.get()
          self.previous = came_from[str(current)]
          
          if self.is_goal(current):
            break 
          
          for next in self.get_next_states(current, self.size):
              new_cost = cost_so_far[str(current)] + 1
              if str(next) not in cost_so_far or new_cost < cost_so_far[str(next)]:
                  cost_so_far[str(next)] = new_cost
                  priority = new_cost + self.h(next, self.goal, self)
                  opened.put(next, priority)
                  self.total_set += 1
                  if self.max_set < len(opened.elements):
                    self.max_set = len(opened.elements)
                  came_from[str(next)] = current
      
      if not self.is_goal(self.current):
        print ("Unsolvable puzzle")
        return -1

      return self.get_solution(came_from, self.initial, self.goal)

  def get_solution(self, came_from, start, goal):
    current = self.current
    self.solution = [current]
    while current != start:
        current = came_from[str(current)]
        self.solution.append(current)
    self.solution = self.solution[::-1]
    return self



def get_map(argv):
  try: 
    with open(argv[1]) as f: 
      l = [line.strip() for line in f if line[0] is not '#']
    return (l)
  except Exception as error:
    exit("Invalid file")



def main(argv):
  given = get_map(argv)
  n = int(given[0])
  given = given[1:]
  initial_state = [int(x) if x is not '0' else n*n for l in given for x in l.split()]
  start = None
  goal_state = verify.spiral_matrix(n)
  solver = A_star(initial_state, goal_state, n*n)
  k = solver.solve()
  print(k)


main(sys.argv)