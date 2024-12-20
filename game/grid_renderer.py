import pygame

# OBSERVER PATTERN BODY

class GridRenderer:
    def __init__(self, game_state, screen, cell_width, cell_height, black, white):
        self.game_state = game_state
        self.screen = screen
        self.cell_width = cell_width
        self.cell_height = cell_height
        self.black = black
        self.white = white

    def render(self):
        """Draw the current game state."""
        for y in range(self.game_state.get_state().shape[1]):
            for x in range(self.game_state.get_state().shape[0]):
                cell = pygame.Rect(x * self.cell_width, y * self.cell_height, self.cell_width, self.cell_height)
                if self.game_state.get_state()[x, y] == 1:
                    pygame.draw.rect(self.screen, self.black, cell)
                else:
                    pygame.draw.rect(self.screen, self.white, cell)
