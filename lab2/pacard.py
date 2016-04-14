
"""
In pacard.py, you will implement the search algorithm  based on refutation resolution 
which will lead Pacard through the cave of the evil GhostWumpus.
"""

import util
from logic import * 

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

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
        state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
        actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def miniWumpusSearch(problem): 
    """
    A sample pass through the miniWumpus layout. Your solution will not contain 
    just three steps! Optimality is not the concern here.
    """
    from game import Directions
    e = Directions.EAST 
    n = Directions.NORTH
    return  [e, n, n]

def logicBasedSearch(problem):
    """

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())

    print "Does the Wumpus's stench reach my spot?", 
               \ problem.isWumpusClose(problem.getStartState())

    print "Can I sense the chemicals from the pills?", 
               \ problem.isPoisonCapsuleClose(problem.getStartState())

    print "Can I see the glow from the teleporter?", 
               \ problem.isTeleporterClose(problem.getStartState())
    
    (the slash '\\' is used to combine commands spanning through multiple lines - 
    you should remove it if you convert the commands to a single line)
    
    Feel free to create and use as many helper functions as you want.

    A couple of hints: 
        * Use the getSuccessors method, not only when you are looking for states 
        you can transition into. In case you want to resolve if a poisoned pill is 
        at a certain state, it might be easy to check if you can sense the chemicals 
        on all cells surrounding the state. 
        * Memorize information, often and thoroughly. Dictionaries are your friends and 
        states (tuples) can be used as keys.
        * Keep track of the states you visit in order. You do NOT need to remember the
        tranisitions - simply pass the visited states to the 'reconstructPath' method 
        in the search problem. Check logicAgents.py and search.py for implementation.
    """
    # array in order to keep the ordering
    visitedStates = []
    startState = problem.getStartState()
    visitedStates.append(startState)
    """
    ####################################
    ###                              ###
    ###        YOUR CODE HERE        ###
    ###                              ###
    ####################################
    """

    open = util.PriorityQueue()
    open.push(startState,1)
    wumpusDict = dict()
    capsuleDict = dict()
    teleporterDict = dict()
    clauses = set()

    clauses.add(Clause(Literal('o', startState, False)))
    clauses.add(Clause(Literal('t', startState, True)))
    clauses.add(Clause(Literal('p', startState, True)))
    clauses.add(Clause(Literal('w', startState, True)))

    while not open.isEmpty():
        state = open.pop()
        if state not in visitedStates:
            visitedStates.append(state)





def checkState(state, problem, clauses):
    if not problem.isWumpusClose(state):
        clauses.add(Clause(set([Literal('w', (state[0]-1, state[1]), True)])))
        clauses.add(Clause(set([Literal('w', (state[0]+1, state[1]), True)])))
        clauses.add(Clause(set([Literal('w', (state[0], state[1]-1), True)])))
        clauses.add(Clause(set([Literal('w', (state[0], state[1]+1), True)])))
        clauses.add(Clause(Literal('s', state, True)))

    else:
        clauses.add(Clause(Literal('s', state, False)))

    if not problem.isPoisonCapsuleClose(state):
        clauses.add(Clause(set([Literal('p', (state[0]-1, state[1]), True)])))
        clauses.add(Clause(set([Literal('p', (state[0]+1, state[1]), True)])))
        clauses.add(Clause(set([Literal('p', (state[0], state[1]-1), True)])))
        clauses.add(Clause(set([Literal('p', (state[0], state[1]+1), True)])))
        clauses.add(Clause(Literal('c', state, True)))
    else:
        clauses.add(Clause(Literal('c', state, False)))

    if not problem.isTeleporterClose(state):
        clauses.add(Clause(set([Literal('t', (state[0]-1, state[1]), True)])))
        clauses.add(Clause(set([Literal('t', (state[0]+1, state[1]), True)])))
        clauses.add(Clause(set([Literal('t', (state[0], state[1]-1), True)])))
        clauses.add(Clause(set([Literal('t', (state[0], state[1]+1), True)])))
        clauses.add(Clause(Literal('g', state, True)))
    else:
        clauses.add(Clause(Literal('g', state, False)))

    if problem.isTeleporter(state):
        clauses.add(Clause(set([Literal('t', state, False)])))
    else:
        clauses.add(Clause(set([Literal('t', state, True)])))

    if problem.isWumpus(state):
        clauses.add(Clause(set([Literal('w', state, False)])))
    else:
        clauses.add(Clause(set([Literal('w', state, True)])))

    if problem.isPoisonCapsule(state):
        clauses.add(Clause(set([Literal('p', state, False)])))
    else:
        clauses.add(Clause(set([Literal('p', state, True)])))
# Abbreviations
lbs = logicBasedSearch
