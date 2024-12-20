import pygame
from game.game_state import GameState                 # Singleton pattern - ensures that only one instance of the game state is used across the simulation
from game.grid_renderer import GridRenderer           # Observer pattern - tracks changes in the GameState and update the rendering 
from game.commands import SaveCommand, LoadCommand    # Command pattern - encapsulates the save/load actions for the code readability

# Singleton use explanation - in this app, we only need one, global instance of game state. Multiple instances could cause problems with synchronization
# (of course this application is rather small, but still it's considered a good practice to use this pattern)

# Observer use explanation - the main cause of implementing observer was to separate game state management and rendering it on the screen. It is crucial because now we can
# modify rendering without affecting the game state. Again it would appear more obvious in larger simulators, but considering this project can grow in the future it's a
# good foundation to work on

# Command use explanation - like before, a need for decoupling saving and loading from main logic. Each command can be executed independently and can be modified separately

# Screen dimensions
width, height = 800, 600
n_cells_x, n_cells_y = 40, 30
cell_width = width // n_cells_x
cell_height = height // n_cells_y

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# Save file path
SAVE_FILE = "assets/save_data.npy"

# Initialize game components
pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Game of Life")

game_state = GameState(n_cells_x, n_cells_y)
grid_renderer = GridRenderer(game_state, screen, cell_width, cell_height, BLACK, WHITE)
save_command = SaveCommand(game_state, SAVE_FILE)
load_command = LoadCommand(game_state, SAVE_FILE)

# Game state flags
running = True
is_running = False  # Pause/Resume flag

# Fonts
font = pygame.font.Font(None, 36)

def draw_button(text, x, y, width, height, color, text_color):
    """Helper function to draw buttons."""
    pygame.draw.rect(screen, color, (x, y, width, height))
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(text_surface, text_rect)

# Button positions
button_width, button_height = 150, 40
pause_button = pygame.Rect(10, height - 50, button_width, button_height)
save_button = pygame.Rect(170, height - 50, button_width, button_height)
load_button = pygame.Rect(330, height - 50, button_width, button_height)

# Main loop
clock = pygame.time.Clock()
while running:
    screen.fill(WHITE)

    # Render grid and game state
    grid_renderer.render()

    # Render buttons
    draw_button("Pause" if is_running else "Resume", pause_button.x, pause_button.y, pause_button.width, pause_button.height, GREEN, BLACK)
    draw_button("Save", save_button.x, save_button.y, save_button.width, save_button.height, GREEN, BLACK)
    draw_button("Load", load_button.x, load_button.y, load_button.width, load_button.height, GREEN, BLACK)

    pygame.display.flip()

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if pause_button.collidepoint(event.pos):
                is_running = not is_running  # Toggle pause/resume
            elif save_button.collidepoint(event.pos):
                save_command.execute()  # Save game state
            elif load_button.collidepoint(event.pos):
                load_command.execute()  # Load game state
            else:
                # Toggle cell state on click
                x, y = event.pos[0] // cell_width, event.pos[1] // cell_height
                game_state.update(x, y, not game_state.get_state()[x, y])

    # Game logic
    if is_running:
        game_state.next_generation()
        clock.tick(10)  # Control the tick rate when the game is running
    else:
        clock.tick(30)  # Smooth rendering while paused

pygame.quit()
