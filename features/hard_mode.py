import tkinter as tk

class HardModeFeature:
    name = "Hard Mode (2x Decay)"
    
    def __init__(self, game):
        self.game = game
        self.enabled_var = tk.BooleanVar(value=False)

    def on_tick(self):
        # If enabled, decrease stats an extra time (effectively doubling the decay)
        if self.enabled_var.get() and self.game.is_alive:
            if self.game.is_sleeping:
                self.game.hunger = max(0, self.game.hunger - 1)
                self.game.hygiene = max(0, self.game.hygiene - 1)
            else:
                self.game.hunger = max(0, self.game.hunger - 4)
                self.game.happiness = max(0, self.game.happiness - 3)
                self.game.energy = max(0, self.game.energy - 2)
                self.game.hygiene = max(0, self.game.hygiene - 3)
