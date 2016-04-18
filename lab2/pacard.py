
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
    database = {}
    teleportDatabase = {}

    MAXWEIGHT= 99999

    while True:
        if state not in visitedStates:
            visitedStates.append(state)

        if problem.isGoalState(state):
            break



        successors = problem.getSuccessors(state)

        found = False
        if problem.isTeleporterClose(state):
            for successor in successors:
                if successor[0] in teleportDatabase:
                    state = successor[0]
                    found = True
                    database[state] = Labels.TELEPORTER
                    break
                else:
                    teleportDatabase[successor[0]] = 1

        if found:
            continue


        for successor in successors:
            if successor[0] in visitedStates:
                continue

            #if Pacard in current state can't sense anything, than the successor is safe
            notWumpus = isNotWumpus(successor[0], state, successors, problem)
            notTeleporter = isNotTeleporter(successor[0], state, successors, problem)
            notPoison = isNotPoison(successor[0], state, successors, problem)

            if notWumpus and notTeleporter and notPoison:
                database[successor[0]] = Labels.SAFE

            #if we can resolve anything about the successor, add it to the database
            if successor[0] not in database:
                if isTeleporter(successor[0], state, successors, database, problem):
                    database[successor[0]] = Labels.TELEPORTER
                elif isSafe(successor[0], state, successors, problem):
                    database[successor[0]] = Labels.SAFE
                elif isWumpus(successor[0], state, successors, database, problem):
                    database[successor[0]] = Labels.WUMPUS
                elif isPoison(successor[0], state, successors, database, problem):
                    database[successor[0]] = Labels.POISON


            if database.get(successor[0]) == Labels.SAFE:
                safeStates.add(successor[0])
                safeSuccessors.add(successor[0])
            elif successor[0] not in visitedStates:
                openStates.add(successor[0])


        currentBest = MAXWEIGHT
        safeFound = False

        # 1. if one of the successors is a teleporter, we go on that position
        for successor in successors:
            if database.get(successor[0]) == Labels.TELEPORTER:
                currentBest = 0
                state = successor[0]
                safeFound = True
                break

        # 2. if we have a safe successor, we go on that position
        if not safeFound and len(safeSuccessors) != 0:
            for safe in safeSuccessors:
                if stateWeight(safe) < currentBest:
                    safeFound = True
                    state = safe
                    currentBest = stateWeight(safe)

        # 3. if we don't have any safe successors, we risk and go to the state with best weight
        if not safeFound:
            for successor in successors:
                if successor[0] in visitedStates:
                    continue

                weight = stateWeight(successor[0])

                if weight < currentBest:
                    currentBest = weight
                    state = successor[0]

        # 4. we can't move anywhere
        if currentBest == MAXWEIGHT:
            break

        if state in safeSuccessors:
            safeSuccessors.remove(state)


    print "Current knowledge: ", database
    print "Visited states: ", visitedStates
    print "Open states: ", openStates
    print "Safe states: ", safeStates
    print
    return problem.reconstructPath(visitedStates)



################################
#functions for resolution logic#
################################

def isTeleporter(testSuccessor, state, successors, database, problem):
    clauses = set()
    literals = set()

    literals.add(Literal(Labels.TELEPORTER_GLOW, state, True))

    # notG v T x4
    for successor in successors:
        literals.add(Literal(Labels.TELEPORTER, successor[0], False))

    clauses.add(Clause(literals))

    #create clauses for all successors except the tested one, that one is the goal
    for successor in successors:
        if successor[0] == testSuccessor:
            continue

        test = database.get(successor[0], Labels.TELEPORTER) is not Labels.TELEPORTER
        clauses.add(Clause(Literal(Labels.TELEPORTER, successor[0], test)))

    clauses.add(Clause(Literal(Labels.TELEPORTER_GLOW, state, not problem.isTeleporterClose(state))))
    goal = Clause(Literal(Labels.TELEPORTER, testSuccessor, False))

    return resolution(clauses, goal)


def isWumpus(testSuccessor, state, successors, database, problem):
    clauses = set()
    literals = set()

    literals.add(Literal(Labels.WUMPUS_STENCH, state, True))

    # notS v W x4
    for successor in successors:
        literals.add(Literal(Labels.WUMPUS, successor[0], False))

    clauses.add(Clause(literals))

    #create clauses for all successors except the tested one, that one is the goal
    for successor in successors:
        if successor[0] == testSuccessor:
            continue

        test = database.get(successor[0], Labels.WUMPUS) is not Labels.WUMPUS
        clauses.add(Clause(Literal(Labels.WUMPUS, successor[0], test)))

    clauses.add(Clause(Literal(Labels.WUMPUS_STENCH, state, not problem.isWumpusClose(state))))
    goal = Clause(Literal(Labels.WUMPUS, testSuccessor, False))

    return resolution(clauses, goal)


def isPoison(testSuccessor, state, successors, database, problem):
    clauses = set()
    literals = set()

    literals.add(Literal(Labels.POISON_CHEMICALS, state, True))

    # notC v P x4
    for successor in successors:
        literals.add(Literal(Labels.POISON, successor[0], False))

    clauses.add(Clause(literals))

    #create clauses for all successors except the tested one, that one is the goal
    for successor in successors:
        if successor[0] is testSuccessor:
            continue

        test = database.get(successor[0], Labels.POISON) is not Labels.POISON
        clauses.add(Clause(Literal(Labels.POISON, successor[0], test)))

    clauses.add(Clause(Literal(Labels.POISON_CHEMICALS, state, not problem.isPoisonCapsuleClose(state))))
    goal = Clause(Literal(Labels.POISON, testSuccessor, False))

    return resolution(clauses, goal)


def isSafe(test, state, successors, problem):
    clauses = set()

    #what we know
    clauses.add(Clause(Literal(Labels.POISON_CHEMICALS, state, not problem.isPoisonCapsuleClose(state))))
    clauses.add(Clause(Literal(Labels.WUMPUS_STENCH, state, not problem.isWumpusClose(state))))
    clauses.add(Clause(Literal(Labels.TELEPORTER_GLOW, state, not problem.isTeleporterClose(state))))
    goal = Clause(Literal(Labels.SAFE, test, False))

    #literals and clauses
    # notC
    C = Literal(Labels.POISON_CHEMICALS, state, False)
    # notS
    S = Literal(Labels.WUMPUS_STENCH, state, False)
    # notG
    G = Literal(Labels.TELEPORTER_GLOW, state, False)

    # C v S v G v 0 x4
    for successor in successors:
        clauses.add(Clause([C, S, G, Literal(Labels.SAFE, successor[0], False)]))

    return  resolution(clauses, goal)

def isNotWumpus(test, state, successors, problem):
    clauses = set()

    S = Literal(Labels.WUMPUS_STENCH, state, False)

    # S v notW x4
    for successor in successors:
        clauses.add(Clause([S, Literal(Labels.WUMPUS, successor[0], True)]))


    # notS
    clauses.add(Clause(Literal(Labels.WUMPUS_STENCH, state, not problem.isWumpusClose(state))))
    goal = Clause(Literal(Labels.WUMPUS, test, True))


    return resolution(clauses, goal)

def isNotPoison(test, state, successors, problem):
    clauses = set()

    C = Literal(Labels.POISON_CHEMICALS, state, False)

    # C v notP x4
    for successor in successors:
        clauses.add(Clause([C, Literal(Labels.POISON, successor[0], True)]))


    # notC
    clauses.add(Clause(Literal(Labels.POISON_CHEMICALS, state, not problem.isPoisonCapsuleClose(state))))
    goal = Clause(Literal(Labels.POISON, test, True))

    return resolution(clauses, goal)

def isNotTeleporter(test, state, successors, problem):
    clauses = set()

    G = Literal(Labels.TELEPORTER_GLOW, state, False)

    # G v notT x4
    for successor in successors:
        clauses.add(Clause([G, Literal(Labels.TELEPORTER, successor[0], True)]))

    # notG
    clauses.add(Clause(Literal(Labels.TELEPORTER_GLOW, state, not problem.isTeleporterClose(state))))
    goal = Clause(Literal(Labels.TELEPORTER, test, True))

    return resolution(clauses, goal)


# Abbreviations
lbs = logicBasedSearch