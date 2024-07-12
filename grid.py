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
                else:
                    glColor3f(*DEFAULT_COLOR)
                self.draw_square((x, y))

        glColor3f(*LINE_COLOR)
        for x in range(self.size[0]):
            for y in range(self.size[1]):
                glBegin(GL_LINE_LOOP)
                glVertex2f(x, y)
                glVertex2f(x + 1, y)
                glVertex2f(x + 1, y + 1)
                glVertex2f(x, y + 1)
                glEnd()

    def draw_square(self, point):
        x, y = point
        glBegin(GL_QUADS)
        glVertex2f(x, y)
        glVertex2f(x + 1, y)
        glVertex2f(x + 1, y + 1)
        glVertex2f(x, y + 1)
        glEnd()
