import tkinter as tk

class DangerAlertFeature:
    name = "Danger Alerts (Beep)"
    
    def __init__(self, game):
        self.game = game
        self.enabled_var = tk.BooleanVar(value=False)

    def on_tick(self):
        if self.enabled_var.get() and self.game.is_alive:
            if (self.game.hunger < 30 or 
                self.game.energy < 30 or 
                self.game.hygiene < 30 or 
                self.game.happiness < 30):
                self.game.root.bell()
