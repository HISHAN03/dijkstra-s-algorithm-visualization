# grid_level_1.py

from OpenGL.GL import *
from colors import *
from grid import Grid

class GridLevel1(Grid):
    def __init__(self, size):
        super().__init__(size)
        self.add_obstacles()

    def add_obstacles(self):
        # Add obstacles to the grid (customize this based on your level design)
        self.grid[2][2] = 1  # Example obstacle
        self.grid[3][4] = 1  # Example obstacle
        self.grid[5][3] = 1  # Example obstacle
        # Add more obstacles as needed for Level 1
