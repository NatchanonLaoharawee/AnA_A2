# -------------------------------------------------------------------
# PLEASE UPDATE THIS FILE.
# Wall following maze solver.
#
# __author__ = 'Jeffrey Chan'
# __copyright__ = 'Copyright 2024, RMIT University'
# -------------------------------------------------------------------


from maze.maze3D import Maze3D
from solving.mazeSolver import MazeSolver
from maze.util import Coordinates3D

from enum import Enum

class Directions(Enum):
    """
    Convention is (level, row, col) for constructing 3D Coordinates
    Enums for level, row, and col
    Has directions: North, North-East, East, South, South-West, West
    """
    NORTH = (0, 1, 0)
    NORTH_EAST = (1, 0, 0)
    EAST = (0, 0, 1)
    SOUTH = (0, -1, 0)
    SOUTH_WEST = (-1, 0, 0)
    WEST = (0, 0, -1)

class WallFollowingMazeSolver(MazeSolver):
    """
    Wall following solver implementation.  You'll need to complete its implementation for task B.
    """

    def __init__(self):
        super().__init__()
        self.m_name = "wall"


    def solveMaze(self, maze: Maze3D, entrance: Coordinates3D):
        # TODO: Implement this for task B!
        self.m_solved = False
        startCoord: Coordinates3D = entrance

        # Set beginning direction
        BEGINNING_DIRECTION = Directions.NORTH
        
        # Follow right wall
        # RIGHT = 

        # currCell is startCoord
        currCell : Coordinates3D = startCoord
        while currCell not in maze.getExits():
            print()
        pass


