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
from random import randint, choice


class PrimMazeGenerator(MazeGenerator):
    """
    Prim's algorithm maze generator.
    TODO: Complete the implementation (Task A)
    """

    def generateMaze(self, maze: Maze3D):
        # TODO: Implement this method for task A.
        # make sure we start the maze with all walls there
        maze.initCells(True)

        # select starting cell
        # random floor
        startLevel = randint(0, maze.levelNum() - 1)
        # start coordinate generated
        startCoord: Coordinates3D = Coordinates3D(
            startLevel,
            randint(0, maze.rowNum(startLevel) - 1),
            randint(0, maze.colNum(startLevel) - 1),
        )

        # pq = PriorityQueue

        # put the starting coordinate in the priority queue, with a weight of 0
        # pq.put(0, startCoord)

        currCell: Coordinates3D = startCoord

        visited: set[Coordinates3D] = set([startCoord])

        # frontier set will hold all possible neighbours that can be visited
        frontier: set[Coordinates3D] = set()

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
            # adds each element from the list (not the whole list as an element)
            frontier.update(nonVisitedNeighs)

            # (YOU CAN ADD WEIGHTS HERE TODO:)visit any node in the frontier set
            selectedNode = choice(list(frontier))

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
            selectedNeighbour = choice(visitedNeighs)

            # remove wall between the current cell and the chosen node
            maze.removeWall(selectedNeighbour, selectedNode)

            # mark chosen node as visited
            visited.add(selectedNode)

            # remove selected node from frontier set (so it is not chosen again)
            frontier.remove(selectedNode)

            # change currCell for next iteration
            currCell = selectedNode
        # while loop exits when all cells are in the visited set
        self.m_mazeGenerated = True
        # pass
