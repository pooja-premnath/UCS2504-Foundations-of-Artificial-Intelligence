import math
start_state = int(input("Enter the starting value: "))
levels = int(input("Enter the number of levels in the tree: "))


total_nodes = (2 ** levels) - 1

tree = [0 for i in range(total_nodes)]


tree[0] = start_state
index = 0

while index < len(tree):
    left_child_index = 2 * index + 1
    right_child_index = 2 * index + 2

    if left_child_index < len(tree):
        tree[left_child_index] = 2 * tree[index] + 1

    if right_child_index < len(tree):
        tree[right_child_index] = 2 * tree[index] + 2

    index += 1

print(tree)




for i in range(len(tree)-1,0,-2):
    current=tree[i]
    pair_current= tree[i-1]
    parent_index= (i-2)//2
    
    current_level=int(math.log(i,2))

    print(current_level)
    print(current, pair_current)

    if current_level%2==0:
        tree[parent_index]=max(current, pair_current)
        print("Maximized value at parent", tree[parent_index])


    else:
        tree[parent_index]=min(current, pair_current)
        print("Minimized value at parent", tree[parent_index])

print(tree[0])

        
    
    
    
    
