arr=[1,3,5,7,9,11,13,15,17]
target=13

cost=0

def dls_search(arr, target, max_level, current_level=0, root_index=0):
    global cost
    cost+=1

    
    if root_index<len(arr) and current_level<max_level:

        
        print(arr[root_index])

        if (arr[root_index]==target):
            print("Element found at level: ", current_level)

            return True


        current_level+=1

        left= dls_search(arr, target, max_level, current_level, 2*root_index+1)


        if left:
            return True

        cost-=1

        right=dls_search(arr, target, max_level, current_level, 2*root_index+2)

        if right:

            return True


    return False


if not dls_search(arr, target, 3):
    print("Element not found in the given depth")

