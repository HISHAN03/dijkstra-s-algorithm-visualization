import sys
import pygame
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from grid.Grid1 import Grid1 as Grid1
from grid.Grid2 import Grid2 as Grid2
from grid.DefaultGrid import DefaultGrid as DefaultGrid
from dijkstra import Dijkstra

# Global variables
window_width = 600
window_height = 600
grid_size = (20, 20)
grid = None
algorithm_started = False
dijkstra_algorithm = None
current_screen = "menu"

# Pygame initialization
pygame.init()
screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Dijkstra's Algorithm Visualization - Menu")
font = pygame.font.SysFont('Arial', 24)
clock = pygame.time.Clock()

flicker_colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
current_flicker_color_index = 0

def display_menu():
    global current_flicker_color_index

    screen.fill((255, 255, 255))

    title_surface = font.render("Dijkstra's Algorithm Visualization", True, (0, 0, 0))
    screen.blit(title_surface, (window_width // 2 - title_surface.get_width() // 2, window_height // 2 - 50))

    flicker_surface = font.render("Press any key to continue", True, flicker_colors[current_flicker_color_index])
    screen.blit(flicker_surface, (window_width // 2 - flicker_surface.get_width() // 2, window_height // 2))

    pygame.display.flip()

def update_flicker_color():
    global current_flicker_color_index
    current_flicker_color_index = (current_flicker_color_index + 1) % len(flicker_colors)

def display_level_selection():
    screen.fill((255, 255, 255))

    title_surface = font.render("Select a Grid Level:", True, (0, 0, 0))
    screen.blit(title_surface, (window_width // 2 - title_surface.get_width() // 2, window_height // 2 - 50))

    options_surface = font.render("1: Grid1, 2: Grid2, 3: Default Grid", True, (0, 0, 0))
    
    screen.blit(options_surface, (window_width // 2 - options_surface.get_width() // 2, window_height // 2))

    pygame.display.flip()

def run_menu():
    global current_screen

    while current_screen == "menu":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                current_screen = "level_selection"

        display_menu()
        update_flicker_color()
        clock.tick(1)

def run_level_selector():
    global current_screen, grid

    while current_screen == "level_selection":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    grid = Grid1(grid_size)
                    current_screen = "game"
                elif event.key == pygame.K_2:
                    grid = Grid2(grid_size)
                    current_screen = "game"
                elif event.key == pygame.K_3:
                    grid = DefaultGrid(grid_size)
                    current_screen = "game"

        display_level_selection()
        clock.tick(30)

# OpenGL initialization
def init_opengl():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(window_width, window_height)
    glutCreateWindow(b"Dijkstra's Algorithm Visualization - Interactive")
    glutDisplayFunc(display)
    glutMouseFunc(mouse)
    glutKeyboardFunc(keyboard)
    glClearColor(1.0, 1.0, 1.0, 1.0)
    gluOrtho2D(0, grid_size[0], 0, grid_size[1])

def display():
    global current_screen

    if current_screen == "game":
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
    global algorithm_started, dijkstra_algorithm

    if key == b'\x1b':  # Escape key
        sys.exit()
    if key == b'\r' and grid.start_point and grid.goal_point:  # Enter key to start the algorithm
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
    run_menu()
    run_level_selector()
    pygame.quit()

    # Initialize and run OpenGL part
    init_opengl()
    glutMainLoop()

if __name__ == "__main__":
    main()
