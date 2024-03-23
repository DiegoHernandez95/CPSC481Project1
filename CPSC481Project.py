import sys, pygame as pg
from collections import deque

from utils import *
import random

# https://github.com/aimacode/aima-python/blob/master/search.py#L15
# now accurately shows which numbers are solved

#create problem class
class Problem:
    def __init__(self, initial, goal=None):
        self.initial = initial
        self.goal = goal

    def actions(self, state):
        row, col = find_empty_cell(state)
        if row is None:
            return []
        valid_actions = []
        for num in range(1, 10):
            if is_valid_move(state, row, col, str(num)):
                valid_actions.append((row, col, str(num)))
        return valid_actions

    # return the new state after the action is taken
    def result(self, state, action):
        row, col, num = action
        new_state = [row[:] for row in state]
        new_state[row][col] = num
        return new_state

    # if empty string is found then return false (aka goal not met)
    def goal_test(self, state):
        for row in state:
            if "" in row:
                return False
        return True

    def path_cost(self, c, state1, action, state2):
        return c + 1

class Node:
    def __init__(self, state, parent=None, action=None, path_cost=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
        self.depth = parent.depth + 1 if parent else 0

    def __repr__(self):
        return "<Node {}".format(self.state)

    def expand(self, problem):
        return [self.child_node(problem, action) for action in problem.actions(self.state)]

    def child_node(self, problem, action):
        next_state = problem.result(self.state, action)
        next_node = Node(next_state, self, action, problem.path_cost(self.path_cost, self.state, action, next_state))
        return next_node

    def solution(self):
        return [node.action for node in self.path()[1:]]

    def path(self):
        node, path_back = self, []
        while node:
            path_back.append(node)
            node = node.parent
        return list(reversed(path_back))

# checks to see if the number is in the 
# same row and column and the rows and columns
# of the other grids
def is_valid_move(grid, row, col, num):
    # Check row
    if num in grid[row]:
        return False

    # Check column
    for i in range(9):
        if grid[i][col] == num:
            return False

    # Check subgrid
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if grid[start_row + i][start_col + j] == num:
                return False

    return True

# this function will return row and column of an empty cell
def find_empty_cell(grid):
    for row in range(9):
        for col in range(9):
            if grid[row][col] == "":
                return row, col
    return None

# establish fronter and explored set
# while there are still nodes in the frontier
# pop the first node, check if it is the goal, then add it to the explored set
# then add the children to the frontier
def depth_first_graph_search(problem):
    frontier = [Node(problem.initial)]

    explored = set()
    while frontier:
        node = frontier.pop()
        if problem.goal_test(node.state):
            return node
        explored.add(tuple(map(tuple, node.state))) 
        frontier.extend(child for child in node.expand(problem) if tuple(map(tuple, child.state)) not in explored and child not in frontier)
    return None

# this function will create a problem space
# then use the dfs function to solve the puzzle
# and then return the solution
def sudoku_solver(initial_state):
    problem = Problem(initial_state)
    solution_node = depth_first_graph_search(problem)
    if solution_node:
        solution = solution_node.state
        return solution  # Return the solution
    else:
        return None  # Return None if no solution exists



# Everything below this line is additional tech stack just to develop a UI to show off the DFS search algorithm
# This is not part of the actual project, but is just a way to show off the algorithm.

pg.init()
screen_size = 1020, 750
screen = pg.display.set_mode(screen_size)
font = pg.font.SysFont(None, 80)

def generate_sudoku():
    global number_grid
    global erased_grid

    # Reset the number grid to an empty grid
    number_grid = [["" for _ in range(9)] for _ in range(9)]

    # Helper function to check if a number is valid in a given position
    def is_valid_position(num, row, col):
        for i in range(9):
            if number_grid[row][i] == num or number_grid[i][col] == num or number_grid[(row // 3) * 3 + i // 3][(col // 3) * 3 + i % 3] == num:
                return False
        return True

    # Helper function to fill the grid recursively
    def fill_grid():
        for i in range(81):
            row = i // 9
            col = i % 9
            if number_grid[row][col] == "":
                random.shuffle(numbers)
                for num in numbers:
                    if is_valid_position(num, row, col):
                        number_grid[row][col] = num
                        if fill_grid():
                            return True
                        number_grid[row][col] = ""
                return False
        return True

    numbers = [str(i) for i in range(1, 10)]

    # Fill the grid with a complete Sudoku solution
    fill_grid()

    # Decided that having difficulty scaling was irrelvant for showing off the algorithm
    # Changed it so that it just randomly erases a certain number of cells
    erase_count = random.randint(10, 50)
    erased_grid = [[False for _ in range(9)] for _ in range(9)]

    for _ in range(erase_count):
        while True:
            row = random.randint(0, 8)
            col = random.randint(0, 8)
            if number_grid[row][col] != "":
                number_grid[row][col] = ""
                erased_grid[row][col] = True
                break

    print("New Sudoku puzzle generated:")

    return number_grid

def draw_menu():
    screen.fill(pg.Color("white"))
    title_text = font.render("DFS Sudoku Solver", True, pg.Color("black"))
    title_rect = title_text.get_rect(center=(screen.get_width()//2, 200))
    play_text = font.render("Play", True, pg.Color("black"))
    play_rect = play_text.get_rect(center=(screen.get_width()//2, 400))
    screen.blit(title_text, title_rect)
    screen.blit(play_text, play_rect)
    pg.display.flip()
    return play_rect

def menu_loop():
    play_rect = draw_menu()
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                if play_rect.collidepoint(event.pos):
                    generate_sudoku()
                    return "game"
    
def draw_background():
    screen.fill(pg.Color("white"))
    pg.draw.rect(screen, pg.Color("black"), pg.Rect(15, 15, 720, 720), 10)
    i = 1
    while (i * 80) < 720:
        line_width = 5 if i % 3 > 0 else 10
        pg.draw.line(screen, pg.Color("black"), pg.Vector2((i * 80) + 15, 15), pg.Vector2((i * 80) + 15, 735), line_width)
        pg.draw.line(screen, pg.Color("black"), pg.Vector2(15, (i * 80) + 15), pg.Vector2(735, (i * 80) + 15), line_width)
        i += 1
        
def draw_numbers():
    row = 0
    offset = 35
    while row < 9:
        col = 0
        while col < 9:
            output = number_grid[row][col]
            if output != "":  # Check if the cell is not empty
                # Check if the cell was erased
                if erased_grid[row][col]:
                    n_color = pg.Color("green")  # Render erased cells in green

                    # Render the outline
                    outline = font.render(str(output), True, pg.Color("navy"))
                    for x in range(-2, 3):
                        for y in range(-2, 3):
                            screen.blit(outline, pg.Vector2((col * 80) + offset + 5 + x, (row * 80) + offset - 2 + y))
                else:
                    n_color = pg.Color("black")  # Render other cells in black

                # Render the main text
                n_text = font.render(str(output), True, n_color)
                screen.blit(n_text, pg.Vector2((col * 80) + offset + 5, (row * 80) + offset - 2))
            col += 1
        row += 1

# Function to draw the game screen
def game_loop():
    global number_grid

    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        elif event.type == pg.MOUSEBUTTONDOWN:
            mouse_pos = pg.mouse.get_pos()
            generate_button_rect = pg.Rect(750, 600, 250, 55)
            solve_button_rect = pg.Rect(775, 400, 200, 50)
            if generate_button_rect.collidepoint(mouse_pos):
                generate_sudoku()  # Generate a new Sudoku puzzle
            elif solve_button_rect.collidepoint(mouse_pos):
                solution = sudoku_solver(number_grid)
                if solution:
                    number_grid = solution

    # Drawing Sudoku grid and numbers
    draw_background()
    draw_numbers()

    # Draw buttons
    generate_button_text = font.render("Generate", True, pg.Color("black"))
    solve_button_text = font.render("Solve", True, pg.Color("black"))
    generate_button_rect = generate_button_text.get_rect(center=(875, 625))
    solve_button_rect = solve_button_text.get_rect(center=(875, 425))
    pg.draw.rect(screen, pg.Color("white"), generate_button_rect)
    pg.draw.rect(screen, pg.Color("white"), solve_button_rect)
    screen.blit(generate_button_text, generate_button_rect)
    screen.blit(solve_button_text, solve_button_rect)

    pg.display.flip()

    return "game"

# Main game loop
draw_menu()
menu_loop()

while True:
    result = game_loop()
    if result == "menu":
        draw_menu()
        menu_loop()


