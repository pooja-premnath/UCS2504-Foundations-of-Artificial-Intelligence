arr = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]
target = 12
cost = 0


def ids_search(arr, target, max_level, root_index=0, current_level=0):
    global cost

    cost += 1

    if root_index < len(arr) and current_level < max_level:
        print(arr[root_index])

        if arr[root_index] == target:
            print("Element found, ", end=" ")
            return True

        current_level += 1

        left = ids_search(arr, target, max_level, 2 * root_index + 1, current_level)
        if left:
            return True

        cost -= 1

        right = ids_search(arr, target, max_level, 2 * root_index + 2, current_level)
        if right:
            return True

    return False


max_level = 2
status = False

while not status:
    if not ids_search(arr, target, max_level):
        print("Element not found at level:", max_level)
        response = input("Enter 'y' to increase depth, or any other key to stop: ")
        if response.lower() == 'y':
            max_level += 1
            print("\nIncreasing depth to", max_level)
        else:
            status = True
    else:
        print("Level= ", max_level)
        status = True
