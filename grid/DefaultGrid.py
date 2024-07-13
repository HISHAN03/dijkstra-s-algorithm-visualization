from OpenGL.GL import *
from colors import *

class DefaultGrid:
    def __init__(self, size):
        self.size = size
        self.grid = [[0 for _ in range(size[1])] for _ in range(size[0])]
        self.start_point = None
        self.goal_point = None
        self.path = []
        self.visited = []

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

    def set_obstacle(self, x, y):
        self.grid[x][y] = 1
