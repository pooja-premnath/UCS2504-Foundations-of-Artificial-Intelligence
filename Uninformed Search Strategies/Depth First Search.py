import networkx as nx
import matplotlib.pyplot as plt

arr=[1,3,5,7,9,11,13,15,17,19]
target=12

cost=0

def dfs_search(arr, target, root_index=0):

    global cost
    global G
    global labels

    cost+=1

    if root_index<len(arr):

        print(arr[root_index])

        cost+=1

        if arr[root_index]==target:
            print("Element found!")
            
            return True


        left=dfs_search(arr,target,2*root_index+1)

        if left:
            return True
        
        cost-=1
        right=dfs_search(arr,target,2*root_index+2)

        if right:
            return True

        


    return False


if not dfs_search(arr, target):
    print("Element not found")




