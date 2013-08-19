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

    
def partition_end_as_pivot2(elements, start, end):
    pivot_index = end - 1
    pivot_value = elements[pivot_index]
    
    current_pivot_index = start
    for j in range(start, end - 1):
        current_value = elements[j]
        if current_value <= pivot_value:
            elements[current_pivot_index], elements[j] = current_value, elements[current_pivot_index]
            current_pivot_index += 1
    
    current_pivot_index -= 1
    elements[pivot_index], elements[current_pivot_index] = elements[current_pivot_index], pivot_value
    
    return current_pivot_index


def inplace_sort(elements, start=None, end=None):
    start = 0 if start is None else start
    end = len(elements) if end is None else end
    
    if end - start <= 1:
        return elements, 0
    
#     print str(elements).replace(" ", "")[1:]
    pivot = partition_first_as_pivot(elements, start, end)
#     pivot = partition_end_as_pivot(elements, start, end)
#     pivot = partition_random_as_pivot(elements, start, end)
#     
#     print str(elements).replace(" ", "")[1:]
#     print "%ss" % ("  "*(start))
#     print "%s%d(%d)" % ("  "*(pivot), pivot, elements[pivot])
#     print "%se" % ("  "*(end))

    _, comp1 = inplace_sort(elements, start, pivot)
    _, comp2 = inplace_sort(elements, pivot + 1, end)

    return elements, end - start - 1 + comp1 + comp2



def compare(orig, expected):
    sorted_list, comparisons = inplace_sort(orig)
    print "orig: %s, comp: %s" % ([], comparisons)
    if sorted_list != expected:
        print "\tsorted: %s" % (sorted_list)
        print "\texpecd: %s" % (expected)

compare([3,1,5,9,2,7,8,0], [0,1,2,3,5,7,8,9])
compare([3,1,5,4,7,9,8,0], [0,1,3,4,5,7,8,9])
compare(map(int, open("resources/QuickSort.txt", "r")), [])


print "END"
