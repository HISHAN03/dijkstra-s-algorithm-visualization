# grid.py

from OpenGL.GL import *
from colors import *

class Grid:
    def __init__(self, size):
        self.size = size
        self.grid = [[0 for _ in range(size[1])] for _ in range(size[0])]
        self.start_point = None
        self.goal_point = None
        self.path = []
        self.visited = []

        # Define fixed obstacles (example)
        self.obstacles = [
            (2, 2), (2, 3), (2, 4), (2, 5), (2, 6),
            (3, 6), (4, 6), (5, 6),
            (6, 2), (6, 3), (6, 4), (6, 5), (6, 6),
            
        ]
        self.set_obstacles()

    def set_obstacles(self):
        for (x, y) in self.obstacles:
            self.grid[x][y] = 1

    def draw(self):
        for x in range(self.size[0]):
            for y in range(self.size[1]):
                if (x, y) == self.start_point:
                    glColor3f(*START_COLOR)
                elif (x, y) == self.goal_point:
                    glColor3f(*GOAL_COLOR)
                elif (x, y) in self.path:
                    glColor3f(*PATH_COLOR)
                elif (x, y) in self.visited:
                    glColor3f(*VISITED_COLOR)
                elif self.grid[x][y] == 1:  # Obstacle
                    glColor3f(*OBSTACLE_COLOR)
                else:
                    glColor3f(*DEFAULT_COLOR)
                self.draw_square((x, y))

        glColor3f(*LINE_COLOR)
        glBegin(GL_LINES)
        for x in range(self.size[0] + 1):
            glVertex2f(x, 0)
            glVertex2f(x, self.size[1])
        for y in range(self.size[1] + 1):
            glVertex2f(0, y)
            glVertex2f(self.size[0], y)
        glEnd()

    def draw_square(self, point):
        x, y = point
        glBegin(GL_QUADS)
        glVertex2f(x, y)
        glVertex2f(x + 1, y)
        glVertex2f(x + 1, y + 1)
        glVertex2f(x, y + 1)
        glEnd()

    def is_obstacle(self, point):
        x, y = point
        return self.grid[x][y] == 1

    def neighbors(self, point):
        x, y = point
        neighbor_points = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
        valid_neighbors = [
            (nx, ny) for nx, ny in neighbor_points
            if 0 <= nx < self.size[0] and 0 <= ny < self.size[1] and not self.is_obstacle((nx, ny))
        ]
        return valid_neighbors
