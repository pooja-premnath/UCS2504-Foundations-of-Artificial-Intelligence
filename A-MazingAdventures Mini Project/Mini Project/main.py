import pygame
import time
import heapq
from priority_queue import PrioritySet, PriorityQueue, AStarQueue
from math import inf
import random
from collections import deque

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
LIGHT_BLUE = (0, 111, 255)
ORANGE = (255, 128, 0)
PURPLE = (128, 0, 255)
YELLOW = (255, 255, 0)
GREY = (143, 143, 143)
BROWN = (186, 127, 50)
DARK_GREEN = (0, 128, 0)
DARKER_GREEN = (0, 50, 0)
DARK_BLUE = (0, 0, 128)

# For creating Buttons
class Button:
    def __init__(self, color, x, y, width, height, text=''):
        self.color = color
        self.x = int(x)
        self.y = int(y)
        self.width = int(width)
        self.height = int(height)
        self.text = text

    def draw(self,win,outline=None):
        # Call this method to draw the Button on the screen
        if outline:
            pygame.draw.rect(win, outline, (self.x,self.y,self.width,self.height),0)
            
        pygame.draw.rect(win, self.color, (self.x+1,self.y+1,self.width-1,self.height-1),0)
        
        if self.text != '':
            font = pygame.font.SysFont('arial', 12)
            text = font.render(self.text, 1, (0,0,0))
            win.blit(text, (self.x + int(self.width/2 - text.get_width()/2), self.y + int(self.height/2 - text.get_height()/2)))

    def isOver(self, pos):
        # Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
            
        return False

# Make it easier to add different node types
class Node:

    nodetypes = ['blank', 'start', 'end', 'wall', 'mud', 'dormant']

    colors = {  'regular': {'blank': WHITE, 'start': RED, 'end': LIGHT_BLUE, 'wall': BLACK, 'mud': BROWN, 'dormant': GREY},
                'visited': {'blank': GREEN, 'start': RED, 'end': LIGHT_BLUE, 'wall': BLACK, 'mud': DARK_GREEN, 'dormant': GREY},
                'path': {'blank': BLUE, 'start': RED, 'end': LIGHT_BLUE, 'wall': BLACK, 'mud': DARK_BLUE, 'dormant': GREY}
            }

    distance_modifiers = {'blank': 1, 'start': 1, 'end': 1, 'wall': inf, 'dormant': inf}

    def __init__(self, nodetype, text='', colors=colors, dmf=distance_modifiers):
        self.nodetype = nodetype
        self.rcolor = colors['regular'][self.nodetype]
        self.vcolor = colors['visited'][self.nodetype]
        self.pcolor = colors['path'][self.nodetype]
        self.is_visited = True if nodetype == 'start' else True if nodetype == 'end' else False
        self.is_path = True if nodetype == 'start' else True if nodetype == 'end' else False
        self.distance_modifier = dmf[self.nodetype]
        self.color = self.pcolor if self.is_path else self.vcolor if self.is_visited else self.rcolor

    def update(self, nodetype=False, is_visited='unchanged', is_path='unchanged', colors=colors, dmf=distance_modifiers, nodetypes=nodetypes):
        if nodetype:
            if (self.nodetype == ('start' or 'end')) and (nodetype == ('wall' or 'mud')):
                pass
            else:
                self.nodetype = nodetype        

        if is_visited != 'unchanged':
            self.is_visited = is_visited

        if is_path != 'unchanged':
            self.is_path = is_path

        self.rcolor = colors['regular'][self.nodetype]
        self.vcolor = colors['visited'][self.nodetype]
        self.pcolor = colors['path'][self.nodetype]
        self.distance_modifier = dmf[self.nodetype]
        self.color = self.pcolor if self.is_path else self.vcolor if self.is_visited else self.rcolor


WIDTH = 7
HEIGHT = WIDTH
BUTTON_HEIGHT = 50

MARGIN = 0

# Create a 2 dimensional array (a list of lists)
grid = []
ROWS = 100

for row in range(ROWS):
    grid.append([])
    for column in range(ROWS):
        grid[row].append(Node('blank')) 


START_POINT = (random.randrange(2,ROWS-1,2)-1,random.randrange(2,ROWS-1,2)-1)
END_POINT = (random.randrange(2,ROWS-1,2),random.randrange(2,ROWS-1,2))

grid[START_POINT[0]][START_POINT[1]].update(nodetype='start')
grid[END_POINT[0]][END_POINT[1]].update(nodetype='end')


mouse_drag = False
drag_start_point = False
drag_end_point = False

# Used for deciding what to do in different situations
path_found = False
algorithm_run = False

pygame.init()

# Set default font for nodes
FONT = pygame.font.SysFont('arial', 6)

# Set the width and height of the screen [width, height]
SCREEN_WIDTH = ROWS * (WIDTH + MARGIN) + MARGIN * 2
SCREEN_HEIGHT = SCREEN_WIDTH + BUTTON_HEIGHT * 3
WINDOW_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
screen = pygame.display.set_mode(WINDOW_SIZE)

# Make some Buttons
bfsButton = Button(GREY, 0, SCREEN_WIDTH, SCREEN_WIDTH/4, BUTTON_HEIGHT*2, "BFS")
astarButton = Button(GREY, SCREEN_WIDTH/4, SCREEN_WIDTH, SCREEN_WIDTH/4, BUTTON_HEIGHT*2, "A*")
resetButton = Button(GREY, SCREEN_WIDTH/2, SCREEN_WIDTH, SCREEN_WIDTH/4, BUTTON_HEIGHT*2, "Reset")
mazeButton = Button(GREY, SCREEN_WIDTH * 3/4, SCREEN_WIDTH, SCREEN_WIDTH/4, BUTTON_HEIGHT*2, "Maze (Prim)")

pygame.display.set_caption("A-Mazing")
 
# Loop until the user clicks the close Button.
done = False
 
while not done:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            
            # Find out which keys have been pressed
            pressed = pygame.key.get_pressed()

            # If click is inside grid
            if pos[1] <= SCREEN_WIDTH-1:

                # Change the x/y screen coordinates to grid coordinates
                column = pos[0] // (WIDTH + MARGIN)
                row = pos[1] // (HEIGHT + MARGIN)

                if (row,column) == START_POINT:
                    drag_start_point = True
                elif (row,column) == END_POINT:
                    drag_end_point = True

            # # When the DFS Button is clicked
            elif bfsButton.isOver(pos):
                clear_visited()
                update_gui(draw_background=False, draw_buttons=False)
                pygame.display.flip()
                path_found = BFS(grid, START_POINT, END_POINT)
                grid[START_POINT[0]][START_POINT[1]].update(nodetype='start')
                algorithm_run = 'bfs'

            # When the A* Button is clicked
            elif astarButton.isOver(pos):
                clear_visited()
                update_gui(draw_background=False, draw_buttons=False)
                pygame.display.flip()
                path_found = a_star(grid, START_POINT, END_POINT)
                grid[START_POINT[0]][START_POINT[1]].update(nodetype='start')
                algorithm_run = 'astar'

            # When the Reset Button is clicked
            elif resetButton.isOver(pos):
                path_found = False
                algorithm_run = False
                for row in range(ROWS):
                    for column in range(ROWS):
                        if (row,column) != START_POINT and (row,column) != END_POINT:
                            grid[row][column].update(nodetype='blank', is_visited=False, is_path=False)

            # When the Prim Button is clicked
            elif mazeButton.isOver(pos):
                path_found = False
                algorithm_run = False
                for row in range(ROWS):
                    for column in range(ROWS):
                        if (row,column) != START_POINT and (row,column) != END_POINT:
                            grid[row][column].update(nodetype='blank', is_visited=False, is_path=False)
                grid = better_prim()

        elif event.type == pygame.MOUSEBUTTONUP:
            mouse_drag = drag_end_point = drag_start_point = False
        
        elif event.type == pygame.MOUSEMOTION:

            left, middle, right = pygame.mouse.get_pressed()
            
            if not left:
                mouse_drag = drag_end_point = drag_start_point = False
                continue

            pos = pygame.mouse.get_pos()
            
            column = pos[0] // (WIDTH + MARGIN)
            row = pos[1] // (HEIGHT + MARGIN)
            
            if pos[1] >= SCREEN_WIDTH-2 or pos[1] <= 2 or pos[0] >= SCREEN_WIDTH-2 or pos[0] <= 2:
                mouse_drag = False
                continue
                        
            cell_updated = grid[row][column]

            # Move the start point
            if drag_start_point == True:
                if grid[row][column].nodetype == "blank":
                    grid[START_POINT[0]][START_POINT[1]].update(nodetype='blank', is_path=False, is_visited=False)
                    START_POINT = (row,column)
                    grid[START_POINT[0]][START_POINT[1]].update(nodetype='start')
                    # If we have already run the algorithm, update it as the point is moved
                    if algorithm_run:
                        path_found = update_path()
                        grid[START_POINT[0]][START_POINT[1]].update(nodetype='start') 
            
            # Move the end point
            elif drag_end_point == True:
                if grid[row][column].nodetype == "blank":
                    grid[END_POINT[0]][END_POINT[1]].update(nodetype='blank', is_path=False, is_visited=False)
                    END_POINT = (row,column)
                    grid[END_POINT[0]][END_POINT[1]].update(nodetype='end')
                    # If we have already run the algorithm, update it as the point is moved
                    if algorithm_run:
                        path_found = update_path()
                        grid[START_POINT[0]][START_POINT[1]].update(nodetype='start')

            pygame.display.flip()

    def clear_visited():
        excluded_nodetypes = ['start', 'end', 'wall', 'mud']
        for row in range(ROWS):
            for column in range(ROWS):
                if grid[row][column].nodetype not in excluded_nodetypes:
                    grid[row][column].update(nodetype="blank", is_visited=False, is_path=False)
                else:
                     grid[row][column].update(is_visited=False, is_path=False)
        update_gui(draw_background=False, draw_buttons=False)

    def update_path(algorithm_run=algorithm_run):
        
        clear_visited()
        
        valid_algorithms = ['dijkstra', 'astar', 'dfs', 'bfs']

        assert algorithm_run in valid_algorithms, f"last algorithm used ({algorithm_run}) is not in valid algorithms: {valid_algorithms}"

        if algorithm_run == 'dijkstra':
            path_found = a_star(grid, START_POINT, END_POINT, visualise=False)
        elif algorithm_run == 'astar':
            path_found = a_star(grid, START_POINT, END_POINT, visualise=False)
        elif algorithm_run == 'dfs':
            path_found = BFS(grid, START_POINT, END_POINT, x='d', visualise=False)
        elif algorithm_run == 'bfs':
            path_found = BFS(grid, START_POINT, END_POINT, x='b', visualise=False)
        else:
            path_found = False
        return path_found
    
    def draw_square(row,column,grid=grid):
        pygame.draw.rect(
            screen,
            grid[row][column].color,
            [
                (MARGIN + HEIGHT) * column + MARGIN,
                (MARGIN + HEIGHT) * row + MARGIN,
                WIDTH,
                HEIGHT
            ]
        )
        pygame.event.pump()

    def update_square(row,column):
        pygame.display.update(
            (MARGIN + WIDTH) * column + MARGIN,
            (MARGIN + HEIGHT) * row + MARGIN,
            WIDTH,
            HEIGHT
        )
        pygame.event.pump()

    def prim(mazearray=False, start_point=False):

        # If a maze isn't input, we just create a grid full of walls
        if not mazearray:
            mazearray = []
            for row in range(ROWS):
                mazearray.append([])
                for column in range(ROWS):
                    mazearray[row].append(Node('wall'))
                    draw_square(row,column,grid=mazearray)

        n = len(mazearray) - 1

        if not start_point:
            start_point = (random.randrange(0,n,2),random.randrange(0,n,2))        

        draw_square(start_point[0], start_point[1], grid=mazearray)
        pygame.display.flip()

        walls = set([])

        neighbours = get_neighbours(start_point, n)

        for neighbour, ntype in neighbours:
            if mazearray[neighbour[0]][neighbour[1]].nodetype == 'wall':
                walls.add(neighbour)
                # walls.append(neighbour)

        # While there are walls in the list:
        # Pick a random wall from the list. If only one of the cells that the wall divides is visited, then:
        # # Make the wall a passage and mark the unvisited cell as part of the maze.
        # # Add the neighboring walls of the cell to the wall list.
        # Remove the wall from the list.
        while len(walls) > 0:                
            wall = random.choice(tuple(walls))
            wall_neighbours = get_neighbours(wall, n)
            neighbouring_walls = set()
            pcount = 0
            for wall_neighbour, ntype in wall_neighbours:
                if wall_neighbour == (start_point or END_POINT):
                    continue
                if mazearray[wall_neighbour[0]][wall_neighbour[1]].nodetype != 'wall':
                    pcount += 1
                else:
                    neighbouring_walls.add(wall_neighbour)
                    
            if pcount <= 1:
                mazearray[wall[0]][wall[1]].update(nodetype='blank')
                draw_square(wall[0],wall[1],mazearray)
                update_square(wall[0],wall[1])
                time.sleep(0.0001)

                walls.update(neighbouring_walls)

            
            walls.remove(wall)            

        mazearray[END_POINT[0]][END_POINT[1]].update(nodetype='end')
        mazearray[START_POINT[0]][START_POINT[1]].update(nodetype='start')

        return mazearray

    def better_prim(mazearray=False, start_point=False):

        # If a maze isn't input, we just create a grid full of walls
        if not mazearray:
            mazearray = []
            for row in range(ROWS):
                mazearray.append([])
                for column in range(ROWS):
                    if row % 2 != 0 and column % 2 != 0:
                        mazearray[row].append(Node('dormant'))
                    else:
                        mazearray[row].append(Node('wall'))

                    draw_square(row,column,grid=mazearray)

        n = len(mazearray) - 1

        if not start_point:
            start_point = (random.randrange(1,n,2),random.randrange(1,n,2))
            mazearray[start_point[0]][start_point[1]].update(nodetype='blank')
    
        draw_square(start_point[0], start_point[1], grid=mazearray)
        pygame.display.flip()

        walls = set()

        starting_walls = get_neighbours(start_point, n)

        for wall, ntype in starting_walls:
            if mazearray[wall[0]][wall[1]].nodetype == 'wall':
                walls.add(wall)

        # While there are walls in the list (set):
        # Pick a random wall from the list. If only one of the cells that the wall divides is visited, then:
        # # Make the wall a passage and mark the unvisited cell as part of the maze.
        # # Add the neighboring walls of the cell to the wall list.
        # Remove the wall from the list.
        while len(walls) > 0:
            wall = random.choice(tuple(walls))
            visited = 0
            add_to_maze = []

            for wall_neighbour, ntype in get_neighbours(wall,n):
                if mazearray[wall_neighbour[0]][wall_neighbour[1]].nodetype == 'blank':
                    visited += 1

            if visited <= 1:
                mazearray[wall[0]][wall[1]].update(nodetype='blank')
                
                draw_square(wall[0],wall[1],mazearray)
                update_square(wall[0],wall[1])
                time.sleep(0.0001)
                
                # A 'dormant' node (below) is a different type of node I had to create for this algo
                # otherwise the maze generated doesn't look like a traditional maze.
                # Every dormant eventually becomes a blank node, while the regular walls
                # sometimes become a passage between blanks and are sometimes left as walls
                for neighbour, ntype in get_neighbours(wall,n):
                    if mazearray[neighbour[0]][neighbour[1]].nodetype == 'dormant':
                        add_to_maze.append((neighbour[0],neighbour[1]))
                
                if len(add_to_maze) > 0:
                    cell = add_to_maze.pop()
                    mazearray[cell[0]][cell[1]].update(nodetype='blank')
                    
                    draw_square(cell[0],cell[1],mazearray)
                    update_square(cell[0],cell[1])
                    time.sleep(0.000001)
                    
                    for cell_neighbour, ntype in get_neighbours(cell,n):
                        if mazearray[cell_neighbour[0]][cell_neighbour[1]].nodetype == 'wall':
                            walls.add(cell_neighbour)

            walls.remove(wall)

        mazearray[END_POINT[0]][END_POINT[1]].update(nodetype='end')
        mazearray[START_POINT[0]][START_POINT[1]].update(nodetype='start')

        return mazearray

    def gaps_to_offset():
        return [x for x in range(2, ROWS, 3)]
    
    def get_neighbours(node, max_width=ROWS-1):
        neighbours = (
            ((min(max_width,node[0]+1),node[1]),"+"),
            ((max(0,node[0]-1),node[1]),"+"),
            ((node[0],min(max_width,node[1]+1)),"+"),
            ((node[0],max(0,node[1]-1)),"+")
        )
        return (neighbour for neighbour in neighbours if neighbour[0] != node)

    def a_star(mazearray, start_point=(0,0), goal_node=False, display=pygame.display):
        heuristic = 0
        distance = 0

        n = len(mazearray) - 1
        
        visited_nodes = set()
        unvisited_nodes = set([(x,y) for x in range(n+1) for y in range(n+1)])
        queue = AStarQueue()

        queue.push(distance+heuristic, distance, start_point)
        v_distances = {}

        if not goal_node:
            goal_node = (n,n)
        priority, current_distance, current_node = queue.pop()
        
        while current_node != goal_node and len(unvisited_nodes) > 0:
            if current_node in visited_nodes:
                if len(queue.show()) == 0:
                    return False
                else:
                    priority, current_distance, current_node = queue.pop()
                    continue
            
            for neighbour in get_neighbours(current_node, n):
                neighbours_loop(
                    neighbour, 
                    mazearr=mazearray, 
                    visited_nodes=visited_nodes, 
                    unvisited_nodes=unvisited_nodes, 
                    queue=queue, 
                    v_distances=v_distances, 
                    current_node=current_node,
                    current_distance=current_distance,
                )

            visited_nodes.add(current_node)
            unvisited_nodes.discard(current_node)
            
            v_distances[current_node] = current_distance
            
            if (current_node[0],current_node[1]) != start_point:
                mazearray[current_node[0]][current_node[1]].update(is_visited = True)
                draw_square(current_node[0],current_node[1],grid=mazearray)

                
                update_square(current_node[0],current_node[1])
                time.sleep(0.00001)
            
            if len(queue.show()) == 0:
                return False
            # Otherwise we take the minimum distance as the new current node
            else:
                priority, current_distance, current_node = queue.pop()
        

        v_distances[goal_node] = current_distance + (1)
        visited_nodes.add(goal_node)

        # Draw the path back from goal node to start node
        trace_back(goal_node, start_point, v_distances, visited_nodes, n, mazearray)
        print("Total nodes visited by A*:",len(visited_nodes))
        return False if v_distances[goal_node] == float('inf') else True

    def neighbours_loop(neighbour, mazearr, visited_nodes, unvisited_nodes, queue, v_distances, current_node, current_distance):
        
        neighbour, ntype = neighbour

        heuristic = 0
        heuristic += abs(END_POINT[0] - neighbour[0]) + abs(END_POINT[1] - neighbour[1])

        if neighbour in visited_nodes:
            pass
        elif mazearr[neighbour[0]][neighbour[1]].nodetype == 'wall':
            visited_nodes.add(neighbour)
            unvisited_nodes.discard(neighbour)
        else:
            modifier = mazearr[neighbour[0]][neighbour[1]].distance_modifier
            if ntype == "+":
                queue.push(current_distance+(1*modifier)+heuristic, current_distance+(1*modifier), neighbour)
            elif ntype == "x": 
                queue.push(current_distance+((2**0.5)*modifier)+heuristic, current_distance+((2**0.5)*modifier), neighbour)

    def trace_back(goal_node, start_node, v_distances, visited_nodes, n, mazearray, diags=False):
        
        path = [goal_node]
        
        current_node = goal_node
        
        while current_node != start_node:
            # Start an empty priority queue for the current node to check all neighbours
            neighbour_distances = PriorityQueue()
            
            neighbours = get_neighbours(current_node, n)

            distance = v_distances[current_node]
            
            # For each neighbour of the current node, add its location and distance
            # to a priority queue
            for neighbour, ntype in neighbours:
                if neighbour in v_distances:
                    distance = v_distances[neighbour]
                    neighbour_distances.push(distance, neighbour)
            
            # Pop the lowest value off; that is the next node in our path
            distance, smallest_neighbour = neighbour_distances.pop()
            mazearray[smallest_neighbour[0]][smallest_neighbour[1]].update(is_path=True)
            
            # Update pygame display
            draw_square(smallest_neighbour[0],smallest_neighbour[1],grid=mazearray)
            # update_square(smallest_neighbour[0],smallest_neighbour[1])            
            
            path.append(smallest_neighbour)
            current_node = smallest_neighbour

        pygame.display.flip()

        mazearray[start_node[0]][start_node[1]].update(is_path=True)

    def BFS(mazearray, start_point, goal_node, display=pygame.display):

        n = len(mazearray) - 1
        
        mydeque = deque()
        mydeque.append(start_point)
        visited_nodes = set([])
        path_dict = {start_point: None}

        # Main algorithm loop
        while len(mydeque) > 0:
            
            current_node = mydeque.popleft()
          
            if current_node == goal_node:
                path_node = goal_node
                while True:
                    path_node = path_dict[path_node]
                    mazearray[path_node[0]][path_node[1]].update(is_path = True)
                    draw_square(path_node[0],path_node[1],grid=mazearray)
                    update_square(path_node[0],path_node[1])
                    if path_node == start_point:
                        print("Total nodes visited by BFS:",len(visited_nodes))
                        return True
            
            if mazearray[current_node[0]][current_node[1]].nodetype == 'wall':
                continue
            
            if current_node not in visited_nodes:
                visited_nodes.add(current_node)
                mazearray[current_node[0]][current_node[1]].update(is_visited = True)
                draw_square(current_node[0],current_node[1],grid=mazearray)                
                update_square(current_node[0],current_node[1])
                time.sleep(0.001)
                
                for neighbour, ntype in get_neighbours(current_node, n):
                    mydeque.append(neighbour)
                    # Used for tracing back
                    if neighbour not in visited_nodes:
                        path_dict[neighbour] = current_node
        
        pygame.display.flip()
        
        return False
    
    grid[START_POINT[0]][START_POINT[1]].update(nodetype='start')
    grid[END_POINT[0]][END_POINT[1]].update(nodetype='end')

    # Update the GUI 
    def update_gui(draw_background=True, draw_buttons=True, draw_grid=True):
        
        if draw_background:
            # Draw a black background to set everything on
            screen.fill(BLACK)
            pass

        if draw_buttons:
            bfsButton.draw(screen, (0,0,0))
            astarButton.draw(screen, (0,0,0))
            resetButton.draw(screen, (0,0,0))
            mazeButton.draw(screen, (0,0,0))
        
        if draw_grid:
            # Draw the grid
            for row in range(ROWS):
                for column in range(ROWS):
                    color = grid[row][column].color
                    draw_square(row,column)

    update_gui()

    pygame.display.flip()
 
pygame.quit()
