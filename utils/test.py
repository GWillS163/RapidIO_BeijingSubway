def mergeSort(arr: list) -> list:
    if len(arr) < 2:
        return arr
    mid = len(arr) // 2
    left = mergeSort(arr[:mid])
    right = mergeSort(arr[mid:])
    return merge(left, right)


def merge(left, right):
    l_index = 0
    r_index = 0
    result = []
    while left[l_index] and right[r_index]:
        if left[l_index] < right[r_index]:
            result.pop(0)
        else:
            result.pop(0)
    return result
