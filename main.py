import sys
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from grid import Grid
from dijkstra import Dijkstra

# Initialize global variables
grid_size = (20, 20)  # Adjusted grid size for medium-sized boxes
grid = Grid(grid_size)
dijkstra = None

def init():
    glClearColor(1.0, 1.0, 1.0, 1.0)
    glMatrixMode(GL_PROJECTION)
    gluOrtho2D(0, grid_size[0], 0, grid_size[1])

def display():
    glClear(GL_COLOR_BUFFER_BIT)
    grid.draw()
    glutSwapBuffers()

def mouse(button, state, x, y):
    global dijkstra
    if state == GLUT_DOWN:
        grid_x = x // (500 // grid_size[0])
        grid_y = (500 - y) // (500 // grid_size[1])
        if not grid.start_point:
            grid.start_point = (grid_x, grid_y)
        elif not grid.goal_point:
            grid.goal_point = (grid_x, grid_y)
            grid.path = []
            grid.visited = []
            dijkstra = Dijkstra(grid)
            dijkstra.init(grid.start_point)
            glutTimerFunc(100, step_dijkstra, 0)
        glutPostRedisplay()

def step_dijkstra(value):
    if dijkstra:
        done = dijkstra.step()
        glutPostRedisplay()
        if not done:
            glutTimerFunc(100, step_dijkstra, 0)

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
