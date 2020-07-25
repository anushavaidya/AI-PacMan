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
        remaining food () and Pacman position after moving (newPos).
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

        final_score=0.0
        #for ghosts
        Ghost_dist= []
        for ghost in newGhostStates:
          Ghost_Position = ghost.getPosition() 
          d=manhattanDistance(Ghost_Position, newPos)
          Ghost_dist.append(d)
        
        for i in Ghost_dist:
          factor=1
          if(i<=1):
            if(ghost.scaredTimer==0): 
              final_score=final_score-200
            else:
              final_score=final_score + 1500
              factor=-1

        #for capsule
        capsule_state= currentGameState.getCapsules()
        capsule_dist= []
        for capsule in capsule_state:
          b=manhattanDistance(capsule,newPos)
          capsule_dist.append(b)

        for j in capsule_dist:
          if(b==0):
            final_score=final_score + 100
          else:
            final_score=final_score + (10.0/b)

        #for food
        Food= currentGameState.getFood() 
        food_list = Food.asList()
        food_pos = []
        for k in food_list:
            a=manhattanDistance(k,newPos)
            food_pos.append(a)
        for i in food_pos:
              if(i==0):
                final_score=final_score + 100
              else:
                final_score=final_score + (1.0/(i**2))
        return final_score

        

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
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

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
      Your minimax agent (question 2)
    """

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
        

        def max_value(gameState,depth):
            if depth==0 or gameState.isWin() or gameState.isLose():
                return (self.evaluationFunction(gameState), None)

            moves=gameState.getLegalActions()
            score_list = []
            for i in moves:
                current_state= self.index
                next_state = gameState.generateSuccessor(current_state,i) 
                value, action= min_value(next_state,1, depth) 
                score_list.append(value)

            max_score=max(score_list)
            score_len= len(score_list)
            for i in range(score_len):
                if score_list[i] == max_score:
                    best_state = [i]
                    chosenIndex = random.choice(best_state)
            return max_score,moves[chosenIndex]

        def min_value(gameState,agent, depth):  
            if depth==0 or gameState.isWin() or gameState.isLose():
              return (self.evaluationFunction(gameState), None)
        
            moves=gameState.getLegalActions(agent) 
            score_list=[]
            
            for i in moves:
                next_state = gameState.generateSuccessor(agent,i)
                ghost_no = gameState.getNumAgents()
                if(agent == ghost_no-1):
                    value, action = max_value(next_state,(depth-1))
                    score_list.append(value)
                else:
                    
                    value, action = min_value(next_state,agent+1,depth)
                    score_list.append(value)

            min_score=min(score_list)
            score_len = len(score_list)
            for j in range(score_len):
                if score_list[j] == min_score:
                    worst_state = [j]
                    chosenIndex = random.choice(worst_state)
            return min_score, moves[chosenIndex]
        
        final_score,final_action= max_value(gameState,self.depth)
        
        return final_action
        util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        " Max value "
        def max_value(gameState, depth, alpha, beta):
            
            action = gameState.getLegalActions(0) 
            if gameState.isWin() or gameState.isLose() or depth == self.depth:
                return (self.evaluationFunction(gameState), None)
            
            #initialize v to - infinity
            v = -(float("inf"))
            for i in action:
                next_state = gameState.generateSuccessor(0, i)
                value, action = min_value(next_state, 1, depth, alpha, beta)
                
                if (v < value):
                    v = value
                    take_action = i

                if (v > beta):
                    return (v, take_action)

                alpha = max(alpha, v)

            return (v, take_action)

        
        def min_value(gameState, agent, depth, alpha, beta):
            
            ghost_action = gameState.getLegalActions(agent) 
            if len(ghost_action) == 0:
              return (self.evaluationFunction(gameState), None)

            #initialize v to +infinity
            v = float("inf")
            

            for i in ghost_action:
                next_state = gameState.generateSuccessor(agent, i)
                ghost_no = gameState.getNumAgents() 
                if (agent == ghost_no - 1):
                    new_depth= depth+1
                    value, action = max_value(next_state, new_depth, alpha, beta)
                else:
                    new_agent= agent+1
                    value, action = min_value(next_state, new_agent, depth, alpha, beta)
                
                if (value < v):
                    v = value
                    take_action = i

                if (v < alpha):
                    return (v, take_action)

                beta = min(beta, v)

            return (v, take_action)

        alpha = -(float("inf"))
        beta = float("inf")
        final_value, final_action = max_value(gameState, 0, alpha, beta)
        return final_action
       

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        def max_value(gameState, depth):
            
             
            if gameState.isWin() or gameState.isLose() or depth == self.depth:
                return (self.evaluationFunction(gameState), None)
            
            legal_moves = gameState.getLegalActions(0)
            v = -(float("inf"))
            take_action = None

            for i in legal_moves:
                next_state = gameState.generateSuccessor(0,i)
                value, action = exp_value(next_state, 1, depth)

                
                if (v < value):
                    v, take_action = value, i

            return (v, take_action)

        
        def exp_value(gameState, agent, depth):
          
            ghost_action = gameState.getLegalActions(agent) 
            ghost_action_len = len(ghost_action)
            if len(ghost_action) == 0:
              return (self.evaluationFunction(gameState), None)

            
            v = 0
            take_action = None

            for i in ghost_action:
                next_state = gameState.generateSuccessor(agent, i)
                ghost_no = gameState.getNumAgents()
                if (agent ==  ghost_no - 1):
                    new_depth= depth+1
                    value, action  = max_value(next_state, new_depth)
                else:
                    new_agent= agent+1
                    value, action = exp_value(next_state, new_agent , depth)

                new_value = value/ghost_action_len
                v =v+ new_value

            return (v, take_action)


        final_value, final_action = max_value(gameState, 0)
        return final_action
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    if currentGameState.isWin():
      return float("inf")
    elif currentGameState.isLose():
      return - float("inf")


    score = scoreEvaluationFunction(currentGameState)   
    current_state = currentGameState.getPacmanPosition()

    #for food
    
    Food= currentGameState.getFood() 
    food_list = Food.asList()
    food_pos = []
    for k in food_list:
        a=manhattanDistance(k,current_state)
        food_pos.append(a)
    for i in food_pos:
        if(i==0):
            score=score + 100
        else:
            score=score + (1.0/(i**2))

    #for ghosts
    ghost_list = currentGameState.getGhostStates() 
    ghost_distance = []
    scared_ghost = [] 
    distance=[]
    for ghost in ghost_list:
        ghost_position= ghost.getPosition()
        pos = manhattanDistance(current_state, ghost_position)
        distance.append(pos)
        if ghost.scaredTimer == 0:
            ghost_distance += distance
        elif ghost.scaredTimer > 0:
            scared_ghost +=  distance
    min_ghost_dist = -1
    min_scared_ghost_dist = -1
    if len(ghost_distance) > 0:
        min_ghost_dist = min(ghost_distance)
    
    elif len(scared_ghost) > 0:
        min_scared_ghost_dist = min(scared_ghost)
    
    score = score - (2  / min_ghost_dist)
    score = score - (2 * min_scared_ghost_dist)


    #For capsules
    capsules = currentGameState.getCapsules()
    capsule_len = len(capsules)   
    score = score - (15 * capsule_len)
    return score
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

