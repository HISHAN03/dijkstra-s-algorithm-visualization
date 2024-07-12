import sys
import numpy as np
import heapq
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

# Initialize global variables
grid_size = (10, 10)
start_point = None
goal_point = None
grid = np.zeros(grid_size)
path = []
visited = []
priority_queue = []
came_from = {}
distances = {}

# Colors
START_COLOR = (0.0, 1.0, 0.0)
GOAL_COLOR = (1.0, 0.0, 0.0)
VISITED_COLOR = (0.6, 0.6, 0.6)
PATH_COLOR = (0.0, 0.0, 1.0)
DEFAULT_COLOR = (1.0, 1.0, 1.0)
LINE_COLOR = (0.0, 0.0, 0.0)

def init():
    glClearColor(1.0, 1.0, 1.0, 1.0)
    glMatrixMode(GL_PROJECTION)
    gluOrtho2D(0, grid_size[0], 0, grid_size[1])

def draw_grid():
    for x in range(grid_size[0]):
        for y in range(grid_size[1]):
            if (x, y) == start_point:
                glColor3f(*START_COLOR)
            elif (x, y) == goal_point:
                glColor3f(*GOAL_COLOR)
            elif (x, y) in path:
                glColor3f(*PATH_COLOR)
            elif (x, y) in visited:
                glColor3f(*VISITED_COLOR)
            else:
                glColor3f(*DEFAULT_COLOR)
            draw_square((x, y))

    glColor3f(*LINE_COLOR)
    for x in range(grid_size[0]):
        for y in range(grid_size[1]):
            glBegin(GL_LINE_LOOP)
            glVertex2f(x, y)
            glVertex2f(x + 1, y)
            glVertex2f(x + 1, y + 1)
            glVertex2f(x, y + 1)
            glEnd()

def draw_square(point):
    x, y = point
    glBegin(GL_QUADS)
    glVertex2f(x, y)
    glVertex2f(x + 1, y)
    glVertex2f(x + 1, y + 1)
    glVertex2f(x, y + 1)
    glEnd()

def display():
    glClear(GL_COLOR_BUFFER_BIT)
    draw_grid()
    glutSwapBuffers()

def mouse(button, state, x, y):
    global start_point, goal_point, path, visited
    if state == GLUT_DOWN:
        grid_x = x // (500 // grid_size[0])
        grid_y = (500 - y) // (500 // grid_size[1])
        if not start_point:
            start_point = (grid_x, grid_y)
        elif not goal_point:
            goal_point = (grid_x, grid_y)
            path = []
            visited = []
            init_dijkstra()
        glutPostRedisplay()

def init_dijkstra():
    global priority_queue, came_from, current_distance, current_node, distances
    distances = { (i, j): float('inf') for i in range(grid_size[0]) for j in range(grid_size[1]) }
    distances[start_point] = 0
    priority_queue = [(0, start_point)]
    came_from = {}
    current_distance = 0
    current_node = None
    glutTimerFunc(100, step_dijkstra, 0)

def step_dijkstra(value):
    global priority_queue, visited, path, current_distance, current_node, distances
    if priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)
        if current_node in visited:
            glutTimerFunc(100, step_dijkstra, 0)
            return
        visited.append(current_node)
        if current_node == goal_point:
            path = reconstruct_path(came_from, start_point, goal_point)
            glutPostRedisplay()
            return
        neighbors = get_neighbors(current_node, grid_size[0], grid_size[1])
        for neighbor in neighbors:
            distance = current_distance + 1
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(priority_queue, (distance, neighbor))
                came_from[neighbor] = current_node
        glutPostRedisplay()
        glutTimerFunc(100, step_dijkstra, 0)
    else:
        path = reconstruct_path(came_from, start_point, goal_point)
        glutPostRedisplay()

def get_neighbors(node, rows, cols):
    x, y = node
    neighbors = []
    if x > 0: neighbors.append((x - 1, y))
    if x < rows - 1: neighbors.append((x + 1, y))
    if y > 0: neighbors.append((x, y - 1))
    if y < cols - 1: neighbors.append((x, y + 1))
    return neighbors

def reconstruct_path(came_from, start, goal):
    current = goal
    path = []
    while current != start:
        if current not in came_from:
            return []  # No path found
        path.append(current)
        current = came_from[current]
    path.append(start)
    path.reverse()
    return path

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(500, 500)
    glutInitWindowPosition(100, 100)
    glutCreateWindow(b"Dijkstra's Algorithm Visualization")
    init()
    glutDisplayFunc(display)
    glutMouseFunc(mouse)
    glutMainLoop()

if __name__ == "__main__":
    main()
