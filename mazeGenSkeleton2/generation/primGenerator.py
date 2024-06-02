# -------------------------------------------------------------------
# DON'T CHANGE THIS FILE.
# Prim's maze generator.
#
# __author__ = 'Jeffrey Chan'
# __copyright__ = 'Copyright 2024, RMIT University'
# -------------------------------------------------------------------

from maze.maze3D import Maze3D
from maze.util import Coordinates3D
from generation.mazeGenerator import MazeGenerator

# Imported libraries
import heapq
from random import randint, choice
from queue import PriorityQueue

class PrimMazeGenerator(MazeGenerator):
    """
    Prim's algorithm maze generator.
    TODO: Complete the implementation (Task A)
    """
    def inPriorityQueue(self, queue, item):
        """
        Searches through priority queue for a passed item 
        """
        return any(element[1] == item for element in queue)
    
    def generateMaze(self, maze: Maze3D):
        # TODO: Implement this method for task A.
        # make sure we start the maze with all walls there
        maze.initCells(True)

        # select starting cell
        # random floor
        randomLevel = randint(0, maze.levelNum() - 1)
        # start coordinate generated
        startCoord: Coordinates3D = Coordinates3D(
            randomLevel,
            randint(0, maze.rowNum(randomLevel) - 1),
            randint(0, maze.colNum(randomLevel) - 1),
        )

        currCell: Coordinates3D = startCoord

        visited: set[Coordinates3D] = set([startCoord])

        # frontier set will hold all possible neighbours that can be visited
        frontier = [] 

        totalCells = sum(
            [maze.rowNum(l) * maze.colNum(l) for l in range(maze.levelNum())]
        )

        # while all the cells in the maze are not visited:
        while len(visited) < totalCells:
            neighbours: list[Coordinates3D] = maze.neighbours(currCell)
            # find non-visited neighbours from list of neighbours
            nonVisitedNeighs: list[Coordinates3D] = [
                neigh
                for neigh in neighbours
                if neigh not in visited
                and neigh.getRow() >= 0
                and neigh.getRow() < maze.rowNum(neigh.getLevel())
                and neigh.getCol() >= 0
                and neigh.getCol() < maze.colNum(neigh.getLevel())
            ]
            # adds each element from the list of neighbours 
            #  and give them their weights here
            for neigh in nonVisitedNeighs:
                if not self.inPriorityQueue(frontier, neigh): 
                    heapq.heappush(frontier, (1, neigh))

            # visit any node in the frontier set and remove from the set
            priority, selectedNode = heapq.heappop(frontier)

            # find which node to carve from
            neighbours = maze.neighbours(selectedNode)
            visitedNeighs: list[Coordinates3D] = [
                neigh
                for neigh in neighbours
                if neigh in visited
                and neigh.getRow() >= 0
                and neigh.getRow() < maze.rowNum(neigh.getLevel())
                and neigh.getCol() >= 0
                and neigh.getCol() < maze.colNum(neigh.getLevel())
            ]

            # Choose a random vsiited neighbour to carve a wall from
            selectedNeighbour = choice(visitedNeighs)

            # remove wall between the current cell and the chosen node
            maze.removeWall(selectedNeighbour, selectedNode)

            # mark chosen node as visited
            visited.add(selectedNode)

            # change currCell for next iteration
            currCell = selectedNode
        # loop exits when all cells are in the visited set
        self.m_mazeGenerated = True
        # pass
