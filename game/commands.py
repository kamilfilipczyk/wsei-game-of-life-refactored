import os
import numpy as np

# COMMAND PATTERN BODY

class SaveCommand:
    def __init__(self, game_state, filename):
        self.game_state = game_state
        self.filename = filename

    def execute(self):
        np.save(self.filename, self.game_state.get_state())
        print("Game state saved.")

class LoadCommand:
    def __init__(self, game_state, filename):
        self.game_state = game_state
        self.filename = filename

    def execute(self):
        if os.path.exists(self.filename):
            self.game_state.state = np.load(self.filename)
            print("Game state loaded.")
        else:
            print("No saved state found.")
