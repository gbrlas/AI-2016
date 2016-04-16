
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

    ####################################
    ###                              ###
    ###        YOUR CODE HERE       ###
    ###                              ###
    ####################################

    safeSuccessors = set()
    safeStates = set()
    openStates = set()
    state = startState
    knowledge = {}

    while True:
        if state not in visitedStates:
            visitedStates.append(state)

        if problem.isGoalState(state):
            break

        successors = problem.getSuccessors(state)

        for successor in successors:
            if successor[0] in visitedStates:
                continue

            notWumpus = isNotWumpus(successor[0], state, successors, problem)
            notTeleporter = isNotTeleporter(successor[0], state, successors, problem)
            notPoison = isNotPoison(successor[0], state, successors, problem)

            if notWumpus and notTeleporter and notPoison:
                knowledge[successor[0]] = Labels.SAFE


            if successor[0] not in knowledge:
                if isTeleporter(successor[0], state, successors, knowledge, problem):
                    knowledge[successor[0]] = Labels.TELEPORTER
                elif isSafe(successor[0], state, successors, problem):
                    knowledge[successor[0]] = Labels.SAFE
                elif isWumpus(successor[0], state, successors, knowledge, problem):
                    knowledge[successor[0]] = Labels.WUMPUS
                elif isPoison(successor[0], state, successors, knowledge, problem):
                    knowledge[successor[0]] = Labels.POISON

            if knowledge.get(successor[0]) == Labels.SAFE:
                safeStates.add(successor[0])

                if successor[0] not in visitedStates:
                    safeSuccessors.add(successor[0])
            elif successor[0] not in visitedStates:
                openStates.add(successor[0])

        currentBest = 99999
        safeFound = False

        for safe in safeSuccessors:
            if stateWeight(safe) < currentBest:
                safeFound = True
                state = safe
                currentBest = stateWeight(safe)

        for successor in successors:
            if successor[0] in visitedStates:
                continue

            weight = stateWeight(successor[0])

            if knowledge.get(successor[0]) == Labels.TELEPORTER:
                currentBest = 0
                state = successor[0]
            elif knowledge.get(successor[0]) is None and weight < currentBest and not safeFound:
                currentBest = weight
                state = successor[0]

            if currentBest == 99999:
                for open in openStates:
                    if open in visitedStates:
                        continue

                    weight =stateWeight(open)

                    if knowledge.get(successor[0]) is None and weight < currentBest and not safeFound:
                        currentBest = weight
                        state = open

        if state in openStates:
            openStates.remove(state)

        if state in safeSuccessors:
            safeSuccessors.remove(state)

        if currentBest == 99999:
            break

    print "Current knowledge: ", knowledge
    print "Visited states: ", visitedStates
    print "Open states: ", openStates
    print "Safe states: ", safeStates
    print
    return problem.reconstructPath(visitedStates)


def nothingImpliesSafe(state, successors):
    clauses = set()

    C = Literal(Labels.POISON_CHEMICALS, state, False)
    S = Literal(Labels.WUMPUS_STENCH, state, False)
    G = Literal(Labels.TELEPORTER_GLOW, state, False)

    for successor in successors:
        clauses.add(Clause([C, S, G, Literal(Labels.SAFE, successor[0], False)]))

    return clauses

def chemicalsImpliesPoison(state, successors):
    literals = set()

    literals.add(Literal(Labels.POISON_CHEMICALS, state, True))

    for successor in successors:
        literals.add(Literal(Labels.POISON, successor[0], False))

    return set([Clause(literals)])

def stenchImpliesWumpus(state, successors):
    literals = set()

    literals.add(Literal(Labels.WUMPUS_STENCH, state, True))

    for successor in successors:
        literals.add(Literal(Labels.WUMPUS, successor[0], False))

    return set([Clause(literals), Clause(Literal(Labels.WUMPUS, (-1, -1), True))])

def glowImpliesTeleporter(state, successors):
    literals = set()

    literals.add(Literal(Labels.TELEPORTER_GLOW, state, True))
    for successor in successors:
        literals.add(Literal(Labels.TELEPORTER, successor[0], False))

    return set([Clause(literals)])

def noStenchImpliesNoWumpus(state, successors):
    clauses = set()

    S = Literal(Labels.WUMPUS_STENCH, state, False)

    for successor in successors:
        clauses.add(Clause([S, Literal(Labels.WUMPUS, successor[0], True)]))

    return clauses

def noPoisonChemicalsImpliesNoPoison(state, successors):
    clauses = set()

    C = Literal(Labels.POISON_CHEMICALS, state, False)

    for successor in successors:
        clauses.add(Clause([C, Literal(Labels.POISON, successor[0], True)]))

    return clauses

def noGlowImpliesNoTeleporter(state, successors):
    clauses = set()

    G = Literal(Labels.TELEPORTER_GLOW, state, False)

    for successor in successors:
        clauses.add(Clause([G, Literal(Labels.TELEPORTER, successor[0], True)]))

    return clauses

def isTeleporter(testSuccessor, state, successors, knowledge, problem):
    clauses = set()


    for successor in successors:
        if successor[0] == testSuccessor:
            continue

        test = knowledge.get(successor[0], Labels.TELEPORTER) is not Labels.TELEPORTER
        clauses.add(Clause(Literal(Labels.TELEPORTER, successor[0], test)))

    clauses.add(Clause(Literal(Labels.TELEPORTER_GLOW, state, not problem.isTeleporterClose(state))))
    goal = Clause(Literal(Labels.TELEPORTER, testSuccessor, False))

    return resolution(clauses | glowImpliesTeleporter(state, successors), goal)

def isWumpus(testSuccessor, state, successors, knowledge, problem):
    clauses = set()

    for successor in successors:
        if successor[0] == testSuccessor:
            continue

        test = knowledge.get(successor[0], Labels.WUMPUS) is not Labels.WUMPUS
        clauses.add(Clause(Literal(Labels.WUMPUS, successor[0], test)))

    clauses.add(Clause(Literal(Labels.WUMPUS_STENCH, state, not problem.isWumpusClose(state))))
    goal = Clause(Literal(Labels.WUMPUS, testSuccessor, False))

    return resolution(clauses | stenchImpliesWumpus(state, successors), goal)

def isPoison(testSuccessor, state, successors, knowledge, problem):
    clauses = set()

    for successor in successors:
        if successor[0] is testSuccessor:
            continue

        test = knowledge.get(successor[0], Labels.POISON) is not Labels.POISON
        clauses.add(Clause(Literal(Labels.POISON, successor[0], test)))

    clauses.add(Clause(Literal(Labels.POISON_CHEMICALS, state, not problem.isPoisonCapsuleClose(state))))
    goal = Clause(Literal(Labels.POISON, testSuccessor, False))

    return resolution(clauses | chemicalsImpliesPoison(state, successors), goal)

def isSafe(successor, state, successors, problem):
    clauses = set()

    clauses.add(Clause(Literal(Labels.POISON_CHEMICALS, state, not problem.isPoisonCapsuleClose(state))))
    clauses.add(Clause(Literal(Labels.WUMPUS_STENCH, state, not problem.isWumpusClose(state))))
    clauses.add(Clause(Literal(Labels.TELEPORTER_GLOW, state, not problem.isTeleporterClose(state))))

    goal = Clause(Literal(Labels.SAFE, successor, False))

    return  resolution(clauses | nothingImpliesSafe(state, successors), goal)

def isNotWumpus(successor, state, successors, problem):
    clauses = set()

    clauses.add(Clause(Literal(Labels.WUMPUS_STENCH, state, not problem.isWumpusClose(state))))

    goal = Clause(Literal(Labels.WUMPUS, successor, True))

    return resolution(clauses | noStenchImpliesNoWumpus(state, successors), goal)

def isNotPoison(successor, state, successors, problem):
    clauses = set()

    clauses.add(Clause(Literal(Labels.POISON_CHEMICALS, state, not problem.isPoisonCapsuleClose(state))))

    goal = Clause(Literal(Labels.POISON, successor, True))

    return resolution(clauses | noPoisonChemicalsImpliesNoPoison(state, successors), goal)

def isNotTeleporter(successor, state, successors, problem):
    clauses = set()

    clauses.add(Clause(Literal(Labels.TELEPORTER_GLOW, state, not problem.isTeleporterClose(state))))

    goal = Clause(Literal(Labels.TELEPORTER, successor, True))

    return resolution(clauses | noGlowImpliesNoTeleporter(state, successors), goal)


# Abbreviations
lbs = logicBasedSearch