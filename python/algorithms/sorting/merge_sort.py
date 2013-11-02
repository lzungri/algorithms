from unittest import TestCase

# Input: array of n elements
# Output: the same array of n elements sorted
# Example:
# |3,1,5,9,2,7,8,0|
# |3,1,5,9|2,7,8,0|
# |3,1|5,9|2,7|8,0|
# |3|1|5|9|2|7|8|0|
# |1,3|5,9|2,7|0,8|
# |1,3,5,9|0,2,7,8|
# |0,1,2,3,5,7,8,9|

def sort(array):
    aux_array = [None]*len(array)
    return mergesort2(array, aux_array, 0, len(array))

def mergesort2(array, aux_array, low, high):
    if high - low <= 1:
        return
    
    middle = (low + high) / 2
    mergesort2(array, aux_array, low, middle)
    mergesort2(array, aux_array, middle, high)

    for i in range(low, high):
        aux_array[i] = array[i]
    
    left = low
    right = middle
    current = low
    
    for current in range(low, high):
        if left >= middle or (right < high and aux_array[right] < aux_array[left]):
            array[current] = aux_array[right]
            right += 1
        else:
            array[current] = aux_array[left]
            left += 1


# Space complexity = O(n logn)
def merge_sort(elements):
    if len(elements) <= 1:
        return elements
    
    left = merge_sort(elements[:len(elements) / 2])
    right = merge_sort(elements[len(elements) / 2:])
    
    i, j = 0, 0

    merged = []
    for _ in range(len(elements)):
        if j >= len(right) or (i < len(left) and left[i] <= right[j]):
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
        
    return merged


class MergeSortTestCase(TestCase):
    def __assert_compare(self, elements, expected):
        self.assertEqual(merge_sort(elements), expected)
        
        sort(elements)
        self.assertEqual(elements, expected)
    
    def test(self):
        self.__assert_compare([3,1,5,9,2,7,8,0], [0,1,2,3,5,7,8,9])
        self.__assert_compare([3,1,5,4,7,9,8,0], [0,1,3,4,5,7,8,9])
        self.__assert_compare([3,1,5,4,7,9,8,1,0], [0,1,1,3,4,5,7,8,9])
        self.__assert_compare([3,1], [1,3])
        self.__assert_compare([3,1,2], [1,2,3])
        self.__assert_compare([], [])
        self.__assert_compare([1], [1])
        self.__assert_compare([1,1], [1,1])
        self.__assert_compare([0,3,1,1,5,4,1,7,9,8], [0,1,1,1,3,4,5,7,8,9])
        self.__assert_compare([3,3,5,9,8,1,1], [1,1,3,3,5,8,9])
        self.__assert_compare([1,0,3,4,2,7], [0,1,2,3,4,7])
