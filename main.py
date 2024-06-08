import os
import sys
import time

import pygame
from moviepy.editor import VideoFileClip
from backend import KenPuzzleMaker
from backend import KenAiSolver
from button import Button
import random
import pygame.mixer
import cv2

# Initialize pygame and mixer
pygame.init()
pygame.mixer.init()
press_sound = pygame.mixer.Sound("resources/press.mp3")

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
background = pygame.image.load('resources/bgmenu.png')
backgroundselect = pygame.image.load('resources/selectbg.png')
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
home_img = pygame.image.load('resources/home.png')
back_img = pygame.image.load('resources/back.png')
playgame_img = pygame.image.load('resources/play_menu.png')
solver_img = pygame.image.load('resources/solve_menu.png')
controls_img = pygame.image.load('resources/tips.png')
exit_border = pygame.image.load('resources/border1.png')
start_border = pygame.image.load('resources/border2.png')
pencil_img = pygame.image.load('resources/pencil.png')
plus_img = pygame.image.load('resources/plus.png')
minus_img = pygame.image.load('resources/minus.png')
multiplication_img = pygame.image.load('resources/multiplication.png')
division_img = pygame.image.load('resources/division.png')
solver_erase_img = pygame.image.load('resources/solver_erase.png')
music_img = pygame.image.load('resources/music.png')
mute_img = pygame.image.load('resources/mute.png')
easy_img = pygame.image.load('resources/easy.png')
medium_img = pygame.image.load('resources/medium.png')
hard_img = pygame.image.load('resources/hard.png')


# Scale the 3x3 image
grid_3x3_image = pygame.transform.scale(grid_3x3_image, (280, 280))  # Adjust the size as per your requirement
grid_4x4_image = pygame.transform.scale(grid_4x4_image, (280, 280))
grid_6x6_image = pygame.transform.scale(grid_6x6_image, (280, 280))
plus_image = pygame.transform.scale(plus_image, (150, 150))
plus_minus_image = pygame.transform.scale(plus_minus_image, (150, 150))
multiply_divide_image = pygame.transform.scale(multiply_divide_image, (150, 150))
plus_minus_multiply_image = pygame.transform.scale(plus_minus_multiply_image, (150, 150))
random_image = pygame.transform.scale(random_image, (150, 150))
new_game_img = pygame.transform.scale(new_game_img, (430, 80))
solve_img = pygame.transform.scale(solve_img, (430, 80))
back_img = pygame.transform.scale(back_img, (100, 40))
undo_img = pygame.transform.scale(undo_img, (70, 70))
reset_img = pygame.transform.scale(reset_img, (70, 70))
erase_img = pygame.transform.scale(erase_img, (70, 70))
pencil_img = pygame.transform.scale(pencil_img, (70, 70))
playgame_img = pygame.transform.scale(playgame_img, (400, 400))
solver_img = pygame.transform.scale(solver_img, (400, 400))
home_img = pygame.transform.scale(home_img, (200, 100))
controls_img = pygame.transform.scale(controls_img, (70, 40))
exit_border = pygame.transform.scale(exit_border, (180, 60))
start_border = pygame.transform.scale(start_border, (210, 70))
plus_img = pygame.transform.scale(plus_img, (90, 90))
minus_img = pygame.transform.scale(minus_img, (90, 90))
multiplication_img = pygame.transform.scale(multiplication_img, (90, 90))
division_img = pygame.transform.scale(division_img, (90, 90))
solver_erase_img = pygame.transform.scale(solver_erase_img, (90, 90))
music_img = pygame.transform.scale(music_img, (70, 40))
mute_img = pygame.transform.scale(mute_img, (70, 40))
easy_img = pygame.transform.scale(easy_img, (250, 100))
medium_img = pygame.transform.scale(medium_img, (250, 100))
hard_img = pygame.transform.scale(hard_img, (250, 100))
pygame.display.set_caption("KenKen Puzzle")


def play_intro_video():
    clip = VideoFileClip("resources/start.mp4")
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
        screen.blit(backgroundselect, (0, 0))
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
    if type == 3:
        return pygame.font.Font("fonts/NerkoOne-Regular.ttf", size)





def select_grid_size(play):
    selecting = True
    while selecting:
        screen.blit(backgroundselect, (0, 0))
        SELECT_MOUSE_POS = pygame.mouse.get_pos()

        # Render "Select Grid Size" text
        TEXT = get_font(90, 3).render("Play Mode", True, (255, 248, 220))
        TEXT_RECT = TEXT.get_rect(center=(screen_width / 2, 120))  # Moved down by 50 pixels
        screen.blit(TEXT, TEXT_RECT)

        # Render "Select here" text
        SELECT_HERE_TEXT = get_font(40, 3).render("Select Grid Size", True, (247, 197, 102))
        SELECT_HERE_RECT = SELECT_HERE_TEXT.get_rect(center=(screen_width / 2, 200))  # Positioned below "Select Grid Size"
        screen.blit(SELECT_HERE_TEXT, SELECT_HERE_RECT)

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
        BACK_BUTTON = Button(image=back_img, pos=(screen.get_width() - back_img.get_width() + 10, 50),
                             # Adjusted x-coordinate
                             text_input="", font=get_font(68, 1), base_color="#D32735", hovering_color=RED)
        CONTROLS_BUTTON = Button(image=controls_img, pos=( screen_width - controls_img.get_width() - 20, screen_height - controls_img.get_height() - 20),
                                 text_input="", font=get_font(68, 1), base_color="#D32735", hovering_color=RED)
        if music_playing:
            MUSIC_BUTTON = Button(image=music_img, pos=(screen.get_width() - back_img.get_width() + 10, 610),
                                  text_input="", font=get_font(68, 1), base_color="#D32735", hovering_color=(255, 0, 0))
        else:
            MUSIC_BUTTON = Button(image=mute_img, pos=(screen.get_width() - back_img.get_width() + 10, 610),
                                  text_input="", font=get_font(68, 1), base_color="#D32735", hovering_color=(255, 0, 0))


        for button in [GRID_3x3_BUTTON, GRID_4x4_BUTTON, GRID_6x6_BUTTON, BACK_BUTTON, MUSIC_BUTTON,CONTROLS_BUTTON]:
            button.changeColor(SELECT_MOUSE_POS)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if GRID_3x3_BUTTON.checkForInput(SELECT_MOUSE_POS):
                    if play:
                        press_sound.play()
                        select_operations(3)
                    else:

                        play_loader()
                        start_solver(3)
                if GRID_4x4_BUTTON.checkForInput(SELECT_MOUSE_POS):
                    if play:
                        press_sound.play()
                        select_operations(4)
                    else:

                        play_loader()
                        start_solver(4)
                if GRID_6x6_BUTTON.checkForInput(SELECT_MOUSE_POS):
                    if play:
                        press_sound.play()
                        select_operations(6)
                    else:

                        play_loader()
                        start_solver(6)
                if CONTROLS_BUTTON.checkForInput(SELECT_MOUSE_POS):
                    press_sound.play()
                    controls()
                if BACK_BUTTON.checkForInput(SELECT_MOUSE_POS):
                    press_sound.play()
                    main_menu()
                if MUSIC_BUTTON.checkForInput(SELECT_MOUSE_POS):
                    press_sound.play()
                    toggle_music()

        pygame.display.update()



def select_operations(grid_size):
    selecting = True
    while selecting:
        screen.blit(backgroundselect, (0, 0))
        SELECT_MOUSE_POS = pygame.mouse.get_pos()
        TEXT = get_font(90, 3).render("Play Mode", True, (255, 248, 220))
        TEXT_RECT = TEXT.get_rect(center=(screen_width / 2, 120))  # Moved down by 50 pixels
        screen.blit(TEXT, TEXT_RECT)

        # Render "Select here" text
        SELECT_HERE_TEXT = get_font(40, 3).render("Select Operation", True, (247, 197, 102))
        SELECT_HERE_RECT = SELECT_HERE_TEXT.get_rect(
            center=(screen_width / 2, 200))  # Positioned below "Select Grid Size"
        screen.blit(SELECT_HERE_TEXT, SELECT_HERE_RECT)
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

        BACK_BUTTON = Button(image=back_img, pos=(screen.get_width() - back_img.get_width() + 10, 50),
                             # Adjusted x-coordinate
                             text_input="", font=get_font(68, 1), base_color="#D32735", hovering_color=RED)
        CONTROLS_BUTTON = Button(image=controls_img, pos=(
            screen_width - controls_img.get_width() - 20, screen_height - controls_img.get_height() - 20),
                                 text_input="", font=get_font(68, 1), base_color="#D32735", hovering_color=RED)

        if music_playing:
            MUSIC_BUTTON = Button(image=music_img, pos=(screen.get_width() - back_img.get_width() + 10, 610),
                                  text_input="", font=get_font(68, 1), base_color="#D32735", hovering_color=(255, 0, 0))
        else:
            MUSIC_BUTTON = Button(image=mute_img, pos=(screen.get_width() - back_img.get_width() + 10, 610),
                                  text_input="", font=get_font(68, 1), base_color="#D32735", hovering_color=(255, 0, 0))

        for button in [PLUS_BUTTON, PLUS_MINUS_BUTTON, MULTIPLY_DIVIDE_BUTTON, PLUS_MINUS_MULTIPLY_BUTTON,
                       RANDOM_BUTTON, BACK_BUTTON, CONTROLS_BUTTON,MUSIC_BUTTON]:
            button.changeColor(SELECT_MOUSE_POS)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLUS_BUTTON.checkForInput(SELECT_MOUSE_POS):
                    press_sound.play()
                    select_difficulty(grid_size, "+")
                if PLUS_MINUS_BUTTON.checkForInput(SELECT_MOUSE_POS):
                    press_sound.play()
                    select_difficulty(grid_size, "+-")
                if MULTIPLY_DIVIDE_BUTTON.checkForInput(SELECT_MOUSE_POS):
                    press_sound.play()
                    select_difficulty(grid_size, "*/")
                if PLUS_MINUS_MULTIPLY_BUTTON.checkForInput(SELECT_MOUSE_POS):
                    press_sound.play()
                    select_difficulty(grid_size, "+-*/")
                if RANDOM_BUTTON.checkForInput(SELECT_MOUSE_POS):
                    press_sound.play()
                    select_difficulty(grid_size, "?")
                if BACK_BUTTON.checkForInput(SELECT_MOUSE_POS):
                    press_sound.play()
                    selecting = False
                if CONTROLS_BUTTON.checkForInput(SELECT_MOUSE_POS):
                    press_sound.play()
                    controls()
                if MUSIC_BUTTON.checkForInput(SELECT_MOUSE_POS):
                    press_sound.play()
                    toggle_music()

        pygame.display.update()
def play_loader():
    cap = cv2.VideoCapture('resources/loader.mp4')
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_duration = 1 / fps

    while cap.isOpened():
        start_time = time.time()

        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (screen_width, screen_height))

        frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
        screen.blit(frame_surface, (0, 0))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                cap.release()
                pygame.quit()
                sys.exit()

        # Ensure the frame rate matches the video's original frame rate
        elapsed_time = time.time() - start_time
        if elapsed_time < frame_duration:
            time.sleep(frame_duration - elapsed_time)

    cap.release()

def select_difficulty(grid_size, operation):
    selecting = True
    while selecting:
        screen.blit(backgroundselect, (0, 0))
        SELECT_MOUSE_POS = pygame.mouse.get_pos()
        TEXT = get_font(90, 3).render("Play Mode", True, (255, 248, 220))
        TEXT_RECT = TEXT.get_rect(center=(screen_width / 2, 150))
        screen.blit(TEXT, TEXT_RECT)

        # Render "Select here" text
        SELECT_HERE_TEXT = get_font(40, 3).render("Select Difficulty", True, (247, 197, 102))
        SELECT_HERE_RECT = SELECT_HERE_TEXT.get_rect(center=(screen_width / 2, 230))
        screen.blit(SELECT_HERE_TEXT, SELECT_HERE_RECT)

        # Adjust the positions to be horizontal
        button_y_position = 400  # Common y position for all difficulty buttons
        horizontal_spacing = 200  # Space between each button

        EASY_BUTTON = Button(image=easy_img, pos=(screen_width / 2 - 1.5 * horizontal_spacing, button_y_position),
                             text_input="", font=get_font(68, 1), base_color="#D32735", hovering_color=RED)
        MEDIUM_BUTTON = Button(image=medium_img, pos=(screen_width / 2, button_y_position),
                               text_input="", font=get_font(68, 1), base_color="#D32735", hovering_color=RED)
        HARD_BUTTON = Button(image=hard_img, pos=(screen_width / 2 + 1.5 * horizontal_spacing, button_y_position),
                             text_input="", font=get_font(68, 1), base_color="#D32735", hovering_color=RED)
        BACK_BUTTON = Button(image=back_img, pos=(screen.get_width() - back_img.get_width() + 10, 50),
                             # Adjusted x-coordinate
                             text_input="", font=get_font(68, 1), base_color="#D32735", hovering_color=RED)
        CONTROLS_BUTTON = Button(image=controls_img, pos=(
            screen_width - controls_img.get_width() - 20, screen_height - controls_img.get_height() - 20),
                                 text_input="", font=get_font(68, 1), base_color="#D32735", hovering_color=RED)

        if music_playing:
            MUSIC_BUTTON = Button(image=music_img, pos=(screen.get_width() - back_img.get_width() + 10, 610),
                                  text_input="", font=get_font(68, 1), base_color="#D32735", hovering_color=(255, 0, 0))
        else:
            MUSIC_BUTTON = Button(image=mute_img, pos=(screen.get_width() - back_img.get_width() + 10, 610),
                                  text_input="", font=get_font(68, 1), base_color="#D32735", hovering_color=(255, 0, 0))

        for button in [EASY_BUTTON, MEDIUM_BUTTON, HARD_BUTTON, BACK_BUTTON,MUSIC_BUTTON,CONTROLS_BUTTON]:
            button.changeColor(SELECT_MOUSE_POS)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if EASY_BUTTON.checkForInput(SELECT_MOUSE_POS):
                    press_sound.play()
                    play_loader()
                    start_game(grid_size, operation, "EASY")
                if MEDIUM_BUTTON.checkForInput(SELECT_MOUSE_POS):
                    press_sound.play()
                    play_loader()
                    start_game(grid_size, operation, "MEDIUM")
                if HARD_BUTTON.checkForInput(SELECT_MOUSE_POS):
                    press_sound.play()
                    play_loader()
                    start_game(grid_size, operation, "HARD")
                if BACK_BUTTON.checkForInput(SELECT_MOUSE_POS):
                    press_sound.play()
                    selecting = False
                if CONTROLS_BUTTON.checkForInput(SELECT_MOUSE_POS):
                    press_sound.play()
                    controls()
                if MUSIC_BUTTON.checkForInput(SELECT_MOUSE_POS):
                    press_sound.play()
                    toggle_music()

        pygame.display.update()



def draw_grid_solver(screen, grid_size, cell_size, grid_x, grid_y, game_board,target_group, selected_group , groups, cells_left):

    for i in range(grid_size):
        for j in range(grid_size):
            cell_x = grid_x + j * cell_size
            cell_y = grid_y + i * cell_size
            cell_rect = pygame.Rect(cell_x, cell_y, cell_size, cell_size)
            cell_color = (255,248,220)  # Default color (white)

            if selected_group:
                for coordinate in selected_group:
                    x, y = coordinate 
                    if (i, j) == (x, y):
                        cell_color = (155,205,126)

            if target_group:
                for coordinate in target_group:
                    x, y = coordinate 
                    if (i, j) == (x, y):
                        cell_color = (235, 64, 52)

            if cells_left:
                for coordinate in cells_left:
                    x, y = coordinate 
                    if (i, j) == (x, y):
                        cell_color = BLUE



            pygame.draw.rect(screen, cell_color, cell_rect)
            pygame.draw.rect(screen, (0, 0, 0), cell_rect, 2)
            cell_value = game_board[i][j]

            if cell_value != 0:
                font = get_font(30, 3)
                text = font.render(str(cell_value), True, (0, 0, 0))  # Text color (black)
                text_rect = text.get_rect(center=(cell_x + cell_size // 2, cell_y + cell_size // 2))
                screen.blit(text, text_rect)

    if groups:
        for group in groups:
            # Separate the cells from the additional elements in the group
            cells = [item for item in group if isinstance(item, tuple)]
            extra_elements = [item for item in group if not isinstance(item, tuple)]

            for i, j in cells:
                color = (255,248,220)
                if cells == selected_group:
                    color = (155,205,126)

                if cells_left:
                    for coordinate in cells_left:
                        x, y = coordinate 
                        if (i, j) == (x, y):
                            color = BLUE

                # Draw horizontal line
                if i < grid_size - 1 and (i + 1, j) in cells:
                    pygame.draw.line(screen, color, ((grid_x + j * cell_size) + 2, (grid_y + (i + 1) * cell_size) - 1),
                                    ((grid_x + (j + 1) * cell_size) - 3, (grid_y + (i + 1) * cell_size) - 1), 4)
                # Draw vertical line
                if j < grid_size - 1 and (i, j + 1) in cells:
                    pygame.draw.line(screen, color, ((grid_x + (j + 1) * cell_size) - 1, (grid_y + i * cell_size) + 2),
                                    ((grid_x + (j + 1) * cell_size) - 1, (grid_y + (i + 1) * cell_size) - 3), 4)

            first_cell = cells[0]  # First cell in the group
            if len(extra_elements) >= 2 and isinstance(extra_elements[-2], int):
                sum_value = extra_elements[-2]
                text_op = extra_elements[-1]
                sum_text = str(sum_value)
                combined_text = sum_text + text_op
                font = pygame.font.Font(None, 36)
                text_surface = font.render(combined_text, True, (0, 0, 0))

                text_rect = text_surface.get_rect(
                    topleft=(grid_x + first_cell[1] * cell_size + 2, grid_y + first_cell[0] * cell_size + 2)
                )

                screen.blit(text_surface, text_rect)






def start_solver(grid_size):
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    screen_width, screen_height = screen.get_size()
    game_board = [[0] * grid_size for _ in range(grid_size)]
    overall_grid_size = 500
    cell_size = overall_grid_size // grid_size
    grid_width = overall_grid_size
    grid_height = overall_grid_size
    grid_x = 100
    grid_y = 160
    button_size = 100
    button_spacing = 10
    button_x = screen_width - 150  # Adjust x position to align to the right with some margin
    button_y_start = 100  # Initial y position for the first button
    button_x_spacing = 100  # Spacing between the control buttons


    # Load images for numbers 0-9
    num_images = [pygame.image.load(f'resources/{i}.png') for i in range(10)]

    NEW_GAME_BUTTON = Button(image=new_game_img, pos=(button_x - 200, button_y_start + 330 + 100),
                             text_input="", font=get_font(24, 1),
                             base_color=BLUE, hovering_color=H_BLUE)

    SOLVE_BUTTON = Button(image=solve_img, pos=(button_x - 200, button_y_start + 520),
                          text_input="",
                          font=get_font(24, 1),
                          base_color=BLUE, hovering_color=H_BLUE)

    PLUS_BUTTON = Button(image=plus_img, pos=(button_x - 420, button_y_start + 80), text_input="",
                         font=get_font(24, 1), base_color=BLUE, hovering_color=H_BLUE)

    MINUS_BUTTON = Button(image=minus_img,
                          pos=(button_x + button_x_spacing - 410, button_y_start + 80),
                          text_input="", font=get_font(24, 1), base_color=BLUE, hovering_color=H_BLUE)

    TIMES_BUTTON = Button(image=multiplication_img,
                          pos=(button_x + 2 * button_x_spacing - 400, button_y_start + 80),
                          text_input="", font=get_font(24, 1), base_color=BLUE, hovering_color=H_BLUE)

    DIVIDE_BUTTON = Button(image=division_img,
                           pos=(button_x + 3 * button_x_spacing - 390, button_y_start + 80),
                           text_input="", font=get_font(24, 1), base_color=BLUE, hovering_color=H_BLUE)
    ERASE_BUTTON = Button(image=solver_erase_img,
                          pos=(button_x + 4 * button_x_spacing - 380, button_y_start + 80),
                          text_input="", font=get_font(24, 1), base_color=BLUE, hovering_color=H_BLUE)
    PLAY_AGAIN_BUTTON = Button(image=new_game_img,
                          pos=(screen_width // 2, screen_height // 2),
                          text_input="", font=get_font(24, 1), base_color=BLUE, hovering_color=H_BLUE)
    BACK_BUTTON = Button(image=back_img, pos=(screen_width - back_img.get_width() + 10, 50),
                         text_input="", font=get_font(24, 1), base_color=BLUE, hovering_color=H_BLUE)
    CONTROLS_BUTTON = Button(image=controls_img, pos=(
    screen.get_width() - controls_img.get_width() - 5, screen.get_height() - controls_img.get_height() - 5),
                             text_input="", font=get_font(68, 1), base_color="#D32735", hovering_color=RED)

    if music_playing:
        MUSIC_BUTTON = Button(image=music_img, pos=(screen.get_width() - back_img.get_width() + 25, 620),
                              text_input="", font=get_font(68, 1), base_color="#D32735", hovering_color=(255, 0, 0))
    else:
        MUSIC_BUTTON = Button(image=mute_img, pos=(screen.get_width() - back_img.get_width() + 25, 620),
                              text_input="", font=get_font(68, 1), base_color="#D32735", hovering_color=(255, 0, 0))

    control_buttons = [NEW_GAME_BUTTON, SOLVE_BUTTON, PLUS_BUTTON, MINUS_BUTTON, TIMES_BUTTON, BACK_BUTTON, DIVIDE_BUTTON, CONTROLS_BUTTON, ERASE_BUTTON,MUSIC_BUTTON]
    num_buttons_start_y = button_y_start + 5 * button_y_start + button_spacing
    button_y_start = 350  # Adjust this value as needed
    num_buttons = []
    button_x_start = button_x - 420  # Start x position for the first button, moved 300 pixels to the left

    # Position buttons in a 5x2 grid layout for numbers 0-9
    for i in range(10):
        button_x = button_x_start + (i % 5) * (button_size + button_spacing)  # Adjust x position
        button_y = button_y_start + (i // 5) * (button_size + button_spacing) - 50  # Adjust y position
        resized_image = pygame.transform.scale(num_images[i], (button_size, button_size))  # Resize image
        num_buttons.append(Button(image=resized_image, pos=(button_x, button_y), text_input="",
                                  font=get_font(24, 1), base_color="#D32735", hovering_color=RED))

    move_history = []
    selected_group = None
    target_group = []
    ken_solver = KenPuzzleMaker(grid_size)
    ken_solver.generate_empty_board()
    cells_left = []
    wrong = False
    def init():
        nonlocal move_history, selected_group, target_group, ken_solver, game_board, wrong
        move_history = []
        selected_group = None
        target_group = []
        ken_solver = KenPuzzleMaker(grid_size)
        game_board = [[0] * grid_size for _ in range(grid_size)]
        wrong = False

    def is_valid(selected_cell, target_group, grid_size):
        for group in ken_solver.solver_group:
            if selected_cell in group:
                print("in group")

                return False
            
        if not target_group:
            return True
        

        
        x, y = selected_cell
    
        adjacent_positions = [
            (x-1, y),  # Above
            (x+1, y),  # Below
            (x, y-1),  # Left
            (x, y+1),   # Right
            (x, y)

        ]
        
        valid_adjacent_positions = [
            (i, j) for i, j in adjacent_positions
            if 0 <= i < grid_size and 0 <= j < grid_size
        ]
        
        for cell in target_group:
            if cell in valid_adjacent_positions:
                return True
            
        print("False in main")

        return False
    
    while True:
        screen.blit(backgroundselect, (0, 0))
        draw_grid_solver(screen, grid_size, cell_size, grid_x, grid_y, game_board,target_group, selected_group , ken_solver.solver_group, cells_left)

        for button in control_buttons:
            button.changeColor(pygame.mouse.get_pos())
            button.update(screen)

        for button in num_buttons:
            button.changeColor(pygame.mouse.get_pos())
            button.update(screen)

        if wrong:
            PLAY_AGAIN_BUTTON.update(screen)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                cells_left = []
                if event.button == 1: # Left click
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if grid_x <= mouse_x < grid_x + grid_width and grid_y <= mouse_y < grid_y + grid_height:
                        cell_x = (mouse_x - grid_x) // cell_size
                        cell_y = (mouse_y - grid_y) // cell_size
                        selected_cell = (cell_y, cell_x)
                        print("selected cell: ",selected_cell)
                        selected_group = ken_solver.find_group_coordinates(selected_cell)
                        print("Selected group: ",selected_group)
                        current_sum = 0
                    else:
                        for i, button in enumerate(num_buttons):
                            if button.checkForInput((mouse_x, mouse_y)):
                                if selected_group:
                                    num_clicked = i
                                    current_sum = current_sum * 10 + num_clicked
                                    print(current_sum)
                                    curr_group = ken_solver.findGroup(selected_group)
                                    curr_op = ken_solver.getGroupOp(curr_group)
                                    print("curr_group: ",curr_group)
                                    print("curop: ",curr_op)
                                    ken_solver.update_group(selected_group,current_sum,curr_op)
                        if NEW_GAME_BUTTON.checkForInput((mouse_x, mouse_y)):
                            init()
                        if SOLVE_BUTTON.checkForInput((mouse_x, mouse_y)):
                            result , cells_left = ken_solver.check_tuples_in_group(grid_size,ken_solver.solver_group)
                            print("result: ",result)
                            print("cell left: ",cells_left)
                            if result:
                                solution_board = solve_game(ken_solver.solver_group,grid_size,screen,cell_size, grid_x, grid_y, game_board,target_group, selected_group)
                                if solution_board:
                                    game_board = solution_board
                                else:
                                    wrong = True
                        if MUSIC_BUTTON.checkForInput(pygame.mouse.get_pos()):
                            press_sound.play()
                            toggle_music()
                        if PLUS_BUTTON.checkForInput((mouse_x, mouse_y)):
                            print("clicked1")
                            if selected_group:
                                op_clicked = "+"
                                print(op_clicked)
                                curr_group = ken_solver.findGroup(selected_group)
                                total = ken_solver.getGroupTotal(curr_group)
                                print("curr_group: ",curr_group)
                                print("total: ",total)
                                ken_solver.update_group(selected_group,total,op_clicked)
                        if PLAY_AGAIN_BUTTON.checkForInput((mouse_x, mouse_y)) and wrong:
                            init()
                        if MINUS_BUTTON.checkForInput((mouse_x, mouse_y)):
                            print("clicked2")
                            if selected_group:
                                op_clicked = "-"
                                print(op_clicked)
                                curr_group = ken_solver.findGroup(selected_group)
                                total = ken_solver.getGroupTotal(curr_group)
                                print("curr_group: ",curr_group)
                                print("total: ",total)
                                ken_solver.update_group(selected_group,total,op_clicked)                        
                        if TIMES_BUTTON.checkForInput((mouse_x, mouse_y)):
                            print("clicked3")
                            if selected_group:
                                op_clicked = "*"
                                print(op_clicked)
                                curr_group = ken_solver.findGroup(selected_group)
                                total = ken_solver.getGroupTotal(curr_group)
                                print("curr_group: ",curr_group)
                                print("total: ",total)
                                ken_solver.update_group(selected_group,total,op_clicked)
                        if DIVIDE_BUTTON.checkForInput((mouse_x, mouse_y)):
                            print("clicked4")
                            if selected_group:
                                op_clicked = "/"
                                print(op_clicked)
                                curr_group = ken_solver.findGroup(selected_group)
                                total = ken_solver.getGroupTotal(curr_group)
                                print("curr_group: ",curr_group)
                                print("total: ",total)
                                ken_solver.update_group(selected_group,total,op_clicked)
                        if BACK_BUTTON.rect.collidepoint(event.pos):
                            press_sound.play()
                            main_menu()
                        if ERASE_BUTTON.checkForInput((mouse_x, mouse_y)):
                            if selected_group:
                                ken_solver.removeGroup(selected_group)
                        if CONTROLS_BUTTON.checkForInput((mouse_x, mouse_y)):
                            press_sound.play()
                            controls()

                elif event.button == 3:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if grid_x <= mouse_x < grid_x + grid_width and grid_y <= mouse_y < grid_y + grid_height :
                        cell_x = (mouse_x - grid_x) // cell_size
                        cell_y = (mouse_y - grid_y) // cell_size
                        selected_cell = (cell_y, cell_x)
                        if target_group:
                            if not is_valid(selected_cell,target_group,grid_size):
                                print("False here")
                                selected_cell = None
                            else:
                                if selected_cell in target_group:
                                    target_group.remove(selected_cell)
                                else:
                                    print("solvergroup: ",ken_solver.solver_group)
                                    target_group.append(selected_cell)       
                        else:
                            if not is_valid(selected_cell,target_group,grid_size):
                                selected_cell = None
                            else:
                                if selected_cell in target_group:
                                    target_group.remove(selected_cell)
                                else:
                                    target_group.append(selected_cell)      


            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DELETE or event.key == pygame.K_BACKSPACE:
                    if selected_group:
                        previous_value = game_board[selected_group[1]][selected_group[0]]
                        move_history.append((selected_group, previous_value))
                        game_board[selected_group[1]][selected_group[0]] = 0
                if event.key == pygame.K_RETURN:
                    if target_group:
                        ken_solver.add_group(target_group)
                        print("solver: ",ken_solver.solver_group)
                        print("SAVED")
                        target_group = []
def solve_game(puzzle, grid_size, screen, cell_size, grid_x, grid_y, game_board, target_group, selected_group):
    def draw_update(game_board):
        # This function updates the display with the current board state
        draw_grid_solver(screen, grid_size, cell_size, grid_x, grid_y, game_board, target_group, selected_group, puzzle, [])
        pygame.display.update()
        time.sleep(0.3)  # Adjust the delay as needed to visualize the steps

    # Initial drawing of the puzzle
    draw_update(game_board)
    
    ken_ai = KenAiSolver(puzzle, draw_update)
    solution_board = ken_ai.solve_kenken(grid_size)

    return False
    
def draw_grid_play(screen, grid_size, cell_size, grid_x, grid_y, game_board, selected_cell, operation ,groups , board_answer ,pencil_marks):
    for i in range(grid_size):
        for j in range(grid_size):
            cell_x = grid_x + j * cell_size
            cell_y = grid_y + i * cell_size
            cell_rect = pygame.Rect(cell_x, cell_y, cell_size, cell_size)
            cell_value = game_board[i][j]
            cell_answer = board_answer[i][j]

            cell_color = (255,248,220)  
            if selected_cell and (j, i) == selected_cell:
                cell_color = (247, 197, 102) 

            if cell_value != 0:
                # print("value: ",cell_value)
                # print("answer: ",cell_answer)
                if cell_value == cell_answer:
                    cell_color = (155,205,126)
                else:
                    cell_color = (235, 64, 52)

            pygame.draw.rect(screen, cell_color, cell_rect)

            # Render cell border
            pygame.draw.rect(screen, (0,0,0), cell_rect, 2)

            # Render cell value
            if cell_value != 0:
                font = pygame.font.SysFont(None, 36)
                text = font.render(str(cell_value), True, (0,0,0))  # Text color (black)
                text_rect = text.get_rect(center=(cell_x + cell_size // 2, cell_y + cell_size // 2))
                screen.blit(text, text_rect)
            else:
                # Render penciled-in numbers
                penciled_nums = pencil_marks[i][j]
                if penciled_nums:
                    font = pygame.font.SysFont(None, 20)
                    for n in penciled_nums:
                        text = font.render(str(n), True, (0, 0, 0))
                        text_rect = text.get_rect(center=(cell_x + (n-1) % 3 * (cell_size // 3 -5) + cell_size // 6 + 5, cell_y + (n-1) // 3 * (cell_size // 3 -5) + cell_size // 6 + 23))
                        screen.blit(text, text_rect)


    for group in groups:
        for i, j in group[:-2]:
            # Draw horizontal line
            color = (255,248,220)
            if selected_cell and (j, i) == selected_cell:
                color = (247, 197, 102) 
            if game_board[i][j]:
                if game_board[i][j] != board_answer[i][j]:
                    color = (235, 64, 52)
                else:
                    color = (155,205,126)


            if i < grid_size - 1 and (i + 1, j) in group:
                pygame.draw.line(screen, color, ((grid_x + j * cell_size )+2, (grid_y + (i + 1) * cell_size) - 1),
                                ((grid_x + (j + 1) * cell_size ) - 3, (grid_y + (i + 1) * cell_size) - 1), 4)
            # Draw vertical line
            if j < grid_size - 1 and (i, j + 1) in group:
                pygame.draw.line(screen, color, ((grid_x + (j + 1) * cell_size) - 1 , (grid_y + i * cell_size)+ 2),
                                ((grid_x + (j + 1) * cell_size) - 1 , (grid_y + (i + 1) * cell_size) - 3), 4)

        first_cell = group[0]
        if not isinstance(group[-1], tuple):
            sum_value = group[-1]
            text_op = group[-2]
            sum_text = str(sum_value)
            combined_text = sum_text + text_op
            font = get_font(30, 3)
            text_surface = font.render(combined_text, True, (0, 0, 0))

            text_rect = text_surface.get_rect(
                topleft=(grid_x + first_cell[1] * cell_size + 2, grid_y + first_cell[0] * cell_size + 2)
            )

            screen.blit(text_surface, text_rect)


def start_game(grid_size, operation, difficulty):
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    screen_width, screen_height = screen.get_size()

    # Generate the game board based on the selected grid size
    game_board = [[0] * grid_size for _ in range(grid_size)]
    initial_board = [row[:] for row in game_board]

    # Set the overall grid size to be consistent, e.g., 500x500 pixels
    overall_grid_size = 500
    cell_size = overall_grid_size // grid_size
    grid_x = 150  # Set grid position to the left with a fixed margin
    grid_y = 160

    num_images = [pygame.image.load(f'resources/{i}.png') for i in range(1, grid_size + 1)]
    button_size = 95  # Adjust button size to make it smaller
    button_spacing = 25

    # Define additional buttons on the right side of the screen
    button_x = screen_width - 150  # Adjust x position to align to the right with some margin
    button_y_start = 0  # Initial y position for the first button
    button_x_spacing = 100  # Spacing between the control buttons

    NEW_GAME_BUTTON = Button(image=new_game_img, pos=(button_x - 150, button_y_start + 520 + 100),
                             text_input="", font=get_font(24, 1),
                             base_color=BLUE, hovering_color=H_BLUE)

    SOLVE_BUTTON = Button(image=solve_img, pos=(button_x - 150, button_y_start + 520),
                          text_input="",
                          font=get_font(24, 1), base_color=BLUE, hovering_color=H_BLUE)

    PENCIL_BUTTON = Button(image=pencil_img,
                           pos=(button_x - 310, button_y_start + 1 * button_y_start + 200),
                           text_input="", font=get_font(24, 1), base_color=BLUE, hovering_color=H_BLUE)
    ERASE_BUTTON = Button(image=erase_img,
                          pos=(button_x + button_x_spacing - 300, button_y_start + 1 * button_y_start + 200),
                          text_input="", font=get_font(24, 1), base_color=BLUE, hovering_color=H_BLUE)
    UNDO_BUTTON = Button(image=undo_img,
                         pos=(button_x + 2 * button_x_spacing - 290, button_y_start + 1 * button_y_start + 200),
                         text_input="",
                         font=get_font(24, 1), base_color=BLUE, hovering_color=H_BLUE)
    RESET_BUTTON = Button(image=reset_img,
                          pos=(button_x + 3 * button_x_spacing - 280, button_y_start + 1 * button_y_start + 200),
                          text_input="", font=get_font(24, 1), base_color=BLUE, hovering_color=H_BLUE)
    PLAY_AGAIN_BUTTON = Button(image=new_game_img,
                          pos=(screen_width // 2, screen_height // 2),
                          text_input="", font=get_font(24, 1), base_color=BLUE, hovering_color=H_BLUE)

    BACK_BUTTON = Button(image=back_img, pos=(screen_width - back_img.get_width() + 10, 50),
                         text_input="", font=get_font(24, 1), base_color=BLUE, hovering_color=H_BLUE)

    CONTROLS_BUTTON = Button(image=controls_img, pos=(
        screen.get_width() - back_img.get_width() + 55, 690),
                             text_input="", font=get_font(68, 1), base_color="#D32735", hovering_color=RED)

    if music_playing:
        MUSIC_BUTTON = Button(image=music_img, pos=(screen.get_width() - back_img.get_width() + 55, 640),
                              text_input="", font=get_font(68, 1), base_color="#D32735", hovering_color=(255, 0, 0))
    else:
        MUSIC_BUTTON = Button(image=mute_img, pos=(screen.get_width() - back_img.get_width() + 55, 620),
                              text_input="", font=get_font(68, 1), base_color="#D32735", hovering_color=(255, 0, 0))

    control_buttons = [NEW_GAME_BUTTON, SOLVE_BUTTON, UNDO_BUTTON, RESET_BUTTON, ERASE_BUTTON, BACK_BUTTON,
                       PENCIL_BUTTON,CONTROLS_BUTTON,MUSIC_BUTTON]

    num_buttons_start_y = button_y_start + 6 * button_spacing
    button_y_start = 350
    distance_from_bottom = 50

    num_buttons = []

    if grid_size == 3:
        button_x_start = button_x - 270
    elif grid_size == 4:
        button_x_start = button_x - 330
    elif grid_size == 6:
        button_x_start = button_x - 270

    if grid_size == 3:
        for i in range(1, grid_size + 1):
            button_x = button_x_start + ((i - 1) % 3) * (button_size + button_spacing)
            button_y = button_y_start + ((i - 1) // 3) * (button_size + button_spacing) + 10
            resized_image = pygame.transform.scale(num_images[i - 1], (button_size, button_size))
            num_buttons.append(Button(image=resized_image, pos=(button_x, button_y), text_input="",
                                      font=get_font(24, 1), base_color="#D32735", hovering_color=RED))
    elif grid_size == 4:
        for i in range(1, grid_size + 1):
            button_x = button_x_start + (i - 1) * (button_size + button_spacing)
            button_y = button_y_start + distance_from_bottom - 50
            resized_image = pygame.transform.scale(num_images[i - 1], (button_size, button_size))
            num_buttons.append(Button(image=resized_image, pos=(button_x, button_y), text_input="",
                                      font=get_font(24, 1), base_color="#D32735", hovering_color=RED))
    elif grid_size == 6:
        for i in range(1, grid_size + 1):
            button_x = button_x_start + ((i - 1) % 3) * (button_size + button_spacing)
            button_y = button_y_start + ((i - 1) // 3) * (button_size + button_spacing) - 50
            resized_image = pygame.transform.scale(num_images[i - 1], (button_size, button_size))
            num_buttons.append(Button(image=resized_image, pos=(button_x, button_y), text_input="",
                                      font=get_font(24, 1), base_color="#D32735", hovering_color=RED))

    move_history = []
    selected_cell = None
    start_time = time.time()
    elapsed_time = 0
    available_cells = {(x, y) for x in range(grid_size) for y in range(grid_size)}
    pencil_mode = False
    pencil_marks = [[set() for _ in range(grid_size)] for _ in range(grid_size)]
   # pencil_marks = [[set(range(1, grid_size + 1)) for _ in range(grid_size)] for _ in range(grid_size)]
    solve= False
    def init():
        nonlocal move_history, selected_cell, start_time, elapsed_time, available_cells, pencil_mode, pencil_marks, solve
        move_history = []
        selected_cell = None
        start_time = time.time()
        elapsed_time = 0
        available_cells = {(x, y) for x in range(grid_size) for y in range(grid_size)}
        pencil_mode = False
        pencil_marks = [[set() for _ in range(grid_size)] for _ in range(grid_size)]
        solve = False
        
    # Placeholder loop to keep the screen open
    board_answer, groups = generate_board(grid_size, operation)
    
    def transfer_values(board_answer, difficulty):
        # Determine grid size
        grid_size = len(board_answer)
        total_cells = grid_size * grid_size

        # Determine number of cells to fill based on difficulty
        if difficulty == "EASY":
            num_cells_to_fill = total_cells * 50 // 100
        elif difficulty == "MEDIUM":
            num_cells_to_fill = total_cells * 25 // 100
        else:
            num_cells_to_fill = 0
        # Create the game board with zeros
        game_board = [[0 for _ in range(grid_size)] for _ in range(grid_size)]

        # Get a list of all cell positions
        all_cells = [(i, j) for i in range(grid_size) for j in range(grid_size)]

        # Randomly select the cells to fill
        selected_cells = random.sample(all_cells, num_cells_to_fill)

        # Shuffle the selected cells to randomize the positions
        random.shuffle(selected_cells)

        # Transfer the values from board_answer to game_board in random positions
        for (i, j) in selected_cells:
            game_board[i][j] = board_answer[i][j]

        return game_board
    print("difficulty: ",difficulty)
    if difficulty == "EASY" or "MEDIUM":
        print("inside")
        game_board = transfer_values(board_answer,difficulty)
    
    while True:
        screen.blit(backgroundselect, (0, 0))
        draw_grid_play(screen, grid_size, cell_size, grid_x, grid_y, game_board, selected_cell, operation, groups, board_answer, pencil_marks)

        # Render control buttons
        for button in control_buttons:
            button.changeColor(pygame.mouse.get_pos())
            button.update(screen)

        # Render number buttons
        for button in num_buttons:
            button.changeColor(pygame.mouse.get_pos())
            button.update(screen)

        # Calculate elapsed 
        if not solve:
            elapsed_time = time.time() - start_time
        minutes = int(elapsed_time // 60)
        seconds = int(elapsed_time % 60)

        # Render timer text
        font = get_font(45, 3)
        timer_text = font.render(f"{minutes:02}:{seconds:02}", True, (247, 197, 102))
        timer_text_rect = timer_text.get_rect()
        timer_text_rect.centerx = screen_width // 2  # Center horizontally
        timer_text_rect.top = 85  # Positioned at the top

        screen.blit(timer_text, timer_text_rect)

        # Render difficulty text
        difficulty_font = get_font(70, 3)
        difficulty_text = difficulty_font.render(difficulty, True, (255, 248, 220))
        difficulty_text_rect = difficulty_text.get_rect(center=(screen_width / 2, 60))
        screen.blit(difficulty_text, difficulty_text_rect)

        if solve:
            PLAY_AGAIN_BUTTON.update(screen)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if grid_x <= mouse_x < grid_x + overall_grid_size and grid_y <= mouse_y < grid_y + overall_grid_size:
                    cell_x = (mouse_x - grid_x) // cell_size
                    cell_y = (mouse_y - grid_y) // cell_size
                    selected_cell = (cell_x, cell_y)
                else:
                    for i, button in enumerate(num_buttons):
                        if button.checkForInput((mouse_x, mouse_y)):
                            if selected_cell:
                                if pencil_mode:
                                    if (i + 1) in pencil_marks[selected_cell[1]][selected_cell[0]]:
                                        pencil_marks[selected_cell[1]][selected_cell[0]].remove(i + 1)
                                    else:
                                        pencil_marks[selected_cell[1]][selected_cell[0]].add(i + 1)
                                else:
                                    previous_value = game_board[selected_cell[1]][selected_cell[0]]
                                    move_history.append((selected_cell, previous_value))
                                    game_board[selected_cell[1]][selected_cell[0]] = i + 1
                                    if (game_board[selected_cell[1]][selected_cell[0]] == board_answer[selected_cell[1]][selected_cell[0]]):
                                        print("correct")
                                        value = i + 1

                                        # Remove the value from the pencil marks in the same row and column
                                        for x in range(grid_size):
                                            if value in pencil_marks[selected_cell[1]][x]:
                                                pencil_marks[selected_cell[1]][x].remove(value)
                                            if value in pencil_marks[x][selected_cell[0]]:
                                                pencil_marks[x][selected_cell[0]].remove(value)

                                        # Determine sub-grid size
                                        if grid_size == 3:
                                            sub_grid_width = sub_grid_height = 3
                                        elif grid_size == 4:
                                            sub_grid_width = sub_grid_height = 2
                                        elif grid_size == 6:
                                            sub_grid_width, sub_grid_height = 3, 2

                                        # Calculate sub-grid starting coordinates
                                        sub_grid_x = (selected_cell[0] // sub_grid_width) * sub_grid_width
                                        sub_grid_y = (selected_cell[1] // sub_grid_height) * sub_grid_height

                                        # Remove the value from the pencil marks in the same sub-grid
                                        for y in range(sub_grid_y, sub_grid_y + sub_grid_height):
                                            for x in range(sub_grid_x, sub_grid_x + sub_grid_width):
                                                if value in pencil_marks[y][x]:
                                                    pencil_marks[y][x].remove(value)
                    if NEW_GAME_BUTTON.checkForInput((mouse_x, mouse_y)):
                        board_answer, groups = generate_board(grid_size, operation)
                        game_board = [row[:] for row in initial_board]
                        init()
                    if SOLVE_BUTTON.checkForInput((mouse_x, mouse_y)):
                        if selected_cell:
                            for i in range(grid_size):
                                for j in range(grid_size):
                                    if selected_cell == (j, i):
                                        game_board[i][j] = board_answer[i][j]
                                        available_cells.remove(selected_cell)
                        else:
                            if available_cells:
                                random_cell = random.choice(tuple(available_cells))
                                available_cells.remove(random_cell)
                            for i in range(grid_size):
                                for j in range(grid_size):
                                    if random_cell == (j, i):
                                        game_board[i][j] = board_answer[i][j]
                        selected_cell = None
                        print("board: ",game_board)
                    if UNDO_BUTTON.checkForInput((mouse_x, mouse_y)):
                        if move_history:
                            last_move = move_history.pop()
                            selected_cell, previous_value = last_move
                            game_board[selected_cell[1]][selected_cell[0]] = previous_value
                    if RESET_BUTTON.checkForInput((mouse_x, mouse_y)):
                        game_board = [row[:] for row in initial_board]
                    if BACK_BUTTON.rect.collidepoint(event.pos):
                        main_menu()
                    if ERASE_BUTTON.checkForInput((mouse_x, mouse_y)):
                        if selected_cell:
                            previous_value = game_board[selected_cell[1]][selected_cell[0]]
                            move_history.append((selected_cell, previous_value))
                            game_board[selected_cell[1]][selected_cell[0]] = 0
                            print("pencil: ",pencil_marks)
                            pencil_marks[selected_cell[1]][selected_cell[0]].clear()

                    if CONTROLS_BUTTON.checkForInput((mouse_x, mouse_y)):
                        press_sound.play()
                        controls()
                    if MUSIC_BUTTON.checkForInput((mouse_x, mouse_y)):
                        press_sound.play()
                        toggle_music()
                    if PENCIL_BUTTON.checkForInput((mouse_x, mouse_y)):
                        pencil_mode = not pencil_mode
                    if PLAY_AGAIN_BUTTON.checkForInput((mouse_x, mouse_y)) and solve:
                        board_answer, groups = generate_board(grid_size, operation)
                        game_board = [row[:] for row in initial_board]
                        init()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DELETE or event.key == pygame.K_BACKSPACE:
                    if selected_cell:
                        previous_value = game_board[selected_cell[1]][selected_cell[0]]
                        move_history.append((selected_cell, previous_value))
                        game_board[selected_cell[1]][selected_cell[0]] = 0
            if game_board == board_answer:
                solve = True



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

    ken_play = KenPuzzleMaker(grid_size)
    print("operation: ",operation)
    # Generate the Sudoku board
    ken_play.updateOp(operation)

    ken_play.generate_answer_board(grid_size,subgrid)
    updated_op = ken_play.op
    print("updated op: ",updated_op)

    # Access the board, random, and groups values
    board = ken_play.board
    updated_groups = ken_play.getAllGroups()
    print(updated_groups)
    # random_instance = ken_play.random
    # groups = ken_play.groups

    # board = [[0] * grid_size for _ in range(grid_size)]
    # You can customize the board generation logic here

    print(board)
    return board,updated_groups


def main():
    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()

    # Load video
    cap = cv2.VideoCapture('resources/Intro.mp4')

    while True:
        MENU_MOUSE_POS = pygame.mouse.get_pos()

        # Read video frame
        ret, frame = cap.read()
        if not ret:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            ret, frame = cap.read()

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (screen_width, screen_height))
        frame = pygame.surfarray.make_surface(frame.swapaxes(0, 1))

        screen.blit(frame, (0, 0))

        # Calculate the positions of buttons to center them
        button_width = 200
        button_height = 50
        start_button_x = (screen_width - button_width) // 2 + 90
        start_button_y = screen_height // 2 + 190
        exit_button_x = (screen_width - button_width) // 2 + 90
        exit_button_y = screen_height // 2 + 270
        controls_button_x = screen_width - controls_img.get_width() - 20
        controls_button_y = screen_height - controls_img.get_height() - 20
        music_button_x = screen_width - music_img.get_width() - 20
        music_button_y = screen_height - music_img.get_height() - 70

        START_BUTTON = Button(image=start_border, pos=(start_button_x, start_button_y),
                              text_input="START", font=get_font(35, 3), base_color="#FFF8DC", hovering_color="#FFF8DC")
        EXIT_BUTTON = Button(image=exit_border, pos=(exit_button_x, exit_button_y),
                             text_input="Exit", font=get_font(30, 3), base_color="#000000", hovering_color="#000000")
        CONTROLS_BUTTON = Button(image=controls_img, pos=(controls_button_x, controls_button_y),
                                 text_input="", font=get_font(68, 1), base_color="#D32735", hovering_color=(255, 0, 0))
        if music_playing:
            MUSIC_BUTTON = Button(image=music_img, pos=(music_button_x, music_button_y),
                                  text_input="", font=get_font(68, 1), base_color="#D32735", hovering_color=(255, 0, 0))
        else:
            MUSIC_BUTTON = Button(image=mute_img, pos=(music_button_x, music_button_y),
                                  text_input="", font=get_font(68, 1), base_color="#D32735", hovering_color=(255, 0, 0))

        START_BUTTON.changeColor(MENU_MOUSE_POS)
        EXIT_BUTTON.changeColor(MENU_MOUSE_POS)
        CONTROLS_BUTTON.changeColor(MENU_MOUSE_POS)
        MUSIC_BUTTON.changeColor(MENU_MOUSE_POS)

        START_BUTTON.update(screen)
        EXIT_BUTTON.update(screen)
        CONTROLS_BUTTON.update(screen)
        MUSIC_BUTTON.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                cap.release()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if START_BUTTON.checkForInput(MENU_MOUSE_POS):
                    press_sound.play()  # Play press sound
                    cap.release()
                    return
                if CONTROLS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    press_sound.play()  # Play press sound
                    controls()
                if MUSIC_BUTTON.checkForInput(MENU_MOUSE_POS):
                    press_sound.play()  # Play press sound
                    toggle_music()
                if EXIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    press_sound.play()  # Play press sound
                    pygame.quit()
                    cap.release()
                    sys.exit()

        pygame.display.update()
        clock.tick(30)  # Control the frame rate

music_playing = False

def toggle_music():
    global music_playing
    pygame.init()
    pygame.mixer.init()
    if not music_playing:
        pygame.mixer.music.load("resources/BG MUSIC.mp3")
        pygame.mixer.music.set_volume(0.25)  # Set volume to 50%
        pygame.mixer.music.play(-1)
    else:
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()
        else:
            pygame.mixer.music.unpause()

    music_playing = not music_playing

def main_menu():
    # Initialize pygame
    pygame.init()
    main()
    # Other initialization code
    running = True

    # Calculate horizontal center
    screen_center_x = screen.get_width() // 2

    # Define button positions
    button_y = 400  # Adjust as needed
    button_spacing = 20  # Adjust as needed

    # Define top text position
    top_text_y = 100  # Adjust as needed

    while running:
        screen.blit(background, (0, 0))
        MENU_MOUSE_POS = pygame.mouse.get_pos()

        # Define button positions centered horizontally
        button_width = playgame_img.get_width()  # Assuming playgame_img is loaded
        button_start_x = screen_center_x - button_width // 2
        button_offset = button_width + button_spacing

        # Render the text "Select game mode"
        text_surface = get_font(50, 3).render("Select Game Mode", True, (247, 197, 102))  # F7C566 color

        # Calculate the position of the text to be at the top center of the screen
        text_x = screen_center_x - text_surface.get_width() // 2

        # Blit the text onto the screen
        screen.blit(text_surface, (text_x, top_text_y))
        music_button_x = screen_width - music_img.get_width() - 20  # Adjusted to not overlap with controls button
        music_button_y = screen_height - music_img.get_height() - 70
        PLAY_BUTTON = Button(image=playgame_img, pos=(button_start_x, button_y),
                             text_input="", font=get_font(68, 1), base_color="#D32735", hovering_color=RED)
        SOLVER_BUTTON = Button(image=solver_img, pos=(button_start_x + button_offset, button_y),
                               text_input="", font=get_font(68, 1), base_color="#D32735", hovering_color=RED)
        CONTROLS_BUTTON = Button(image=controls_img, pos=(screen.get_width() - controls_img.get_width() - 20, screen.get_height() - controls_img.get_height() - 20),
                                 text_input="", font=get_font(68, 1), base_color="#D32735", hovering_color=RED)
        BACK_BUTTON = Button(image=back_img, pos=(screen.get_width() - back_img.get_width() + 10, 50),  # Adjusted x-coordinate
                             text_input="", font=get_font(68, 1), base_color="#D32735", hovering_color=RED)
        if music_playing:
            MUSIC_BUTTON = Button(image=music_img, pos=(music_button_x, music_button_y),
                                  text_input="", font=get_font(68, 1), base_color="#D32735", hovering_color=RED)
        else:
            MUSIC_BUTTON = Button(image=mute_img, pos=(music_button_x, music_button_y),
                                  text_input="", font=get_font(68, 1), base_color="#D32735", hovering_color=RED)

        for button in [PLAY_BUTTON, SOLVER_BUTTON, CONTROLS_BUTTON, BACK_BUTTON, MUSIC_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    press_sound.play()
                    select_grid_size(True)
                    select_operations()
                    select_difficulty()
                    start_game()
                    pass
                if SOLVER_BUTTON.checkForInput(MENU_MOUSE_POS):
                    press_sound.play()
                    select_grid_size(False)
                    solve_puzzle()  # Solve the puzzle directly
                if CONTROLS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    press_sound.play()
                    controls()
                if BACK_BUTTON.checkForInput(MENU_MOUSE_POS):
                    press_sound.play()
                    main_menu()
                if MUSIC_BUTTON.checkForInput(MENU_MOUSE_POS):
                    press_sound.play()
                    toggle_music()  # Call the toggle_music function when music button is clicked

        pygame.display.update()



def controls():
    # Controls screen code
    controls_bg = pygame.image.load("resources/CONTROLS.png")
    screen.blit(controls_bg, (0, 0))

    while True:
        CONTROLS_MOUSE = pygame.mouse.get_pos()
        BACK_BUTTON = Button(image=back_img, pos=(1160, 650),
                             text_input="", font=get_font(50, 1), base_color="#D32735", hovering_color=RED)

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
def solve_puzzle():
        pygame.display.flip()



# play_intro_video()
toggle_music()  # Call toggle_music() before displaying the main menu
main_menu()