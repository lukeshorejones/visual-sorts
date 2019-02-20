import random


def bubble_sort(numbers, i, pass_swaps, comparisons, swaps, sorting):
    comparisons += 1
    if numbers[i] > numbers[i + 1]:
        x = numbers[i + 1]
        numbers[i + 1] = numbers[i]
        numbers[i] = x
        pass_swaps += 1
        swaps += 1

    if i < len(numbers) - 2:
        i += 1
    else:
        if pass_swaps == 0:
            sorting = False
        i = 0
        pass_swaps = 0

    return numbers, i, pass_swaps, comparisons, swaps, sorting


def insertion_sort(numbers, i, next_i, comparisons, swaps, sorting):
    comparisons += 1
    if i + 1 < len(numbers):
        if i >= 0:
            if numbers[i + 1] < numbers[i]:
                x = numbers[i + 1]
                numbers[i + 1] = numbers[i]
                numbers[i] = x
                swaps += 1
            i -= 1
        else:
            i = next_i
            next_i += 1
    else:
        sorting = False

    return numbers, i, next_i, comparisons, swaps, sorting


def merge_sort(current_list):
    if len(current_list) < 2:
        return current_list

    centre = len(current_list)//2
    left = current_list[:centre]
    right = current_list[centre:]

    left = merge_sort(left)
    right = merge_sort(left)

    sorted_list = []
    while left != [] and right != []:
        if left[0] < right[0]:
            sorted_list.append(left[0])
            left.remove(left[0])
        else:
            sorted_list.append(right[0])
            right.remove(right[0])

    if left != []:
        sorted_list = sorted_list + left
    else:
        sorted_list = sorted_list + right

    return sorted_list

def bogosort(numbers):
    ordered = False
    while not ordered:
        ordered = True
        for i in range(1, len(numbers)):
            if numbers[i-1] > numbers[i]:
                ordered = False
                break
        
        if not ordered:
            random.shuffle(numbers)
            
            time.sleep(delay)
            update_canvas(numbers)

    return numbers


def bogobogosort(numbers):
    global sublists_sorted

    while sublists_sorted < len(current_list)-1:
        sublist = current_list[:sublists_sorted+2]
        bogobogoloop(sublist, current_list)
        
        current_list[:sublists_sorted+2] = sublist
        sublists_sorted += 1

        time.sleep(delay)
        update_canvas(current_list)
    
    return current_list


def bogobogoloop(sublist, current_list):
    global sublists_sorted
    ordered = False
    while not ordered:
        ordered = True
        for i in range(1, len(sublist)):
            if sublist[i-1] > sublist[i]:
                ordered = False
                break
        
        if not ordered:
            random.shuffle(sublist)
            
            temp_list = current_list
            temp_list[:sublists_sorted+2] = sublist

            time.sleep(delay)
            update_canvas(temp_list)

    return current_list