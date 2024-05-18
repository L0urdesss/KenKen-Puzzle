import pygame
import sys
from button import Button
import os
import time

pygame.init()

# Colors
RED = pygame.Color("#FF7276")
H_RED = pygame.Color("#FFAAAC")
BLUE = pygame.Color("#3E5AAA")
H_BLUE = pygame.Color("#6477AF")
WHITE = pygame.Color("#FFFFFF")

# Screen dimensions
screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))

# Load images
background_image = pygame.image.load("resources/MENU.png")
game_bg_image = pygame.image.load("resources/GAME BG.png")
grid_3x3_image = pygame.image.load("resources/3x3.png")
grid_4x4_image = pygame.image.load("resources/4x4.png")
grid_6x6_image = pygame.image.load("resources/6x6.png")
plus_image = pygame.image.load("resources/+.png")
plus_minus_image = pygame.image.load("resources/+_-.png")
multiply_divide_image = pygame.image.load("resources/x_÷.png")
plus_minus_multiply_image = pygame.image.load("resources/+_-_x_÷.png")
random_image = pygame.image.load("resources/no_option.png")


# Scale the 3x3 image
grid_3x3_image = pygame.transform.scale(grid_3x3_image, (280, 280))  # Adjust the size as per your requirement
grid_4x4_image = pygame.transform.scale(grid_4x4_image, (280, 280))
grid_6x6_image = pygame.transform.scale(grid_6x6_image, (280, 280))
plus_image = pygame.transform.scale(plus_image , (150, 150))
plus_minus_image = pygame.transform.scale(plus_minus_image, (150, 150))
multiply_divide_image = pygame.transform.scale(multiply_divide_image, (150, 150))
plus_minus_multiply_image = pygame.transform.scale(plus_minus_multiply_image, (150, 150))
random_image = pygame.transform.scale(random_image, (150, 150))
pygame.display.set_caption("KenKen Puzzle")

def get_font(size, type):
    if type == 1:
        return pygame.font.SysFont("berlin sans fb demi", size)
    if type == 2:
        return pygame.font.SysFont("Arial Narrow", size)

def main():
    running = True
    while running:
        screen.blit(background_image, (0, 0))
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        PLAY_BUTTON = Button(image=None, pos=(960, 350),
                             text_input="PLAY GAME", font=get_font(68, 1), base_color="#D32735", hovering_color=RED)
        CONTROLS_BUTTON = Button(image=None, pos=(960, 450),
                                 text_input="CONTROLS", font=get_font(68, 1), base_color="#D32735", hovering_color=RED)
        QUIT_BUTTON = Button(image=None, pos=(960, 550),
                             text_input="QUIT GAME", font=get_font(68, 1), base_color="#D32735", hovering_color=RED)

        for button in [PLAY_BUTTON, CONTROLS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    select_grid_size()
                if CONTROLS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    controls()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()
def select_grid_size():
    selecting = True
    while selecting:
        screen.fill(WHITE)
        SELECT_MOUSE_POS = pygame.mouse.get_pos()

        # Load the background image
        background_image = pygame.image.load(os.path.join("resources", "GAME BG.png")).convert_alpha()
        screen.blit(background_image, (0, 0))  # Blit the background image onto the screen

        TEXT = get_font(50, 1).render("SELECT GRID SIZE", True, BLUE)
        TEXT_RECT = TEXT.get_rect(center=(screen_width / 2,220))  # Moved down by 50 pixels
        screen.blit(TEXT, TEXT_RECT)
        # Adjusted positions for the grid buttons with added space
        button_width = 200  # Adjust as needed
        space_between = 150  # Adjust as needed
        start_x = (screen_width - (3 * button_width + 2 * space_between)) / 2 + 100  # Move 100 pixels to the right
        start_y = 420  # Move 50 pixels below
        GRID_3x3_BUTTON = Button(image=grid_3x3_image, pos=(start_x, start_y),
                                 text_input="", font=get_font(68, 1), base_color="#D32735", hovering_color=RED)
        GRID_4x4_BUTTON = Button(image=grid_4x4_image, pos=(start_x + button_width + space_between, start_y),
                                 text_input="", font=get_font(68, 1), base_color="#D32735", hovering_color=RED)
        GRID_6x6_BUTTON = Button(image=grid_6x6_image, pos=(start_x + 2 * (button_width + space_between), start_y),
                                 text_input="", font=get_font(68, 1), base_color="#D32735", hovering_color=RED)
        BACK_BUTTON = Button(image=None, pos=(screen_width / 2, 600),  # Move back button below
                             text_input="BACK", font=get_font(68, 1), base_color=BLUE, hovering_color=H_BLUE)

        for button in [GRID_3x3_BUTTON, GRID_4x4_BUTTON, GRID_6x6_BUTTON, BACK_BUTTON]:
            button.changeColor(SELECT_MOUSE_POS)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if GRID_3x3_BUTTON.checkForInput(SELECT_MOUSE_POS):
                    select_operations(3)
                if GRID_4x4_BUTTON.checkForInput(SELECT_MOUSE_POS):
                    select_operations(4)
                if GRID_6x6_BUTTON.checkForInput(SELECT_MOUSE_POS):
                    select_operations(6)
                if BACK_BUTTON.checkForInput(SELECT_MOUSE_POS):
                    selecting = False

        pygame.display.update()
def select_operations(grid_size):
    selecting = True
    while selecting:
        screen.fill(WHITE)
        SELECT_MOUSE_POS = pygame.mouse.get_pos()
        background_image = pygame.image.load(os.path.join("resources", "GAME BG.png")).convert_alpha()
        screen.blit(background_image, (0, 0))  # Blit the background image onto the screen
        TEXT = get_font(50, 1).render("SELECT OPERATION", True, BLUE)
        TEXT_RECT = TEXT.get_rect(center=(screen_width / 2, 200))
        screen.blit(TEXT, TEXT_RECT)
        button_width = 100  # Adjust as needed
        space_between =100 # Adjust as needed
        start_x = (screen_width - (4 * button_width + 3 * space_between)) / 2 + 150  # Move the buttons to the right
        start_y =330 # Move 50 pixels below for the first row
        # Define buttons
        PLUS_BUTTON = Button(image=plus_image, pos=(start_x, start_y),
                             text_input="", font=get_font(68, 1), base_color="#D32735", hovering_color=RED)
        PLUS_MINUS_BUTTON = Button(image=plus_minus_image, pos=(start_x + button_width + space_between, start_y),
                                   text_input="", font=get_font(68, 1), base_color="#D32735", hovering_color=RED)
        MULTIPLY_DIVIDE_BUTTON = Button(image=multiply_divide_image,
                                        pos=(start_x + 2 * (button_width + space_between), start_y),
                                        text_input="", font=get_font(68, 1), base_color="#D32735", hovering_color=RED)

        # Adjust start_y for the second row
        start_y_second_row = start_y + button_width + space_between

        PLUS_MINUS_MULTIPLY_BUTTON = Button(image=plus_minus_multiply_image,
                                            pos=(start_x + 0.5 * (button_width + space_between), start_y_second_row),
                                            # Move slightly to the right
                                            text_input="", font=get_font(68, 1), base_color="#D32735",
                                            hovering_color=RED)
        RANDOM_BUTTON = Button(image=random_image,
                               pos=(start_x + 1.5 * (button_width + space_between), start_y_second_row),
                               # Move further right
                               text_input="", font=get_font(68, 1), base_color="#D32735", hovering_color=RED)

        BACK_BUTTON = Button(image=None, pos=(screen_width / 2, 650),
                             text_input="BACK", font=get_font(68, 1), base_color=BLUE, hovering_color=H_BLUE)

        for button in [PLUS_BUTTON, PLUS_MINUS_BUTTON, MULTIPLY_DIVIDE_BUTTON, PLUS_MINUS_MULTIPLY_BUTTON,
                       RANDOM_BUTTON, BACK_BUTTON]:
            button.changeColor(SELECT_MOUSE_POS)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLUS_BUTTON.checkForInput(SELECT_MOUSE_POS):
                    select_difficulty(grid_size, "+")
                if PLUS_MINUS_BUTTON.checkForInput(SELECT_MOUSE_POS):
                    select_difficulty(grid_size, "+-")
                if MULTIPLY_DIVIDE_BUTTON.checkForInput(SELECT_MOUSE_POS):
                    select_difficulty(grid_size, "x/")
                if PLUS_MINUS_MULTIPLY_BUTTON.checkForInput(SELECT_MOUSE_POS):
                    select_difficulty(grid_size, "+-x/")
                if RANDOM_BUTTON.checkForInput(SELECT_MOUSE_POS):
                    select_difficulty(grid_size, "?")
                if BACK_BUTTON.checkForInput(SELECT_MOUSE_POS):
                    selecting = False

        pygame.display.update()

def select_difficulty(grid_size, operation):
    selecting = True
    while selecting:
        screen.fill(WHITE)  # Clear the screen
        SELECT_MOUSE_POS = pygame.mouse.get_pos()
        background_image = pygame.image.load(os.path.join("resources", "GAME BG.png")).convert_alpha()
        screen.blit(background_image, (0, 0))  # Blit the background image onto the screen
        TEXT = get_font(50, 1).render("SELECT DIFFICULTY", True, BLUE)
        TEXT_RECT = TEXT.get_rect(center=(screen_width / 2, 220))
        screen.blit(TEXT, TEXT_RECT)

        EASY_BUTTON = Button(image=None, pos=(screen_width / 2, 300),
                             text_input="EASY", font=get_font(68, 1), base_color="#D32735", hovering_color=RED)
        MEDIUM_BUTTON = Button(image=None, pos=(screen_width / 2, 400),
                               text_input="MEDIUM", font=get_font(68, 1), base_color="#D32735", hovering_color=RED)
        HARD_BUTTON = Button(image=None, pos=(screen_width / 2, 500),
                             text_input="HARD", font=get_font(68, 1), base_color="#D32735", hovering_color=RED)
        BACK_BUTTON = Button(image=None, pos=(screen_width / 2, 600),
                             text_input="BACK", font=get_font(68, 1), base_color=BLUE, hovering_color=H_BLUE)

        for button in [EASY_BUTTON, MEDIUM_BUTTON, HARD_BUTTON, BACK_BUTTON]:
            button.changeColor(SELECT_MOUSE_POS)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if EASY_BUTTON.checkForInput(SELECT_MOUSE_POS):
                    start_game(grid_size, operation, "EASY")
                if MEDIUM_BUTTON.checkForInput(SELECT_MOUSE_POS):
                    start_game(grid_size, operation, "MEDIUM")
                if HARD_BUTTON.checkForInput(SELECT_MOUSE_POS):
                    start_game(grid_size, operation, "HARD")
                if BACK_BUTTON.checkForInput(SELECT_MOUSE_POS):
                    selecting = False

        pygame.display.update()


def start_game(grid_size, operation, difficulty):
    # Generate the game board based on the selected grid size
    game_board = generate_board(grid_size)

    # Calculate the size and position of the grid on the screen
    cell_size = 80  # Adjust this value based on your screen size and grid size
    grid_width = cell_size * grid_size
    grid_height = cell_size * grid_size
    grid_x = (screen_width - grid_width) // 2
    grid_y = (screen_height - grid_height) // 2

    # Define number buttons
    button_size = 40
    button_spacing = 10
    num_buttons = []
    for i in range(1, grid_size + 1):
        button_x = grid_x + i * (button_size + button_spacing)
        button_y = grid_y + grid_height + button_spacing
        num_buttons.append(Button(image=None, pos=(button_x, button_y), text_input=str(i),
                                  font=get_font(24, 1), base_color="#D32735", hovering_color=RED))

    # Initialize selected cell
    selected_cell = None

    # Initialize timer variables
    start_time = time.time()
    elapsed_time = 0

    # Placeholder loop to keep the window open
    while True:
        screen.fill((108, 3, 32))  # Fill the screen with black (you can change this color if needed)

        # Render the game board on the screen
        for i in range(grid_size):
            for j in range(grid_size):
                cell_x = grid_x + j * cell_size
                cell_y = grid_y + i * cell_size
                cell_rect = pygame.Rect(cell_x, cell_y, cell_size, cell_size)

                # Render cell background color
                cell_color = (255, 255, 255)  # Default color (white)
                if selected_cell and (j, i) == selected_cell:
                    cell_color = (0, 255, 0)  # Selected color (green)
                pygame.draw.rect(screen, cell_color, cell_rect)

                # Render cell border
                pygame.draw.rect(screen, (0, 0, 0), cell_rect, 2)

                # Render cell value
                cell_value = game_board[i][j]
                if cell_value != 0:
                    font = pygame.font.SysFont(None, 36)
                    text = font.render(str(cell_value), True, (0, 0, 0))  # Text color (black)
                    text_rect = text.get_rect(center=(cell_x + cell_size // 2, cell_y + cell_size // 2))
                    screen.blit(text, text_rect)

        # Render number buttons
        for button in num_buttons:
            button.changeColor(pygame.mouse.get_pos())
            button.update(screen)

        # Calculate elapsed time
        elapsed_time = time.time() - start_time
        minutes = int(elapsed_time // 60)
        seconds = int(elapsed_time % 60)

        # Render timer text
        font = pygame.font.SysFont(None, 36)
        timer_text = font.render(f" {minutes:02}:{seconds:02}", True, (255, 255, 255))
        screen.blit(timer_text, (10, 10))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                # Check if the click is within the grid boundaries
                if grid_x <= mouse_x < grid_x + grid_width and grid_y <= mouse_y < grid_y + grid_height:
                    # Calculate the cell index based on the mouse position
                    cell_x = (mouse_x - grid_x) // cell_size
                    cell_y = (mouse_y - grid_y) // cell_size
                    selected_cell = (cell_x, cell_y)
                else:
                    # Check if any number button is clicked
                    for i, button in enumerate(num_buttons):
                        if button.checkForInput((mouse_x, mouse_y)):
                            if selected_cell:
                                # Update the value of the selected cell with the clicked number
                                game_board[selected_cell[1]][selected_cell[0]] = i + 1
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DELETE or event.key == pygame.K_BACKSPACE:
                    if selected_cell:
                        # Clear the value of the selected cell
                        game_board[selected_cell[1]][selected_cell[0]] = 0


def generate_board(grid_size):
    # Generate a grid_size x grid_size game board
    board = [[0] * grid_size for _ in range(grid_size)]
    # You can customize the board generation logic here

    return board


def controls():
    controls_bg = pygame.image.load("resources/CONTROLS.png")
    screen.blit(controls_bg, (0, 0))

    while True:
        CONTROLS_MOUSE = pygame.mouse.get_pos()
        BACK_BUTTON = Button(image=None, pos=(1160, 650),
                             text_input="BACK", font=get_font(50, 1), base_color="#D32735", hovering_color=RED)

        for button in [BACK_BUTTON]:
            button.changeColor(CONTROLS_MOUSE)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if BACK_BUTTON.checkForInput(CONTROLS_MOUSE):
                    main()

        pygame.display.flip()

main()
