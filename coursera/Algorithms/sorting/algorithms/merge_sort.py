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

def inplace_sort(elements):
    return merge_sort(elements)

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

def compare(orig, expected):
    sorted_list = inplace_sort(orig)
    if sorted_list != expected:
        print "orig: %s" % orig
        print "\tsorted: %s" % (sorted_list)
        print "\texpecd: %s" % (expected)

compare([3,1,5,9,2,7,8,0], [0,1,2,3,5,7,8,9])
compare([3,1,5,4,7,9,8,0], [0,1,3,4,5,7,8,9])
compare([3,1,5,4,7,9,8,1,0], [0,1,1,3,4,5,7,8,9])
compare([3,1], [1,3])
compare([3,1,2], [1,2,3])
compare([], [])
compare([1], [1])
compare([1,1], [1,1])
compare([0,3,1,1,5,4,1,7,9,8], [0,1,1,1,3,4,5,7,8,9])
compare([3,3,5,9,8,1,1], [1,1,3,3,5,8,9])
compare([1,0,3,4,2,7], [0,1,2,3,4,7])

print "END"
