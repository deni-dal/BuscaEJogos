# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util
import sys
import copy

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def goalTest(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getActions(self, state):
        """
        Given a state, returns available actions.
        Returns a list of actions
        """        
        util.raiseNotDefined()

    def getResult(self, state, action):
        """
        Given a state and an action, returns resulting state.
        """
        util.raiseNotDefined()

    def getCost(self, state, action):
        """
        Given a state and an action, returns step cost, which is the incremental cost 
        of moving to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first.

    You are not required to implement this, but you may find it useful for Q5.
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0
###################################################################################
def iterativeDeepeningSearch(problem):
    """
    Perform DFS with increasingly larger depth.

    Begin with a depth of 1 and increment depth by 1 at every step.
    """
    "*** YOUR CODE HERE ***"
    x = 1;
    while True:
        visited = util.Queue() #hummmmmmm
        solution = util.Queue() #hummmmm
        border = util.Stack() #border??? frontierrr????
        result = BPLRecursive(problem.getStartState(), problem, x, solution, visited, border)
        x += 1
        if result != 0:            
            return solution.list
    
    

def BPLRecursive(node, problem, limit, solution, visited, border):
    # marcar o no visitado???
    # testar se e objetivo
    # se o limite for 0 retorna oque?
    # senaooooooo
    cut = False
    visited.push(node)
    if problem.goalTest(node):
        return True
    elif limit > 0:
        actions = util.Queue()
        for action in problem.getActions(node):
            node_child = problem.getResult(node, action)
            actions.push(action)
            border.push(node_child)
        for action in actions.list:
            node_child = border.pop()
            if node_child not in visited.list and node_child not in border.list:
                result = BPLRecursive(node_child, problem, limit - 1, solution, visited, border)
                if result:
                    solution.push(action)
                    return True
        return False

#####################################################################################
def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    soluction = []                     #caminho de retorno -> solucao
    startState = problem.getStartState()
    listaaberta = util.PriorityQueue() #Fila preferencial
    listafechada = util.Queue()        #Fila comum
    node = problem.getStartState()     #node atual e o inicio
    listaaberta.push(startState,0)     #aqui nao precisa calcular o custo do inicial que e 0
    while len(listaaberta) is not 0
        node = listaaberta.pop()       #retira o no atual da lista aberta
        listafechada.push(node)        #insere o no atual na lista fechada
        if problem.goalTest(node)      #caminho encontrado
            return soluction     
        if len(listaaberta) is 0       #caminho nao encontrado
            return soluction
        
	
def recursiveastar(node, problem, heuristic, possible_solution, node_cost, solution, visited): 

def convertOriginMapToActionList(node, originMap):
	actionsList = []
	while node in originMap:
		node, action = originMap[node]
		actionsList.insert(0, action)	
	return actionsList    

# Abbreviations
bfs = breadthFirstSearch
astar = aStarSearch
ids = iterativeDeepeningSearch
