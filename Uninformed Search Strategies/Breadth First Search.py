import networkx as nx
import matplotlib.pyplot as plt

def bfs_search(array, target):

    index=0
    found=False
    labels={}
    cost=0

    G=nx.DiGraph()


    while index<len(arr):
        current_node=arr[index]

        left_child_ind=(2*index)+1
        right_child_ind=(2*index)+2

        if left_child_ind<len(arr):
            left_child=arr[left_child_ind]
            print(left_child)
            G.add_edge(current_node,left_child)
            labels[left_child]=f'{left_child}'

            if left_child==target:
                print("Element found")
                found=True
                break


        if right_child_ind<len(arr):
            right_child=arr[right_child_ind]
            print(right_child)
            G.add_edge(current_node,right_child)
            labels[right_child]=f'{right_child}'

            if right_child==target:
                print("Element found")
                found=True
                break


        index+=1

        if not found:
            print("Element not found")


    nx.draw(G,with_labels=True, labels=labels)
    plt.show()

arr=[1,3,5,7,9,11,13,15,17,19]
target=17

bfs_search(arr,target)


        
