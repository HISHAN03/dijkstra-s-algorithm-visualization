import sys
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from grid.Grid1 import Grid1 as Grid1
from grid.Grid2 import Grid2 as Grid2
from grid.DefaultGrid  import DefaultGrid as DefaultGrid
from dijkstra import Dijkstra

# Global variables
window_width = 600
window_height = 600
grid_size = (20, 20)
grid = None
algorithm_started = False
dijkstra_algorithm = None
current_screen = "menu"

def init():
    glClearColor(1.0, 1.0, 1.0, 1.0)
    gluOrtho2D(0, grid_size[0], 0, grid_size[1])

def display_menu():
    glClear(GL_COLOR_BUFFER_BIT)
    glColor3f(0.0, 0.0, 0.0)
    glRasterPos2f(grid_size[0] // 2 - 5, grid_size[1] // 2)
    for ch in "Welcome to Dijkstra's Algorithm Visualization":
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ctypes.c_int(ord(ch)))
    glRasterPos2f(grid_size[0] // 2 - 5, grid_size[1] // 2 - 2)
    for ch in "Press any key to continue":
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ctypes.c_int(ord(ch)))
    glutSwapBuffers()

def display_level_selection():
    glClear(GL_COLOR_BUFFER_BIT)
    glColor3f(0.0, 0.0, 0.0)
    glRasterPos2f(grid_size[0] // 2 - 5, grid_size[1] // 2)
    for ch in "Select a Grid Level:":
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ctypes.c_int(ord(ch)))
    glRasterPos2f(grid_size[0] // 2 - 5, grid_size[1] // 2 - 2)
    for ch in "1: Grid1, 2: Grid2, 3: Default Grid":
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ctypes.c_int(ord(ch)))
    glutSwapBuffers()

def display():
    global current_screen
    if current_screen == "menu":
        display_menu()
    elif current_screen == "level_selection":
        display_level_selection()
    else:
        glClear(GL_COLOR_BUFFER_BIT)
        grid.draw()
        glutSwapBuffers()

def mouse(button, state, x, y):
    global algorithm_started
    if state == GLUT_DOWN and not algorithm_started and current_screen == "game":
        grid_x = x * grid_size[0] // window_width
        grid_y = (window_height - y) * grid_size[1] // window_height
        if grid.start_point is None:
            grid.start_point = (grid_x, grid_y)
        elif grid.goal_point is None:
            grid.goal_point = (grid_x, grid_y)
        else:
            grid.set_obstacle(grid_x, grid_y)
        glutPostRedisplay()

def keyboard(key, x, y):
    global current_screen, grid, algorithm_started, dijkstra_algorithm
    if key == b'\x1b':  # Escape key
        sys.exit()
    if current_screen == "menu":
        current_screen = "level_selection"
    elif current_screen == "level_selection":
        if key == b'1':
            grid = Grid1(grid_size)
            current_screen = "game"
        elif key == b'2':
            grid = Grid2(grid_size)
            current_screen = "game"
        elif key == b'3':
            grid = DefaultGrid(grid_size)
            current_screen = "game"
    elif current_screen == "game" and key == b'\r' and grid.start_point and grid.goal_point:  # Enter key to start the algorithm
        algorithm_started = True
        dijkstra_algorithm = Dijkstra(grid)
        dijkstra_algorithm.init(grid.start_point)
        step_dijkstra(0)
    glutPostRedisplay()

def step_dijkstra(value):
    if dijkstra_algorithm:
        done = dijkstra_algorithm.step()
        glutPostRedisplay()
        if not done:
            glutTimerFunc(100, step_dijkstra, 0)

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(window_width, window_height)
    glutCreateWindow(b"Dijkstra's Algorithm Visualization - Interactive")
    glutDisplayFunc(display)
    glutMouseFunc(mouse)
    glutKeyboardFunc(keyboard)
    init()
    glutMainLoop()

if __name__ == "__main__":
    main()
