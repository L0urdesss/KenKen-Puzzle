import pygame
import sys
from button import Button
import os

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
        screen.fill(WHITE)
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
    screen.blit(game_bg_image, (0, 0))
    pygame.display.update()

    # Placeholder loop to keep the window open
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

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
