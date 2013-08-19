# Input: array of n elements
# Output: the same array of n elements sorted
# Example:
# [3,1,5,9,2,7,8]
# [1,3,5,9,2,7,8]
# [1,3,5,9,2,7,8]
# [1,3,5,2,9,7,8]
# [1,3,5,2,7,9,8]
# [1,3,5,2,7,8,9]
# [1,3,5,2,7,8,9]
# [1,3,5,2,7,8,9]
# [1,3,2,5,7,8,9]
# [1,3,2,5,7,8,9]
# [1,2,3,5,7,8,9]

def inplace_sort(elements):
    for i in range(len(elements) - 1):
        for j in range(len(elements) - i - 1):
            j_value = elements[j]
            next_j_value = elements[j+1]
            if j_value > next_j_value:
                elements[j], elements[j+1] = next_j_value, j_value
    return elements

print inplace_sort([3,1,5,9,2,7,8])
print inplace_sort([3,1,5,4,7,9,8])
print inplace_sort([3,1])
print inplace_sort([])
print inplace_sort([3])
print inplace_sort([0,3,1,1,5,4,1,7,9,8])
print inplace_sort([3,3,5,9,8,1,1])
