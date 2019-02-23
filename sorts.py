import random


def bubble_sort(numbers, comparisons, swaps, i, pass_swaps):
    swapped = None
    sorting = True
    comparisons += 1
    compared = (i, i + 1)
    if numbers[i] > numbers[i + 1]:
        x = numbers[i + 1]
        numbers[i + 1] = numbers[i]
        numbers[i] = x
        pass_swaps += 1
        swaps += 1
        swapped = compared

    if i < len(numbers) - 2:
        i += 1
    else:
        if pass_swaps == 0:
            sorting = False
        i = 0
        pass_swaps = 0

    return numbers, comparisons, swaps, (i, pass_swaps), compared, swapped, sorting


def selection_sort(numbers, comparisons, swaps, base_i, i, min_i):
    compared = None
    swapped = None
    sorting = True
    if base_i < len(numbers):
        if i < len(numbers):
            comparisons += 1
            compared = (i, min_i)
            if numbers[i] <= numbers[min_i]:
                min_i = i
            i += 1
        elif min_i != base_i:
            x = numbers[min_i]
            numbers[min_i] = numbers[base_i]
            numbers[base_i] = x

            swaps += 1
            swapped = (min_i, base_i)
            base_i += 1
            i = base_i
            min_i = base_i
        else:
            base_i += 1
            i = base_i
            min_i = base_i
    else:
        sorting = False

    return numbers, comparisons, swaps, (base_i, i, min_i), compared, swapped, sorting


def insertion_sort(numbers, comparisons, swaps, i, next_i):
    compared = None
    swapped = None
    sorting = True
    if i + 1 < len(numbers):
        if i >= 0:
            comparisons += 1
            compared = (i, i+1)
            if numbers[i + 1] < numbers[i]:
                x = numbers[i + 1]
                numbers[i + 1] = numbers[i]
                numbers[i] = x
                swaps += 1
                swapped = compared
            i -= 1
        else:
            i = next_i
            next_i += 1
    else:
        sorting = False

    return numbers, comparisons, swaps, (i, next_i), compared, swapped, sorting


def merge_sort(numbers, comparisons, swaps, size, start_left, end, left, right, merge):
    referenced = None
    appended = None
    sorting = True
    if size < len(numbers):
        if start_left + size < len(numbers):
            if not merge:
                start_right = start_left + size
                end = min(start_right + size, len(numbers))

                left = numbers[start_left:start_right]
                right = numbers[start_right:end]

            if left and right:
                comparisons += 1
                if left[0] < right[0]:
                    merge.append(left[0])
                    left = left[1:]
                else:
                    merge.append(right[0])
                    right = right[1:]
                numbers[start_left + len(merge) - 1] = merge[-1]
                swaps += 1
                referenced = (start_left, end - 1)
                appended = (start_left + len(merge) - 1, start_left + len(merge) - 1)
            elif left:
                merge.append(left[0])
                left = left[1:]
                numbers[start_left + len(merge) - 1] = merge[-1]
                swaps += 1
                referenced = (start_left, end - 1)
                appended = (start_left + len(merge) - 1, start_left + len(merge) - 1)
            elif right:
                merge.append(right[0])
                right = right[1:]
                numbers[start_left + len(merge) - 1] = merge[-1]
                swaps += 1
                referenced = (start_left, end - 1)
                appended = (start_left + len(merge) - 1, start_left + len(merge) - 1)
            else:
                merge = []

            if not merge:
                start_left += 2 * size

        else:
            start_left = 0
            size *= 2
    else:
        sorting = False

    return numbers, comparisons, swaps, (size, start_left, end, left, right, merge), referenced, appended, sorting


def bogosort(numbers, comparisons, swaps, i, ordered):
    sorting = True
    compared = None
    if i < len(numbers) and ordered:
        compared = (i-1, i)
        comparisons += 1
        if numbers[i-1] > numbers[i]:
            ordered = False
        i += 1

    elif ordered:
        sorting = False

    else:
        i = 1
        ordered = True
        swaps += 1
        random.shuffle(numbers)

    return numbers, comparisons, swaps, (i, ordered), compared, sorting


def bogobogosort(numbers, comparisons, swaps, sublist_end, i, ordered):
    sublist = numbers[:sublist_end]
    sublist, comparisons, swaps, (i, ordered), compared, sorting = bogosort(sublist, i, ordered, comparisons, swaps)

    numbers = sublist + numbers[sublist_end:]
    if not sorting and sublist_end < len(numbers):
        sublist_end += 1
        ordered = False
        sorting = True

    return numbers, comparisons, swaps, (sublist_end, i, ordered), compared, sorting
