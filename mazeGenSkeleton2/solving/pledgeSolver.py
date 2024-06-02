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

    def getNumberOfTurns(self, currDirection, destDirection, wallFollowerType):
        """
        Takes currDirection of algorithm at cell and a destDirection of algorithm,
        which is the direction of the next cell.
        Also takes a right or left string to indicate direction of wall follower
        Tries to return the number of turns made to get the destDirection
        """
        directions = list(PledgeDirections)
        # numTurns = directions.index(self)
        # if (wallFollowerType == "right"):
        #     while currDirection != destDirection:
        #         currDirection = currDirection.getLeft()

        # elif (wallFollowerType == "left"):

        # else:
        #     raise("Unexpected wallFollowerType passed as argument")
        # return numTurns

        pass



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

        # Select a direction of preference
        selectDirection: PledgeDirections = choice(list(PledgeDirections))

        while currCell not in maze.getExits():
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
                # Perform wall following
                # Start counter at 0; negative is a left turn, and positive is a right turn
                counter: int = 0
                # currDirection is selectDirection
                currDirection = selectDirection
                # turn left instead of right for right-wall follower
                # Get opposite direction (which cell you came from)
                currDirection = currDirection.getOppositeDirection()

                # Check wall one rotation to the left
                currDirection = currDirection.getRight()

                # While cannot move forward
                while (currCell + currDirection.getValue()) not in possibleNeighs:
                    # Check wall one rotation to the left, save to counter
                    currDirection = currDirection.getRight()

                # Save left turn as negative because
                counter += -1
                # Move forward while there is no wall
                while currCell not in maze.getExits() or counter != 0:
                    currCell = currCell + currDirection.getValue()

                while currCell not in maze.getExits() or counter != 0:
                    # Get opposite direction (which cell you came from)
                    currDirection = currDirection.getOppositeDirection()

                    # Check wall one rotation to the right, change this to change which wall to follow
                    currDirection = currDirection.getLeft()
                    # While cannot move forward
                    while (currCell + currDirection.getValue()) not in possibleNeighs:
                        # Check wall one rotation to the right, change this to change which wall to follow
                        currDirection = currDirection.getLeft()

                    # Move forward if there is no wall
                    currCell = currCell + currDirection.getValue()

        # ensure we are currently at the exit
        if currCell in maze.getExits():
            # append exit cell to solverPath
            self.solverPathAppend(currCell)
            self.solved(entrance, currCell)
