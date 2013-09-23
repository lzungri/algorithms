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
    for i in reversed(range(len(elements) - 1)):
        swapped = False
        for j in range(i + 1):
            if elements[j] > elements[j+1]:
                elements[j], elements[j+1] = elements[j+1], elements[j]
                swapped = True
        if not swapped:
            return elements
    return elements

# TODO: Create a test case

print inplace_sort([3,1,5,9,2,7,8])
print inplace_sort([3,1,5,4,7,9,8])
print inplace_sort([3,1])
print inplace_sort([])
print inplace_sort([3])
print inplace_sort([0,3,1,1,5,4,1,7,9,8])
print inplace_sort([3,3,5,9,8,1,1])
