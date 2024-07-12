# grid_level_2.py

from OpenGL.GL import *
from colors import *
from grid import Grid

class GridLevel2(Grid):
    def __init__(self, size):
        super().__init__(size)
        self.add_obstacles()

    def add_obstacles(self):
        # Add more obstacles compared to Level 1
        self.grid[1][1] = 1  # Example obstacle
        self.grid[2][3] = 1  # Example obstacle
        self.grid[4][5] = 1  # Example obstacle
        self.grid[6][2] = 1  # Example obstacle
        self.grid[7][4] = 1  # Example obstacle
        # Add more obstacles as needed for Level 2
