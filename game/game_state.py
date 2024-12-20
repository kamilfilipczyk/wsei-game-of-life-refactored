import numpy as np

# SINGLETON PATTERN BODY

class GameState:
    _instance = None

    def __new__(cls, n_cells_x, n_cells_y):
        if cls._instance is None:
            cls._instance = super(GameState, cls).__new__(cls)
            cls._instance.state = np.random.choice([0, 1], size=(n_cells_x, n_cells_y), p=[0.8, 0.2])
        return cls._instance

    def update(self, x, y, value):
        """Update the state at position (x, y)."""
        self.state[x, y] = value

    def get_state(self):
        """Return the current game state."""
        return self.state

    def next_generation(self):
        """Create the next generation."""
        new_state = np.copy(self.state)
        for y in range(self.state.shape[1]):
            for x in range(self.state.shape[0]):
                n_neighbors = self._count_neighbors(x, y)
                if self.state[x, y] == 1 and (n_neighbors < 2 or n_neighbors > 3):
                    new_state[x, y] = 0
                elif self.state[x, y] == 0 and n_neighbors == 3:
                    new_state[x, y] = 1
        self.state = new_state

    def _count_neighbors(self, x, y):
        """Count neighbors for a cell at (x, y)."""
        return sum(self.state[(x + dx) % self.state.shape[0], (y + dy) % self.state.shape[1]]
                   for dx in [-1, 0, 1] for dy in [-1, 0, 1] if (dx, dy) != (0, 0))
