# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        return successorGameState.getScore()

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent & AlphaBetaPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 7)

      Algoritmo minimax, eh um algoritmo que determina a acao dos agentes adversarios,
      O jogador Max sempre considera que o jogador Min vai escolher a jogada que o deixa na pior situacao.
      A cada jogada o jogador Max procura maximizar suas chances de ganhar enquanto o jogador Min procura 
      minimizar as chances de isso acontecer. 
    """

    def min_max(self, gameState, depth): # o metodo minmax faz a verificacao do agente e a chamada da funcao referente a ele
        if gameState.isWin() or gameState.isLose() or depth == self.depth * gameState.getNumAgents():  # verifica se eh o fim do jogo ou profundidade = 0
            return self.evaluationFunction(gameState)    # retorna

        if depth % gameState.getNumAgents() == 0: # pacman / se for o pacman faz acoes max, senao faz acoes min
            return self.maxValue(gameState, depth, depth % gameState.getNumAgents())
        else : #fantasmas
            return self.minValue(gameState, depth, depth % gameState.getNumAgents())

    def maxValue(self, gameState, depth, index): # o metodo maxValue verifica o valor maximo entre o valor maximo conhecido e o da proxima acao       
        actions = gameState.getLegalActions(index)
        max_value = -float("inf")

        for action in actions:
            max_value = max(max_value, self.min_max(gameState.generateSuccessor(index, action), depth+1)) # calcula qual valor maximo 

        return max_value

    def minValue(self, gameState, depth, index): # o metodo minValue faz o contrario do maxValue
        actions = gameState.getLegalActions(index) 
        min_value = float("inf")
        
        for action in actions:
            min_value = min(min_value, self.min_max(gameState.generateSuccessor(index, action), depth+1)) # calcula qual valor minimo 
            
        return min_value   

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        next_action = None
        actions = gameState.getLegalActions(0) # acoes possiveis para o pacman
        max_value = -float("inf")

        for action in actions:
            value = self.min_max(gameState.generateSuccessor(0, action), 1) # um valor min ou maximo eh dado para acao
            if value > max_value: 
                next_action = action
                max_value = value
        
        return next_action         
        

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 8)

      Diferente do minimax, o expectimax procura otimizar a escolha de acao, realizando um 
      o calculo de probabilidade para escolher a acao que sera realizada.
      A melhor acao e calculada pela media das melhores pontuacoes das acoes

    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        return self.expectimax(gameState, self.depth, 0)[1]

    def expectimax(self, gameState, depth, index):
        if depth == 0 or gameState.isWin() or gameState.isLose():  # verifica se eh o fim do jogo ou profundidade = 0
            return (self.evaluationFunction(gameState), None)      # retorna
        
        actions     = gameState.getLegalActions(index)       # lista de acoes possiveis
        next_index  = (index + 1) % gameState.getNumAgents() # proximo agente
        if index == gameState.getNumAgents() -1:
            depth -= 1
        
        score_list = {} # dicionario
        for action in actions:
            next_action = gameState.generateSuccessor(index, action) # proxima acao 
            score_list[action] = self.expectimax(next_action, depth, next_index)[0] # realiza o calculo de pontuacao para cada acao possivel

        if index == 0:
            best_action = max(score_list, key=score_list.get) # melhor acao no conjunto de pontuacoes
            best_score = score_list[best_action] # melhor pontuacao no conjunto de pontuacoes
        else:
            best_action = None
            best_score = 0.0
            for score in score_list.values():
                best_score += score 
            best_score = best_score / len(score_list) # media das melhores pontuacoes

        return (best_score, best_action)     

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 9).

      DESCRIPTION: 
      calculo de distancia minima entre a posicao do pacman e as comidas. 
      calculo de distancia minima entre a posicao pacman e a posicao dos fantasmas.
      O resultado é soma das distancias

    """
    "*** YOUR CODE HERE ***"
    result              = 0
    min_distance        = 1000
    is_min_distance     = False
    pacman_position     = currentGameState.getPacmanPosition()
    food_position_list  = currentGameState.getFood().asList()  # lista de posicionamento das comidas
    ghost_position_list = currentGameState.getGhostPositions() # lista de posicionamento dos fantasmas    
    
    for food_position in food_position_list: # calcula a distancia entre o pacman e as comidas
        food_distance = util.manhattanDistance(pacman_position, food_position)

        if food_distance < min_distance: # determina a menor distancia
            min_distance = food_distance
            is_min_distance = True
    
    if is_min_distance:
        result += min_distance # soma a menor distancia ao resultado

    result += 1000 * currentGameState.getNumFood()
    result += 10 * len(currentGameState.getCapsules())
    
    
    for ghost_position in ghost_position_list: # calcula a distancia entre o pacman e os fantasmas
        ghost_distance = util.manhattanDistance(pacman_position, ghost_position)

        if ghost_distance < 2:
            result = float("inf") 
            
    result -= 10 * currentGameState.getScore()
    
    return result * (-1)

# Abbreviation
better = betterEvaluationFunction

