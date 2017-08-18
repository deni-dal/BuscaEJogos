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
    
def recursive_LDS(node, problem, limit, solution, visited, border):
    visited.push(node)          # comeca adicionando o no na lista de visitados
    if problem.goalTest(node):  # verifica se o no e o objetivo
        return True             # se sim retorna para adicionar na lista de solucoes
    elif limit == 0:            # se a profundidade for zero, retorna falso
        return False
    else:   
        actions = util.Queue()      # cria uma lista de acoes
        for action in problem.getActions(node):              
            new_node = problem.getResult(node, action)  #expande o no 
            actions.push(action)    # adiciona as acoes validas na lista de acoes
            border.push(new_node)   # adiciona o novo no na lista de bordas

        for action in actions.list:
            new_node = border.pop()     # retira o ultimo no
            if new_node not in visited.list and new_node not in border.list:    # verifica se o no esta em alguma das listas
                result = recursive_LDS(new_node, problem, (limit-1), solution, visited, border) # se nao esta, faz a busca novamente
                if result:
                    solution.push(action)   # se encontrar o no, adiciona na lista de solucoes
                    return True
    return False
        

def iterativeDeepeningSearch(problem):
    """
    Perform DFS with increasingly larger depth.

    Begin with a depth of 1 and increment depth by 1 at every step.
    """
    depth = 1   
    while True:
        visited = util.Queue()
        solution = util.Queue()
        border = util.Stack()
        
        result = recursive_LDS(problem.getStartState(), problem, depth, solution, visited, border)
        
        if result:    
            return solution.list
        depth += 1

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    solution = [] # lista nos para solucao
    node = problem.getStartState()     # estado inicial
    possible_solution = util.PriorityQueue()   # Fila onde cada item possui uma prioridade determinada 
    
    node_cost = heuristic(node, problem) # custo inicial 

    visited = util.Queue()  # Lista de nos ja visitados - FIFO
    visited.push(node)

    solution = recursive_AStar(node, problem, heuristic, possible_solution, node_cost, solution, visited) 

    return solution
         
def recursive_AStar(node, problem, heuristic, possible_solution, node_cost, solution, visited):
    while True:
        if problem.goalTest(node): # Verifica se o no ja e o objetivo
            return solution
    
        for action in problem.getActions(node):
            new_solution = copy.copy(solution)
            new_solution.append(action)
            result_node = problem.getResult(node, action)   # expande o no  
            
                            #custo entre o no expandido    + custo entre o no atual e o proximo  + (custo inicial - custo atual)
            action_cost = (heuristic(result_node, problem) + problem.getCost(node, action)) + (node_cost - heuristic(node, problem))
            possible_solution.push((result_node, action_cost, new_solution), action_cost)   # adiciona o no a lista de possiveis solucoes, o custo equivale a prioridade do item

        new_solution_found = False
        while not new_solution_found:
            if possible_solution.isEmpty():
                return False

            (node, node_cost, solution) = possible_solution.pop() # verificar o que essa lista significa para simplificar

            if node not in visited.list:
                visited.push(node)      # se o no ainda nao tiver sido visitado, adiciona na lista
                new_solution_found = True   

# Abbreviations
bfs = breadthFirstSearch
astar = aStarSearch
ids = iterativeDeepeningSearch
tms = tinyMazeSearch

# Comando Busca A* 
#python pacman.py -l bigMaze -z .5 -p SearchAgent -a fn=astar,heuristic=euclideanHeuristic

# Comando Busca Iterative Deep Search
#python pacman.py -l tinyMaze -p SearchAgent -a fn=ids