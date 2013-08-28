# Input: array of n elements
# Output: the same array of n elements sorted
# Example:
# [3,1,5,2,7,9,8] -> [1,2,3,5,7,8,9]
# [1,3,5,2,7,9,8]
# [1,2,3,5,7,9,8]

def inplace_sort(elements):
    for index_to_sort in range(1, len(elements)):
        value_to_sort = elements[index_to_sort]
        
        current_index = index_to_sort - 1
        while current_index >= 0 and elements[current_index] > value_to_sort:
            elements[current_index + 1] = elements[current_index]
            current_index -= 1

        elements[current_index + 1] = value_to_sort
    
    return elements

print inplace_sort([3,1,5,4,7,9,8])
print inplace_sort([3,1])
print inplace_sort([])
print inplace_sort([3])
print inplace_sort([0,3,1,1,5,4,1,7,9,8])
print inplace_sort([3,3,5,9,8,1,1])
