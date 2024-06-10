# -------------------------------------------------------------------
# PLEASE UPDATE THIS FILE.
# Pledge maze solver.
#
# __author__ = 'Jeffrey Chan'
# __copyright__ = 'Copyright 2024, RMIT University'
# -------------------------------------------------------------------


from maze.maze3D import Maze3D
from solving.mazeSolver import MazeSolver
from maze.util import Coordinates3D

from random import choice
from enum import Enum


class PledgeDirections(Enum):
    """
    Subclass of Directions class used for Pledge
    """

    NORTH = Coordinates3D(0, 1, 0)
    NORTH_EAST = Coordinates3D(1, 0, 0)  # Up
    EAST = Coordinates3D(0, 0, 1)
    SOUTH = Coordinates3D(0, -1, 0)
    SOUTH_WEST = Coordinates3D(-1, 0, 0)  # Down
    WEST = Coordinates3D(0, 0, -1)

    # Function to get coordinate, though can be done with .value
    def getValue(self) -> Coordinates3D:
        """
        Gets Coordinates3D value of direction
        """
        return self.value

    # Functions to get the next direction
    def getRight(self):
        """
        Gets the right direction of a current value according to the order of enums
        """
        directions = list(PledgeDirections)
        current_index = directions.index(self)
        next_index = (current_index + 1) % len(
            directions
        )  # Cycle to the beginning if at the end
        return directions[next_index]

    def getLeft(self):
        """
        Gets the left direction of a current value according to the order of enums
        """
        directions = list(PledgeDirections)
        current_index = directions.index(self)
        next_index = (current_index - 1) % len(
            directions
        )  # Cycle to the beginning if at the end
        return directions[next_index]

    # Function to get the opposite direction
    def getOppositeDirection(self):
        """
        Get the opposite direction of the current direction,
        which is currently 3 rotations to the left or right
        """
        directions = list(PledgeDirections)
        current_index = directions.index(self)
        next_index = (current_index + 3) % len(
            directions
        )  # Cycle to the beginning if at the end
        return directions[next_index]

    def getNumberOfTurns(self, currDirection, destDirection, wallFollowerType) -> int:
        """
        Takes currDirection of algorithm at cell and a destDirection of algorithm,
        which is the direction of the next cell.
        Also takes a right or left string to indicate direction of wall follower
        Tries to return the number of turns made to get the destDirection
        """
        numTurns = 0
        tempTurnCounter = 0
        currDirection = currDirection.getOppositeDirection()
        # Turn counter for right wall follower
        if wallFollowerType == "right":
            # Do one turn first, to avoid base case
            currDirection.getLeft()
            tempTurnCounter += 1
            # Calculate number of turns
            while currDirection != destDirection:
                currDirection = currDirection.getLeft()
                tempTurnCounter += 1
            # Exit loop as number of turns gathered.
            # After getting number of turns, calculate number of turns to return
            # 60 degree right turn
            if tempTurnCounter == 1:
                numTurns = 2
            # 120 degree right turn
            elif tempTurnCounter == 2:
                numTurns = 1
            # 0 degree turn
            elif tempTurnCounter == 3:
                numTurns = 0
            # -60 degree left turn
            elif tempTurnCounter == 4:
                numTurns = -1
            # -120 degree left turn
            elif tempTurnCounter == 5:
                numTurns = -2
            # -180 degree left turn
            elif tempTurnCounter == 6:
                numTurns = -3
        # Turn counter for left wall follower
        elif wallFollowerType == "left":
            # Do one turn first, to avoid base case
            currDirection.getLeft()
            tempTurnCounter += 1
            # Calculate number of turns
            while currDirection != destDirection:
                currDirection = currDirection.getLeft()
                tempTurnCounter += 1
            # Exit loop as number of turns gathered.

        else:
            raise ("Unexpected wallFollowerType passed as argument")

        # return numTurns for pledge algorithm
        return numTurns


class PledgeMazeSolver(MazeSolver):
    """
    Pledge solver implementation.  You'll need to complete its implementation for task B.
    """

    def __init__(self):
        super().__init__()
        self.m_name = "pledge"

    def solveMaze(self, maze: Maze3D, entrance: Coordinates3D):
        # TODO: Implement this for task B!
        self.m_solved = False

        # select starting cell
        startCoord: Coordinates3D = entrance

        currCell: Coordinates3D = startCoord

        # Select a direction of preference, currently random
        # selectDirection: PledgeDirections = choice(list(PledgeDirections))
        selectDirection: PledgeDirections = PledgeDirections.NORTH

        print("Randomised pledge direction is: ", selectDirection)

        # Beginning direction
        currDirection: PledgeDirections = selectDirection
        while currCell not in maze.getExits():
            # This code is used to only append when the cell visited is unique.
            if (currCell, False) not in self.m_solverPath:
                self.solverPathAppend(currCell)

            # find all neighbours of current cell
            neighbours: list[Coordinates3D] = maze.neighbours(currCell)

            # filter to ones that haven't been visited and within boundary and doesn't have a wall between them
            possibleNeighs: list[Coordinates3D] = [
                neigh
                for neigh in neighbours
                if not maze.hasWall(currCell, neigh)
                and (neigh.getRow() >= -1)
                and (neigh.getRow() <= maze.rowNum(neigh.getLevel()))
                and (neigh.getCol() >= -1)
                and (neigh.getCol() <= maze.colNum(neigh.getLevel()))
            ]

            # Travel in selectDirection until hitting a wall
            # If there is not a wall in selectDirection
            if currCell + selectDirection.getValue() in possibleNeighs:
                # Move in that direction
                currCell = currCell + selectDirection.getValue()

            # Else there is a wall, perform wall following
            else:
                # Start counter at 0; negative is a left turn, and positive is a right turn
                turnCounter: int = 0

                # turn left instead of right (to touch wall) for right-wall follower
                # Check wall one rotation to the left
                destDirection = currDirection.getLeft()
                turnCounter += -1
                # While cannot move forward - this loop is redundant for first iteration, as there can only be at most three left turns,
                # but kept for readability
                while (currCell + destDirection.getValue()) not in possibleNeighs:
                    # Check wall one rotation to the left, save to counter
                    destDirection = destDirection.getLeft()
                    turnCounter += -1

                # Increment turnCounter by value of turns
                # After finding a valid neighbour, set currDirection to destDirection
                currDirection = destDirection
                # Traverse in that direction
                currCell = currCell + currDirection.getValue()

                # Now do right wall-follower until counter is 0, should be -1 or -2 when starting.
                while currCell not in maze.getExits():
                    print("Turn counter is: ", turnCounter)
                    # This code is used to only append when the cell visited is unique.
                    if (currCell, False) not in self.m_solverPath:
                        self.solverPathAppend(currCell)

                    # find all neighbours of current cell
                    neighbours: list[Coordinates3D] = maze.neighbours(currCell)

                    # filter to ones that haven't been visited and within boundary and doesn't have a wall between them
                    possibleNeighs: list[Coordinates3D] = [
                        neigh
                        for neigh in neighbours
                        if not maze.hasWall(currCell, neigh)
                        and (neigh.getRow() >= -1)
                        and (neigh.getRow() <= maze.rowNum(neigh.getLevel()))
                        and (neigh.getCol() >= -1)
                        and (neigh.getCol() <= maze.colNum(neigh.getLevel()))
                    ]

                    destDirection = currDirection.getOppositeDirection()
                    # Right wall follower, rotate left by one.
                    destDirection = destDirection.getLeft()
                    # rotate left until you can move forward
                    while (currCell + destDirection.getValue()) not in possibleNeighs:
                        destDirection = destDirection.getLeft()

                    turnCounter += PledgeDirections.getNumberOfTurns(
                        self, currDirection, destDirection, "right"
                    )

                    # if turncounter is 0, we can resume in the preferred direction.
                    if turnCounter == 0:
                        break

                    # Continue wall follower otherwise
                    currDirection = destDirection
                    # Traverse to next cell
                    currCell = currCell + currDirection.getValue()

                # end wall follower when currCell is an exit or turnCounter is 0.

        # ensure we are currently at the exit
        if currCell in maze.getExits():
            # append exit cell to solverPath
            self.solverPathAppend(currCell)
            self.solved(entrance, currCell)
