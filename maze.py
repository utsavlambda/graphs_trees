"""Maze generation and path finding"""

__author__ = "talatiuh"

from random import shuffle, randint, random


class Cell:
    """
    Cell objects represent a single maze location with up-to 4 walls.

    The .N, .E, .S, .W attributes represent the walls in the North,
    East, South and West directions. If the attribute is True, there is a
    wall in the given direction.

    The .x and .y attributes store the coordinates of the cell.
    """

    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.N = True
        self.E = True
        self.S = True
        self.W = True

        self.visited = False

        self.coordinates = ['N', 'S', 'E', 'W']

    def remove_wall(self, direction):
        """
        Remove one wall - keep all neighbors consistent
        Direction is one of these strings: 'N', 'E', 'S', 'W'
        """
        direction = direction.upper()

        loc = " @(x=%d, y=%d)" % (self.x, self.y)
        if direction == "W":
            if self.x < 1:
                raise ValueError("cannot remove side wall on west" + loc)
            if self.W:
                self.W = False
                assert maze[self.x - 1][self.y].E
                maze[self.x - 1][self.y].E = False
        if direction == "E":
            if self.x >= size_x - 1:
                raise ValueError("cannot remove side wall on east" + loc)
            if self.E:
                self.E = False
                assert maze[self.x + 1][self.y].W
                maze[self.x + 1][self.y].W = False
        if direction == "N":
            if self.y < 1:
                raise ValueError("cannot remove side wall on north" + loc)
            if self.N:
                self.N = False
                assert maze[self.x][self.y - 1].S
                maze[self.x][self.y - 1].S = False
        if direction == "S":
            if self.y >= size_y - 1:
                raise ValueError("cannot remove side wall on south" + loc)
            if self.S:
                self.S = False
                assert maze[self.x][self.y + 1].N
                maze[self.x][self.y + 1].N = False

    def has_wall(self, direction):
        """
        True if there is a wall in the given direction
        Direction is one of these strings: 'N', 'E', 'S', 'W'
        """
        return getattr(self, direction.upper())


# Global variables for the maze and its size
size_x = size_y = 32
maze = [[Cell(x, y) for y in range(size_y)] for x in range(size_x)]


def building_wall_recursive(x, y):
    """
    create DIRECTION tuple which contains N,S,E,W
    Randomize the directions
    make sure test_conditions are met:
    """
    maze[x][y].visited = True

    # NOTE this order shouldn't matter once we randomize the coordinates
    direction = [(x - 1, y), (x, y + 1), (x + 1, y), (x, y - 1)]

    shuffle(direction)

    leny = (size_y - 1)
    lenx = (size_x - 1)
    for (i1, i2) in direction:
        if (i2 < 0 ):
            continue
        elif(i2 > leny):
            continue
        elif(i1 < 0):
            continue
        elif(i1 > lenx):
            continue
        elif(maze[i1][i2].visited):
            continue
        if i1 == x:
            maze[x][max(y, i2)].remove_wall('N')
        elif i2 == y:
            maze[min(x, i1)][y].remove_wall('E')

        building_wall_recursive(i1, i2)


def build_maze():
    """
    Build a valid maze by tearing down walls

    The function has access to the following global variables:
        size_x - integer, the horizontal size of the maze
        size_y - integer, the vertical size of the maze
        maze - a two dimensional array (list of lists) for all cells
            e.g. maze[3][4] is a Cell object for x=3, y=4

    This function does not need to return any value but should modify the
    cells (walls) to create a perfect maze.
    When the function is invoked all cells have all their four walls standing.
    """
    x = randint(0, size_x - 1)
    y = randint(0, size_y - 1)
    building_wall_recursive(x, y)


def generate_path(lst, start, end):
    """
    current is the last element of path
    if current is end RETURN true

    iterate over directions:
        if there is no wall towards the direction and next cell
        is not in the path:
            append next cell to path
            make a move (rec)
            if move returned successfully, RETURN true:
            otherwise
            remove the last element from the path
    """
    xx = start[0]
    yy = start[1]

    east = 'E'
    north = 'N'
    west = 'W'
    south = 'S'

    verified = True

    # base condition(s)
    if start in lst:
        return
    lst.append(start)
    if start == end:
        return verified


    else:
        for move in maze[xx][yy].coordinates:
            if (move == north) and (not maze[xx][yy].has_wall('N')):
                if generate_path(lst, (xx, yy - 1), end):
                    return verified

            if (move == east) and (not maze[xx][yy].has_wall('E')):
                if generate_path(lst, (xx + 1, yy), end):
                    return verified

            if (move == south) and (not maze[xx][yy].has_wall('S')):
                if generate_path(lst, (xx, yy + 1), end):
                    return verified

            if (move == west) and (not maze[xx][yy].has_wall('W')):
                if generate_path(lst, (xx - 1, yy), end):
                    return verified

        # pop() removes element
        lst.pop()
        generate_path(lst, lst[-1], end)


def find_path(start, end):
    """
    Find a path from the start position to the end

    The start and end parameters are coordinate pairs (tuples) for the
    start and end (target) position. E.g. (0, 0) or (7, 13).

    The function has access to the following global variables:
        size_x - integer, the horizontal size of the maze
        size_y - integer, the vertical size of the maze
        maze - a two dimensional array (list of lists) for all cells
            e.g. maze[3][4] is a Cell object for x=3, y=4

    The function is invoked after build_maze removed the walls to create a
    perfect maze.

    This function shall return a list of coordinate pairs (tuples or lists)
    w`hich list the cell coordinates on a valid path from start to end.
    E.g.: [(0, 0), (0, 1), (1, 1), (2, 1), (3, 1), ..., (7, 13)]
    """
    lst = []
    generate_path(lst, start, end)
    return lst


###############################################################################
# Testing and visualizing results - no need to understand and/or change
def draw_maze(start=None, end=None, path=None):
    """Draw the maze and the path in a graphical window"""
    import tkinter
    cell_size = 20
    master = tkinter.Tk()
    canvas = tkinter.Canvas(master, width=size_x * cell_size + 1,
                            height=size_y * cell_size + 1,
                            bd=0, highlightthickness=0, relief='ridge')
    canvas.pack()
    for x in range(size_x):
        for y in range(size_y):
            if maze[x][y].N:
                canvas.create_line(cell_size * x, cell_size * y,
                                   cell_size * (x + 1), cell_size * y)
            if maze[x][y].E:
                canvas.create_line(cell_size * (x + 1), cell_size * y,
                                   cell_size * (x + 1), cell_size * (y + 1))
            if maze[x][y].S:
                canvas.create_line(cell_size * x, cell_size * (y + 1),
                                   cell_size * (x + 1), cell_size * (y + 1))
            if maze[x][y].W:
                canvas.create_line(cell_size * x, cell_size * y,
                                   cell_size * x, cell_size * (y + 1))

    if path is not None:
        line = [x * cell_size + cell_size // 2 for step in path for x in step]
        canvas.create_line(*line, fill='red', width=2)

    radius = cell_size // 3
    if start is not None:
        img_start = [cell_size * x + cell_size // 2 for x in start]
        canvas.create_oval(img_start[0] - radius,
                           img_start[1] - radius,
                           img_start[0] + radius,
                           img_start[1] + radius, fill='red')
    if end is not None:
        img_end = [cell_size * x + cell_size // 2 for x in end]
        canvas.create_oval(img_end[0] - radius,
                           img_end[1] - radius,
                           img_end[0] + radius,
                           img_end[1] + radius, fill='green')

    master.title('Maze')
    master.lift()
    master.call('wm', 'attributes', '.', '-topmost', True)
    tkinter.mainloop()


def main():
    import sys

    sys.setrecursionlimit(4096)

    print("Testing build_maze()...")
    build_maze()

    # checking maze
    maze_ok = True
    n_edges = 0
    for x in range(size_x):
        for y in range(size_y):
            n_node_edges = 0
            for direction in 'NESW':
                n_node_edges += not maze[x][y].has_wall(direction)
            if n_node_edges < 1:
                print('ERROR: walled in cell @ (x=%d, y=%d)' % (x, y))
                maze_ok = False
            n_edges += n_node_edges
    n_perfect_edges = (size_x * size_y - 1) * 2
    if n_edges < n_perfect_edges:
        print('ERROR: not a perfect maze, too many walls')
        maze_ok = False
    if n_edges > n_perfect_edges:
        print('ERROR: not a perfect maze, redundant paths')
        maze_ok = False

    if not maze_ok:
        print("Error in maze building task (fix this first): 0 pts")
        draw_maze()
        return

    print("Testing find_path()...")
    start, end = (0, 0), (size_x - 1, size_y - 1)
    path = find_path(start, end)

    # checking path
    path_ok = True
    try:
        assert len(path) >= 2
        if path[0] != start:
            print('ERROR: invalid starting point for path', path[0])
            path_ok = False
        if path[-1] != end:
            print('ERROR: invalid endpoint for path', path[-1])
            path_ok = False

        prev = None
        for step in path:
            assert 0 <= step[0] < size_x
            assert 0 <= step[1] < size_y
            if prev is not None:
                dst = abs(step[0] - prev[0]) + abs(step[1] - prev[1])
                if dst != 1:
                    print('ERROR: invalid step in path', prev, step)
                    path_ok = False
            prev = step

    except Exception as e:
        print(e)
        print('ERROR: invalid path object:', path)
        path_ok = False
        path = None

    if path_ok:
        print("Maze and path looks good: 100 pts")
    else:
        print("Maze looks good, but incorrect path: 50 pts")

    draw_maze(start, end, path)


if __name__ == '__main__':
    main()
