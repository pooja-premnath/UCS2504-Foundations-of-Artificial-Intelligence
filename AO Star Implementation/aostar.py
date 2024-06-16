#implementation of the Ao* algorithm


def update_costs(H, condition, weight):

    least_cost={}

    main_values= list(condition.keys())

    #reverse this list
    main_values.reverse()

    #iterate through this list:
    for key in main_values:

        current_condition=condition[key]

        #calculate the new cost
        computed_cost=cost(H, current_condition, weight)

        #update heuristic
        H[key]=min(list(computed_cost.values()))

        print("Updated heuristics", H)

        least_cost[key]=computed_cost

    return least_cost


#define a function to calculate the cost
def cost(H, condition, weight):

    cost={}

    if 'AND' in condition:
        and_nodes=condition['AND']
        and_path=' AND '.join(and_nodes)

        cost[and_path]= sum(H[node] + weight for node in and_nodes)


    if 'OR' in condition:
        or_nodes=condition['OR']
        or_path=' OR '.join(or_nodes)
        cost[or_path]=min(H[node] + weight for node in or_nodes)

        
    return cost


#define a function to compute the shortestpath
def shortest_path(start, updated_costs, weight):

    path=start

    if start in updated_costs.keys():

        min_cost=min(updated_costs[start].values())

        key=list(updated_costs[start].keys())

        value=list(updated_costs[start].values())

        index=value.index(min_cost)

        next_node=key[index].split()

        if len(next_node)==1:
            start=next_node[0]

            path += '->'+ shortest_path(start,updated_costs,weight)

        else:

            path+= '->' + key[index]

            start=next_node[0]

            path+= '[' + shortest_path(start,updated_costs,weight)
             
            start=next_node[-1]

            path+= shortest_path(start,updated_costs,weight) + ']'

    return path

            

        
#define the heuristic values
H={"A": 1, "B": 4, "C": 2, "D": 3, "E": 6, "F": 8, "G": 2, "H": 0, "I": 0, "J":0}

# define the and or conditions of the graph
conditions={"A": {"OR" : ["B"], "AND": ["C","D"]},
            "B": {"OR": ["E", "F"]},
            "C": {"OR" : ["G"], "AND": ["H", "I"]},
            "D": {"OR" : ["J"]}}



#create a function that updates the heuristic values
weight=1
start="A"


#create a function that updates the costs
updated_costs= update_costs(H,conditions, weight)

print(shortest_path(start, updated_costs, weight))
