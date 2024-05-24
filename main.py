import os
import sys
import time

import pygame
from moviepy.editor import VideoFileClip
from backend import KenPuzzleMaker

from button import Button

pygame.init()

# Colors
RED = pygame.Color("#FF7276")
H_RED = pygame.Color("#FFAAAC")
BLUE = pygame.Color("#3E5AAA")
H_BLUE = pygame.Color("#6477AF")
WHITE = pygame.Color("#FFFFFF")
BLACK = pygame.Color("#000000")

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
new_game_img = pygame.image.load('resources/new game.png')
solve_img = pygame.image.load('resources/solve.png')
undo_img = pygame.image.load('resources/undo.png')
reset_img = pygame.image.load('resources/reset.png')
erase_img = pygame.image.load('resources/eraser.png')


# Scale the 3x3 image
grid_3x3_image = pygame.transform.scale(grid_3x3_image, (280, 280))  # Adjust the size as per your requirement
grid_4x4_image = pygame.transform.scale(grid_4x4_image, (280, 280))
grid_6x6_image = pygame.transform.scale(grid_6x6_image, (280, 280))
plus_image = pygame.transform.scale(plus_image, (150, 150))
plus_minus_image = pygame.transform.scale(plus_minus_image, (150, 150))
multiply_divide_image = pygame.transform.scale(multiply_divide_image, (150, 150))
plus_minus_multiply_image = pygame.transform.scale(plus_minus_multiply_image, (150, 150))
random_image = pygame.transform.scale(random_image, (150, 150))
new_game_img = pygame.transform.scale(new_game_img, (180, 90))
solve_img = pygame.transform.scale(solve_img, (180, 90))
undo_img = pygame.transform.scale(undo_img, (90, 90))
reset_img = pygame.transform.scale(reset_img, (90, 90))
erase_img = pygame.transform.scale(erase_img, (90, 90))
pygame.display.set_caption("KenKen Puzzle")


def play_intro_video():
    clip = VideoFileClip("resources/Intro.mp4")
    clip_resized = clip.resize(height=screen_height)  # Resize video to fit the screen height
    clip_width, clip_height = clip_resized.size

    start_x = (screen_width - clip_width) // 2
    start_y = (screen_height - clip_height) // 2

    # Extract and play audio
    audio = clip.audio
    audio_path = "resources/temp_audio.mp3"
    audio.write_audiofile(audio_path)
    pygame.mixer.music.load(audio_path)
    pygame.mixer.music.play()

    clock = pygame.time.Clock()
    for frame in clip_resized.iter_frames(fps=24, dtype="uint8"):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()  # Stop the music if the user quits
                pygame.quit()
                sys.exit()

        frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
        screen.fill((0, 0, 0))  # Clear the screen
        screen.blit(frame_surface, (start_x, start_y))  # Blit the frame surface on screen
        pygame.display.update()
        clock.tick(24)  # Control the frame rate

    pygame.mixer.music.stop()
    pygame.mixer.quit()  # Ensure mixer is properly closed
    clip.close()
    os.remove(audio_path)  # Clean up the temporary audio file

    clip.close()
def get_font(size, type):
    if type == 1:
        return pygame.font.SysFont("berlin sans fb demi", size)
    if type == 2:
        return pygame.font.SysFont("Arial Narrow", size)




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
                    select_difficulty(grid_size, "*/")
                if PLUS_MINUS_MULTIPLY_BUTTON.checkForInput(SELECT_MOUSE_POS):
                    select_difficulty(grid_size, "+-*/")
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
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    screen_width, screen_height = screen.get_size()

    # Generate the game board based on the selected grid size
    game_board,groups = generate_board(grid_size,operation)
    # Store the initial state for the reset functionality
    initial_board = [row[:] for row in game_board]

    # Set the overall grid size to be consistent, e.g., 300x300 pixels
    overall_grid_size = 600
    cell_size = overall_grid_size // grid_size
    grid_width = overall_grid_size
    grid_height = overall_grid_size
    grid_x = 100  # Set grid position to the left with a fixed margin
    grid_y = (screen_height - grid_height) // 2

    num_images = []
    button_width = 30  # Define the width of the button
    button_height = 30  # Define the height of the button

    num_images = [pygame.image.load(f'resources/{i}.png') for i in range(1, grid_size + 1)]
    # Define number buttons with images
    button_size = 100  # Adjust button size to make it smaller
    button_spacing = 10

    # Define additional buttons on the right side of the screen
    button_x = screen_width - 150  # Adjust x position to align to the right with some margin
    button_y_start = 100  # Initial y position for the first button
    button_x_spacing = 150  # Spacing between the control buttons

    # Define buttons for new game and solve separately
    NEW_GAME_BUTTON = Button(image=new_game_img, pos=(button_x + button_x_spacing-400, button_y_start+520), text_input="", font=get_font(24, 1),
                             base_color=BLUE, hovering_color=H_BLUE)

    # Adjust button_y_start to move the SOLVE_BUTTON a little bit below NEW_GAME_BUTTON
    SOLVE_BUTTON = Button(image=solve_img, pos=(button_x + button_x_spacing-190, button_y_start + 520), text_input="",
                          font=get_font(24, 1),
                          base_color=BLUE, hovering_color=H_BLUE)

    # Define additional buttons for undo, reset, and erase
    UNDO_BUTTON = Button(image=undo_img, pos=(button_x - 290, button_y_start + 1 * button_y_start - 10), text_input="",
                         font=get_font(24, 1), base_color=BLUE, hovering_color=H_BLUE)
    RESET_BUTTON = Button(image=reset_img,
                          pos=(button_x + button_x_spacing - 290, button_y_start + 1 * button_y_start - 10),
                          text_input="", font=get_font(24, 1), base_color=BLUE, hovering_color=H_BLUE)
    ERASE_BUTTON = Button(image=erase_img,
                          pos=(button_x + 2 * button_x_spacing - 290, button_y_start +1  * button_y_start - 10),
                          text_input="", font=get_font(24, 1), base_color=BLUE, hovering_color=H_BLUE)

    # Combine all buttons into a list
    control_buttons = [NEW_GAME_BUTTON, SOLVE_BUTTON, UNDO_BUTTON, RESET_BUTTON, ERASE_BUTTON]


    # Calculate y position for the number buttons, starting below the last control button
    num_buttons_start_y = button_y_start + 5 * button_y_start + button_spacing

    # Adjust button_y_start for number buttons
    button_y_start = 400  # Adjust this value as needed
    distance_from_bottom = 50  # Adjust this value as needed

    num_buttons = []
    if grid_size == 3:
        button_x_start = button_x - 250  # Start x position for the first button, moved 250 pixels to the left for a 3x3 grid
    elif grid_size == 4:
        button_x_start = button_x - 300  # Start x position for the first button, moved 300 pixels to the left for a 4x4 grid
    elif grid_size == 6:
        button_x_start = button_x - 250  # Start x position for the first button, moved 200 pixels to the left for a 6x6 grid

    if grid_size == 4:
        for i in range(1, grid_size + 1):
            button_x = button_x_start + (i - 1) * (button_size + button_spacing)  # Adjust x position
            button_y = button_y_start + distance_from_bottom - 50  # Adjust y position
            resized_image = pygame.transform.scale(num_images[i - 1], (button_size, button_size))  # Resize image
            num_buttons.append(Button(image=resized_image, pos=(button_x, button_y), text_input="",
                                      font=get_font(24, 1), base_color="#D32735", hovering_color=RED))
    else:  # Assume 6x6 grid or 3x3 grid
        for i in range(1, grid_size + 1):
            button_x = button_x_start + ((i - 1) % 3) * (button_size + button_spacing)  # Adjust x position
            button_y = button_y_start + ((i - 1) // 3) * (button_size + button_spacing) - 50  # Adjust y position
            resized_image = pygame.transform.scale(num_images[i - 1], (button_size, button_size))  # Resize image
            num_buttons.append(Button(image=resized_image, pos=(button_x, button_y), text_input="",
                                      font=get_font(24, 1), base_color="#D32735", hovering_color=RED))

    # List to keep track of moves for undo functionality
    move_history = []

    # Initialize selected cell
    selected_cell = None

    # Initialize timer variables
    start_time = time.time()
    elapsed_time = 0

    # Placeholder loop to keep the screen open
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

        for group in groups:
            for i, j in group[:-2]:
                # Draw horizontal line
                if i < grid_size - 1 and (i + 1, j) in group:
                    pygame.draw.line(screen, (255, 255, 255), ((grid_x + j * cell_size )+2, (grid_y + (i + 1) * cell_size) - 1),
                                    ((grid_x + (j + 1) * cell_size ) - 3, (grid_y + (i + 1) * cell_size) - 1), 4)
                # Draw vertical line
                if j < grid_size - 1 and (i, j + 1) in group:
                    pygame.draw.line(screen, (255, 255, 255), ((grid_x + (j + 1) * cell_size) - 1 , (grid_y + i * cell_size)+ 2),
                                    ((grid_x + (j + 1) * cell_size) - 1 , (grid_y + (i + 1) * cell_size) - 3), 4)

            first_cell = group[0]
            if not isinstance(group[-1], tuple):
                sum_value = group[-1]
                text_op = group[-2]
                sum_text = str(sum_value)
                combined_text = sum_text + text_op
                font = pygame.font.Font(None, 36)
                text_surface = font.render(combined_text, True, (0, 0, 0))

                text_rect = text_surface.get_rect(
                    topleft=(grid_x + first_cell[1] * cell_size + 2, grid_y + first_cell[0] * cell_size + 2)
                )

                screen.blit(text_surface, text_rect)

                line_length = 3
                pygame.draw.line(screen, (0, 0, 0), (text_rect.right + 3, text_rect.top - 1),
                                    (text_rect.right + 3, text_rect.bottom + line_length), 3)
                pygame.draw.line(screen, (0, 0, 0), (text_rect.left - 1, text_rect.bottom + 2),
                                    (text_rect.right + line_length, text_rect.bottom + 2), 3)

        # Render control buttons
        for button in control_buttons:
            button.changeColor(pygame.mouse.get_pos())
            button.update(screen)

        # Render number buttons
        for button in num_buttons:
            button.changeColor(pygame.mouse.get_pos())
            button.update(screen)

        # Calculate elapsed time
        elapsed_time = time.time() - start_time
        minutes = int(elapsed_time // 60)
        seconds = int(elapsed_time % 60)

        # Render timer text
        font = pygame.font.SysFont(None, 60)
        timer_text = font.render(f" {minutes:02}:{seconds:02}", True, (255, 255, 255))
        timer_text_rect = timer_text.get_rect()
        timer_text_rect.topright = (screen_width - 40, 20)

        screen.blit(timer_text, timer_text_rect)

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
                                previous_value = game_board[selected_cell[1]][selected_cell[0]]
                                move_history.append((selected_cell, previous_value))
                                game_board[selected_cell[1]][selected_cell[0]] = i + 1
                    # Check if additional buttons are clicked
                    if NEW_GAME_BUTTON.checkForInput((mouse_x, mouse_y)):
                        start_game(grid_size, operation, difficulty)  # Restart the game
                    if SOLVE_BUTTON.checkForInput((mouse_x, mouse_y)):
                        solve_game(game_board)  # Placeholder for the solve functionality
                    if UNDO_BUTTON.checkForInput((mouse_x, mouse_y)):
                        if move_history:
                            last_move = move_history.pop()
                            selected_cell, previous_value = last_move
                            game_board[selected_cell[1]][selected_cell[0]] = previous_value
                    if RESET_BUTTON.checkForInput((mouse_x, mouse_y)):
                        game_board = [row[:] for row in initial_board]  # Reset to the initial state
                    if ERASE_BUTTON.checkForInput((mouse_x, mouse_y)):
                        if selected_cell:
                            previous_value = game_board[selected_cell[1]][selected_cell[0]]
                            move_history.append((selected_cell, previous_value))
                            game_board[selected_cell[1]][selected_cell[0]] = 0
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DELETE or event.key == pygame.K_BACKSPACE:
                    if selected_cell:
                        # Clear the value of the selected cell
                        previous_value = game_board[selected_cell[1]][selected_cell[0]]
                        move_history.append((selected_cell, previous_value))
                        game_board[selected_cell[1]][selected_cell[0]] = 0

def solve_game(game_board):
    # Placeholder function for the solve functionality
    # Implement the logic to solve the KenKen puzzle
    pass


def generate_board(grid_size,operation):
    # Generate a grid_size x grid_size game board
    # Create an instance of KenPuzzleMaker
    if(grid_size == 3):
        subgrid = 1
    else:
        subgrid = 2
    print("sizes")
    print(grid_size)
    print(subgrid)

    ken_solver = KenPuzzleMaker(grid_size)
    print("operation: ",operation)
    # Generate the Sudoku board
    ken_solver.updateOp(operation)

    ken_solver.generate_answer_board(grid_size,subgrid)
    updated_op = ken_solver.op
    print("updated op: ",updated_op)

    # Access the board, random, and groups values
    board = ken_solver.board
    updated_groups = ken_solver.getAllGroups()
    print(updated_groups)
    # random_instance = ken_solver.random
    # groups = ken_solver.groups

    # board = [[0] * grid_size for _ in range(grid_size)]
    # You can customize the board generation logic here

    print(board)
    return board,updated_groups


def main():
    # Initialize pygame
    pygame.init()

    # Load the background music
    pygame.mixer.music.load("resources/BG MUSIC.mp3")

    # Play the music on loop (-1 means infinite loop)
    pygame.mixer.music.play(-1)

    # Other initialization code
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


def controls():
    # Controls screen code
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
                    return  # Return to the main loop

        pygame.display.flip()


# play_intro_video()
main()
