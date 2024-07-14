from OpenGL.GL import *
from colors import *

class Grid1:
    def __init__(self, size):
        self.size = size
        self.grid = [[0 for _ in range(size[1])] for _ in range(size[0])]
        self.start_point = None
        self.goal_point = None
        self.path = []
        self.visited = []
        self.obstacles =[
          (2, 8), (3, 8), (4, 8), (5, 8), (6, 8), (7, 8),
            (2, 7), (7, 7),
            (2, 6), (7, 6),
            (2, 5), (7, 5),
            (2, 4), (7, 4),
          
            (2, 2), (3, 2), (4, 2), (5, 2), (6, 2), (7, 2),

            # Square cut in the middle
            (12, 8), (13, 8), (14, 8), (15, 8),
            (12, 7), (15, 7),
            
            (12, 5), (15, 5),
            (12, 4), (13, 4), (14, 4), (15, 4),
            
            
            (7, 18), (8, 18), (9, 18),
            (6, 17),  
            (5, 16),  (11, 16),
            (12, 15),
            (3, 14), (4, 14), (5, 14), (6, 14), (7, 14), (8, 14), (9, 14), (10, 14), (11, 14), (12, 14), (13, 14)

           
       ]
    
       

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
        

