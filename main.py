# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    main.py                                            :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: rbaum <rbaum@student.42.fr>                +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2016/11/05 23:28:27 by rbaum             #+#    #+#              #
#    Updated: 2016/11/05 23:29:00 by rbaum            ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import sys
from verify import count_inversions, check_validity, print_2by2_matrix, spiral_matrix
import pr_queue

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
	matrix = [int(x) if x is not '0' else n*n for l in given for x in l.split()]
	spiral = spiral_matrix(n)
	check_validity(matrix, spiral, n)



if __name__ == '__main__':
  main(sys.argv)