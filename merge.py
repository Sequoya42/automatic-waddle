# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    merge.py                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: rbaum <rbaum@student.42.fr>                +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2016/11/14 02:57:20 by rbaum             #+#    #+#              #
#    Updated: 2016/11/14 02:57:23 by rbaum            ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

def merge_sort(m, c):
    if len(m) < 2:
        return m, c
    middle = len(m) // 2
    (left, c) = merge_sort(m[:middle], c)
    (right, c) = merge_sort(m[middle:], c)
    return (merge(left, right, c))


def merge(left, right, c):
    res = []
    i, j = 0, 0
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            res.append(left[i])
            i += 1
        else:
            res.append(right[j])
            j += 1
            c += len(left) - i
    res += left[i:]
    res += right[j:]
    return res, c
