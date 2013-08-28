import time

def benchmark(callable, *args):
    start_time = time.time()
    try:
        return callable(*args)
    finally:
        print "\ttime: %s" % (time.time() - start_time)

def bruteforce_count_inversions(integers):
    count = 0
    for i in range(len(integers)):
        for j in range(i+1, len(integers)):
            if i < j and integers[i] > integers[j]:
                count += 1
    return count

print benchmark(bruteforce_count_inversions, [1,0,3,4,2,7])
print benchmark(bruteforce_count_inversions, [1,0])
print benchmark(bruteforce_count_inversions, [])
print benchmark(bruteforce_count_inversions, [2,0,1])
print benchmark(bruteforce_count_inversions, [2,0,1,5,3,4])
print benchmark(bruteforce_count_inversions, [2,2,3])
print benchmark(bruteforce_count_inversions, [3,2,2])
print benchmark(bruteforce_count_inversions, map(int, open("resources/SmallIntegerArray.txt", "r")))
# print bruteforce_count_inversions(map(int, open("resources/IntegerArray.txt", "r")))

# total time: 2.8133392334e-05
# 7
# total time: 3057.58431411
# 2407905288


def count_inversions(elements):
    if len(elements) <= 1:
        return (elements, 0)

    left, left_count = count_inversions(elements[:len(elements) / 2])
    right, right_count = count_inversions(elements[len(elements) / 2:])

    print "(%s) left %s" % (left_count, left)
    print "(%s) right %s" % (right_count, right)

    merged = []
    merge_count = 0
    li = 0
    ri = 0
    for _ in range(len(elements)):
        if ri >= len(right) or (li < len(left) and left[li] <= right[ri]):
            merged.append(left[li])
            li += 1
        else:
            merged.append(right[ri])
            ri += 1
            if li < len(left):
                merge_count += len(left) - li
    
    return (merged, merge_count + left_count + right_count)

        

print benchmark(count_inversions, [1,0,3,4,2,7])
print benchmark(count_inversions, [1,0])
print benchmark(count_inversions, [])
print benchmark(count_inversions, [2,0,1])
print benchmark(count_inversions, [2,0,1,5,3,4])
print benchmark(count_inversions, [2,2,3])
print benchmark(count_inversions, [3,2,2])
print benchmark(count_inversions, map(int, open("resources/SmallIntegerArray.txt", "r")))
print benchmark(count_inversions, map(int, open("resources/IntegerArray.txt", "r")))[1]
