from state import *
from collections import deque

def update_max_fringe(frontier, max_fringe_size):
    if(len(frontier) > max_fringe_size):
        max_fringe_size = len(frontier)

    return max_fringe_size

def update_max_depth(node, max_search_depth):
    if(node.depth > max_search_depth):
        max_search_depth = node.depth

    return max_search_depth

def breadth_first_search(input):
    input_list = input.split(',')
    input_list = list(map(int, input_list))

    puzzle_instance = tuple(input_list)
    initialize(input_list)

    children = []
    frontier = deque()
    frontier.append(create_node(puzzle_instance, None, None, 0, 0 ))
    max_fringe_size = 1
    max_search_depth = 0
    nodes_expanded = 0
    explored = set()

    while frontier:
        node = frontier.popleft()

        if(node.state in explored):
            continue
        
        explored.add(node.state)

        if(goalTest(node)):
            input_list = []
            input_list.append(node)
            input_list.append(max_fringe_size)
            input_list.append(len(frontier))
            input_list.append(max_search_depth)
            input_list.append(nodes_expanded)
            return input_list  

        nodes_expanded = nodes_expanded+1

        children = expand_nodes(node)
        for child in children:
            if(child.state in explored):
                continue
            elif(child not in frontier):
                frontier.append(child)
                max_fringe_size = update_max_fringe(frontier, max_fringe_size)
                max_search_depth = update_max_depth(child, max_search_depth)
    return False


            
def depth_first_search(input):
    input_list = input.split(',')
    input_list = list(map(int, input_list))

    puzzle_instance = tuple(input_list)
    
    initialize(input_list)
     
    firstNode = create_node(puzzle_instance,None,None,0,0)
    frontier = deque()
    frontier.append(firstNode)
    explored = set()

    nodes_expanded = 0
    fringe_size = len(frontier)
    max_fringe_size = fringe_size
    max_search_depth = 0
    running_time = 0

    while frontier:
        node = frontier.pop()   
        explored.add(node.state) 

  
        if(goalTest(node)):
            input_list = []
            input_list.append(node)
            input_list.append(max_fringe_size)
            input_list.append(len(frontier))
            input_list.append(max_search_depth)
            input_list.append(nodes_expanded)
            return input_list   

        nodes_expanded = nodes_expanded+1

        children = expand_nodes_reverse(node)
        for child in children:
            if child.state not in explored:
                frontier.append(child)
                explored.add(child.state)
                max_fringe_size = update_max_fringe(frontier, max_fringe_size)
                max_search_depth = update_max_depth(child, max_search_depth)

    return False        
 


def a_star(input):
    input_list = input.split(',')
    input_list = list(map(int, input_list))

    puzzle_instance = tuple(input_list)
    initialize(input_list)

    children = []
    frontier = []
    cost = costFunction(puzzle_instance)
    heappush(frontier, create_node(puzzle_instance, None, None, 0, cost ))
    
    max_fringe_size = 1
    max_search_depth = 0
    nodes_expanded = 0
    explored = set()

    while frontier:
        node = heappop(frontier)
        
        if(node.state in explored):
            continue
        
        explored.add(node.state)

        if(goalTest(node)):
            input_list = []
            input_list.append(node)
            input_list.append(max_fringe_size)
            input_list.append(len(frontier))
            input_list.append(max_search_depth)
            input_list.append(nodes_expanded)
            return input_list  
        
        nodes_expanded = nodes_expanded+1

        children = expand_nodes_ast(node)
        for child in children:
            if(child.state in explored):
                continue
            elif(child not in frontier):
                heappush(frontier, child)
                max_fringe_size = update_max_fringe(frontier, max_fringe_size)
                max_search_depth = update_max_depth(child, max_search_depth)
            
    return False


def a_star_limit(puzzle_instance, cost_limit, nodes_expanded, max_fringe_size, max_search_depth):

    children = []
    frontier = []
    cost = costFunction(puzzle_instance)
    heappush(frontier, create_node(puzzle_instance, None, None, 0, cost ))
    explored = set()

    while frontier:
        node = heappop(frontier)
        
        if(node.state in explored):
            continue
        
        explored.add(node.state)

        if(goalTest(node)):
            input_list = []
            input_list.append(node)
            input_list.append(max_fringe_size)
            input_list.append(len(frontier))
            input_list.append(max_search_depth)
            input_list.append(nodes_expanded)
            return input_list  
        
        nodes_expanded = nodes_expanded+1

        children = expand_nodes_ast(node)
        for child in children:
            if(child.cost > cost_limit):
                continue
            elif(child.state in explored):
                continue
            elif(child not in frontier):
                heappush(frontier, child)
                max_fringe_size = update_max_fringe(frontier, max_fringe_size)
                max_search_depth = update_max_depth(child, max_search_depth)
            
    return None

def ida_star(input):
    input_list = input.split(',')
    input_list = list(map(int, input_list))

    puzzle_instance = tuple(input_list)
    initialize(input_list)

    cost_limit =1 
    nodes_expanded = 0 
    max_fringe_size = 1
    max_search_depth = 0
    running_time = 0

    while(1):

        if(a_star_limit(puzzle_instance, cost_limit, nodes_expanded, max_fringe_size, max_search_depth)==None):
            cost_limit += 1
            a_star_limit(puzzle_instance, cost_limit, nodes_expanded, max_fringe_size, max_search_depth)
        else:
            input_list = []
            input_list =  a_star_limit(puzzle_instance, cost_limit, nodes_expanded, max_fringe_size, max_search_depth)
            return input_list
           
    return False        
