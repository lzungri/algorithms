from unittest import TestCase


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


def quickselect(elements, pos):
    if pos >= len(elements):
        raise IndexError()
    
    if not elements:
        return None
    return __quickselect(elements, pos, 0, len(elements))


def __quickselect(elements, pos, start=None, end=None):
    if end - start <= 1:
        return elements[start] 
    
    pivot = partition_first_as_pivot(elements, start, end)
    if pivot == pos:
        return elements[pivot]
    if pivot > pos:
        return __quickselect(elements, pos, start, pivot)
    return __quickselect(elements, pos, pivot+1, end)


def median(elements):
    return quickselect(elements, len(elements) / 2)


class Test(TestCase):
    
    def test(self):
        self.assertRaises(IndexError, quickselect, [], 0)
        self.assertEqual(quickselect([11], 0), 11)
        self.assertEqual(quickselect([10,2,3,5,8,11], 2), 5)
        self.assertEqual(quickselect([10,2,3,5,8,11], 0), 2)
        self.assertEqual(quickselect([10,2,3,5,8,11], 1), 3)
        self.assertEqual(quickselect([10,2,3,5,8,11], 3), 8)
        self.assertEqual(quickselect([10,2,3,5,8,11], 4), 10)
        self.assertEqual(quickselect([10,2,3,5,8,11], 5), 11)
        self.assertEqual(quickselect(range(100)[::-1], 50), 50)
        
    def test_median(self):
        self.assertEqual(median([10,2,3,5,8,11,13]), 8)
        self.assertEqual(median([10,2,3,5,8,11]), 8)
