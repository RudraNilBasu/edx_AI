from node import *
from Queue import *
from heapq import *
from copy import deepcopy
import math

def goalTest(node):
	if(node.state == initGoalTest):
		return True
	return False

def initialize(input_list):

	global initGoalTest
	global BOUNDARY
	
	BOUNDARY = int(math.sqrt(len(input_list)))
	initGoalTest = tuple(range(BOUNDARY*BOUNDARY))
	
	return initGoalTest

def costFunction(state):
	cost = 0
	distanceSum = 0
	row = 0
	column = 0


	while row<BOUNDARY:
		column = 0
		while column < BOUNDARY:
			position = row*BOUNDARY
			position += column
			value = state.index(position);
			if (value != 0):
				targetRow = (value ) / BOUNDARY; 
				targetColumn = (value ) % BOUNDARY; 
				dx = row - targetRow; 
				dy = column - targetColumn;
				distanceSum += math.fabs(dx) + math.fabs(dy); 
			column+=1
		row+=1
	cost = distanceSum
	return cost


def expand_nodes(node):

	children = []
	state = node.state
	depth = node.depth
	i = int(state.index(0))

	newState = move_up(i, state)
	newNodeUp = create_node(newState, node, "Up", depth+1, 0)
	children.append(newNodeUp)

	newState = move_down(i, state)
	newNodeDown = create_node(newState, node, "Down", depth+1, 0)
	children.append(newNodeDown)

	newState = move_left(i, state)
	newNodeLeft = create_node(newState, node, "Left", depth+1, 0)
	children.append(newNodeLeft)

	newState = move_right(i, state)
	newNodeRight = create_node(newState, node, "Right", depth+1, 0)
	children.append(newNodeRight)

	children = [node for node in children if node.state != None] 
	return children

def expand_nodes_reverse_ida(node):

	children = []
	state = node.state
	depth = node.depth
	i = int(state.index(0))

	newStateRight = move_right(i, state)
	if(newStateRight != None):
		newCostRight = costFunction(newStateRight)
		newNodeRight = create_node(newStateRight, node, "Right", depth+1, newCostRight)
		children.append(newNodeRight)

	newStateLeft = move_left(i, state)
	if(newStateLeft != None):
		newCostLeft = costFunction(newStateLeft)
		newNodeLeft = create_node(newStateLeft, node, "Left", depth+1, newCostLeft)
		children.append(newNodeLeft)

	newStateDown = move_down(i, state)
	if(newStateDown != None):
		newCostDown = costFunction(newStateDown)
		newNodeDown = create_node(newStateDown, node, "Down", depth+1, newCostDown)
		children.append(newNodeDown)

	newStateUp = move_up(i, state)
	if(newStateUp != None):
		newCostUp = costFunction(newStateUp)
		newNodeUp = create_node(newStateUp, node, "Up", depth+1, newCostUp)
		children.append(newNodeUp)

	children = [node for node in children if node.state != None] 
	return children



def expand_nodes_ast(node):

	children = []
	state = node.state
	depth = node.depth
	i = int(state.index(0))

	newStateUp = move_up(i, state)
	if(newStateUp != None):
		newCostUp = costFunction(newStateUp)
		newNodeUp = create_node(newStateUp, node, "Up", depth+1, newCostUp)
		children.append(newNodeUp)

	newStateDown = move_down(i, state)
	if(newStateDown != None):
		newCostDown = costFunction(newStateDown)
		newNodeDown = create_node(newStateDown, node, "Down", depth+1, newCostDown)
		children.append(newNodeDown)

	newStateLeft = move_left(i, state)
	if(newStateLeft != None):
		newCostLeft = costFunction(newStateLeft)
		newNodeLeft = create_node(newStateLeft, node, "Left", depth+1, newCostLeft)
		children.append(newNodeLeft)

	newStateRight = move_right(i, state)
	if(newStateRight != None):
		newCostRight = costFunction(newStateRight)
		newNodeRight = create_node(newStateRight, node, "Right", depth+1, newCostRight)
		children.append(newNodeRight)

	children = [node for node in children if node.state != None] 
	return children


def expand_nodes_reverse(node):

	children = []
	state = node.state
	depth = node.depth

	i = state.index(0)

	newStateRight = move_right(i, state)
	newNodeRight = create_node(newStateRight, node, "Right", depth+1, 0)
	children.append(newNodeRight)

	newStateLeft = move_left(i, state)
	newNodeLeft = create_node(newStateLeft, node, "Left", depth+1, 0)
	children.append(newNodeLeft)

	newStateDown = move_down(i, state)
	newNodeDown = create_node(newStateDown, node, "Down", depth+1, 0)
	children.append(newNodeDown)

	newStateUp = move_up(i, state)
	newNodeUp = create_node(newStateUp, node, "Up", depth+1, 0)
	children.append(newNodeUp)

	children = [node for node in children if node.state != None] 

	return children


def create_node( state, parent, direction, depth, cost ):
	return Node( state, parent, direction, depth, cost )


def move_up(i, state):  
	if i-BOUNDARY>=0:
		changed_state = list(deepcopy(state))

		changed_state[i]= state[i-BOUNDARY]
		changed_state[i-BOUNDARY]=state[i]
		
		return tuple(changed_state)

	return None

def move_down(i, state):  

	if i+BOUNDARY<BOUNDARY*BOUNDARY:
		changed_state = list(deepcopy(state))

		changed_state[i]= state[i+BOUNDARY]
		changed_state[i+BOUNDARY]=state[i]
		
		return tuple(changed_state)

	return None 

def move_left(i, state):
	
	if i%BOUNDARY != 0:
		changed_state = list(deepcopy(state))

		changed_state[i]= state[i-1]
		changed_state[i-1]=state[i]
		
		return tuple(changed_state)

	return None 

def move_right(i, state):

	if (i+1)%BOUNDARY != 0:
		changed_state = list(deepcopy(state))

		changed_state[i]= state[i+1]
		changed_state[i+1]=state[i]
		
		return tuple(changed_state)

	return None 
