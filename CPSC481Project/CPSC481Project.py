import sys, pygame as pg
from collections import deque

from utils import *
import random

# https://github.com/aimacode/aima-python/blob/master/search.py#L15
# so far this is just a working sudoku puzzle generator
# the github page has a lot of classes and functions for implementing the search algorithms
# I'll mainly be focusing on the depth first graph search algorithm
# once we have a working algorithm, I'll add another button to run the search


# Everything below this line is additional tech stack just to develop a UI to show off the DFS search algorithm
# This is not part of the actual project, but is just a way to show off the algorithm.

pg.init()
screen_size = 1000, 750
screen = pg.display.set_mode(screen_size)
font = pg.font.SysFont(None, 80)

number_grid = [["" for _ in range(9)] for _ in range(9)]

def generate_sudoku(difficulty):
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

    # Initialize the grid with empty strings
    number_grid = [["" for _ in range(9)] for _ in range(9)]

    # List of numbers from 1 to 9
    numbers = [str(i) for i in range(1, 10)]

    # Fill the grid with a complete Sudoku solution
    fill_grid()

    # Remove numbers based on difficulty
    erase_count = {"easy": (5, 10), "medium": (11, 20), "hard": (21, 40)}
    if difficulty not in erase_count:
        raise ValueError("Invalid difficulty level")

    min_erase_count, max_erase_count = erase_count[difficulty]
    erase_count = random.randint(min_erase_count, max_erase_count)

    for _ in range(erase_count):
        while True:
            row = random.randint(0, 8)
            col = random.randint(0, 8)
            if number_grid[row][col] != "":
                number_grid[row][col] = ""
                break

    return number_grid
            

# Function to draw the main menu
def draw_menu():
    screen.fill(pg.Color("white"))
    title_text = font.render("Sudoku Game", True, pg.Color("black"))
    easy_text = font.render("Easy", True, pg.Color("black"))
    medium_text = font.render("Medium", True, pg.Color("black"))
    hard_text = font.render("Hard", True, pg.Color("black"))
    
    title_rect = title_text.get_rect(center=(screen.get_width()//2, 200))
    easy_rect = easy_text.get_rect(center=(screen.get_width()//2, 350))
    medium_rect = medium_text.get_rect(center=(screen.get_width()//2, 450))
    hard_rect = hard_text.get_rect(center=(screen.get_width()//2, 550))
    
    screen.blit(title_text, title_rect)
    screen.blit(easy_text, easy_rect)
    screen.blit(medium_text, medium_rect)
    screen.blit(hard_text, hard_rect)
    
    pg.display.flip()
    
    return easy_rect, medium_rect, hard_rect

# Function to handle events in the main menu
def menu_loop():
    easy_rect, medium_rect, hard_rect = draw_menu()
    selected_difficulty = None
    
    while selected_difficulty is None:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                mouse_pos = pg.mouse.get_pos()
                if easy_rect.collidepoint(mouse_pos):
                    selected_difficulty = "easy"
                elif medium_rect.collidepoint(mouse_pos):
                    selected_difficulty = "medium"
                elif hard_rect.collidepoint(mouse_pos):
                    selected_difficulty = "hard"
        
        pg.time.Clock().tick(30)
    
    global number_grid  # Declare number_grid as global
    number_grid = generate_sudoku(selected_difficulty)  # Assign the result of generate_sudoku to the global number_grid

    
    
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
            #print(str(output))
            n_text = font.render(str(output), True, pg.Color("black"))
            screen.blit(n_text, pg.Vector2((col * 80) + offset + 5, (row * 80) + offset - 2))
            col += 1
        row += 1

def game_loop():
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        elif event.type == pg.MOUSEBUTTONDOWN:
            mouse_pos = pg.mouse.get_pos()
            # Define the bounding box of the button
            x_center, y_center = 850, 675  # Center of the button
            button_width, button_height = 132, 50  # Example width and height of the button

            # Calculate the top-left corner and bottom-right corner coordinates
            x1 = x_center - button_width // 2
            y1 = y_center - button_height // 2
            x2 = x_center + button_width // 2
            y2 = y_center + button_height // 2

            # Check if the mouse click is within the bounding box of the button
            if x1 <= mouse_pos[0] <= x2 and y1 <= mouse_pos[1] <= y2:
                return "menu"  # Return to menu if the "Back to Menu" button is clicked

    draw_background()
    draw_numbers()

    # Draw "Back to Menu" button
    back_text = font.render("Menu", True, pg.Color("black"))
    back_rect = back_text.get_rect(center=(850, 675))
    pg.draw.rect(screen, pg.Color("white"), back_rect)
    screen.blit(back_text, back_rect)

    pg.display.flip()

    return "game"  # Return "game" to indicate that the game loop should continue

draw_menu()
menu_loop()

while True:
    result = game_loop()
    if result == "menu":
        draw_menu()
        menu_loop()



