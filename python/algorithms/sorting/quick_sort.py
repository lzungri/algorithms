import random
from unittest import TestCase

# Input: array of n elements
# Output: the same array of n elements sorted
# Example:
# [3,1,5,9,2,7,8] Pivot=5
# [ij3,1,5,9,2,7,8]
# [3,ij1,5,9,2,7,8]
# [3,1,5,ij9,2,7,8]
# [3,1,5,i9,j2,7,8]
# [3,1,5,2,i9,j7,8]
# [3,1,5,2,i9,7,j8]
# [3,1,2,5,i9,7,8]


def partition_first_as_pivot(elements, start, end):
    pivot_index = start
    pivot_value = elements[pivot_index]
    
    current_pivot_index = start + 1
    for j in range(start + 1, end):
        current_value = elements[j]
        if current_value <= pivot_value:
            elements[current_pivot_index], elements[j] = current_value, elements[current_pivot_index]
            current_pivot_index += 1
    
    current_pivot_index -= 1
    elements[pivot_index], elements[current_pivot_index] = elements[current_pivot_index], pivot_value
    
    return current_pivot_index


def partition_end_as_pivot(elements, start, end):
    elements[start], elements[end - 1] = elements[end - 1], elements[start]
    return partition_first_as_pivot(elements, start, end)


def partition_random_as_pivot(elements, start, end):
    pivot_index = random.randrange(start, end)
    pivot_value = elements[pivot_index]
    
    current_pivot_index = start
    for j in range(start, end):
        current_value = elements[j]
        if current_value <= pivot_value:
            elements[current_pivot_index], elements[j] = current_value, elements[current_pivot_index]

            if current_pivot_index == pivot_index:
                pivot_index = j
            
            if j == pivot_index:
                pivot_index = current_pivot_index
                
            current_pivot_index += 1
        
    current_pivot_index -= 1
    elements[pivot_index], elements[current_pivot_index] = elements[current_pivot_index], pivot_value
    
    return current_pivot_index


def inplace_sort(elements, start=None, end=None):
    start = 0 if start is None else start
    end = len(elements) if end is None else end
    
    if end - start <= 1:
        return
    
    pivot = partition_first_as_pivot(elements, start, end)
#     pivot = partition_end_as_pivot(elements, start, end)
#     pivot = partition_random_as_pivot(elements, start, end)

    inplace_sort(elements, start, pivot)
    inplace_sort(elements, pivot + 1, end)

    return



class QuickSortTestCase(TestCase):
    def __assert_compare(self, original, expected):
        inplace_sort(original)
        self.assertEqual(original, expected)

    def test(self):
        self.__assert_compare([3,1,5,9,2,7,8,0], [0,1,2,3,5,7,8,9])
        self.__assert_compare([3,1,5,4,7,9,8,0], [0,1,3,4,5,7,8,9])
        self.__assert_compare([3,1,5,4,7,9,8,1,0], [0,1,1,3,4,5,7,8,9])
        self.__assert_compare([3,1], [1,3])
        self.__assert_compare([3,1,2], [1,2,3])
        self.__assert_compare([], [])
        self.__assert_compare([1], [1])
        self.__assert_compare([1,1], [1,1])
        self.__assert_compare([1,1,1,3,0], [0,1,1,1,3])
        self.__assert_compare([0,3,1,1,5,4,1,7,9,8], [0,1,1,1,3,4,5,7,8,9])
        self.__assert_compare([3,3,5,9,8,1,1], [1,1,3,3,5,8,9])
        self.__assert_compare([1,0,3,4,2,7], [0,1,2,3,4,7])
