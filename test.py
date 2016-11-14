import sys
from merge import merge_sort




# If the width is odd, then every solvable state has an even number of inversions.
# If the width is even, then every solvable state has
# an even number of inversions if the blank is on an odd numbered row counting from the bottom;
# an odd number of inversions if the blank is on an even numbered row counting from the bottom;

def yolo():
	i = "bla"
	j = 31
	z = 3
	for k in range(z, j):
		yield(k)
	yield(j)
	yield(i)
	return (3)


def main(argv):
	toto = yolo()
	print(toto[0])
	
# def main(argv):
# 	given = get_map(argv)
# 	n = int(given[0])
# 	given = given[1:]
# 	matrix = [[int(x) if x is not '0' else n*n for x in l.split()] for l in given]
# 	print_2by2_matrix(matrix, n)
# 	identity = [[int(i + 1 + (n *j)) for i in range(0, n)] for j in range(0, n)]
# 	print_2by2_matrix(identity, n)
# 	spiral = spiral_matrix(n)
# 	print_2by2_matrix(spiral, n)
# 	#
# 	check_validity(matrix, spiral, n)




# if __name__ == '__main__':
main(sys.argv)

# # List Comprehension 
# [word for sentence in text for word in sentence]


#   >> a = [[1, 2], [3, 4]]
# >>> [x for x in b for b in a]
# Traceback (most recent call last):
#   File "<stdin>", line 1, in <module>
# NameError: name 'b' is not defined




# >>> [x for b in a for x in b]
# [1, 2, 3, 4]
# >>> [x for x in b for b in a]
# [3, 3, 4, 4]