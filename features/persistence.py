import json
import os
import tkinter as tk

class PersistenceFeature:
    name = "Auto-Save State"
    SAVE_FILE = "pet_state.json"
    
    def __init__(self, game):
        self.game = game
        self.enabled_var = tk.BooleanVar(value=True)
        # Load the saved state immediately upon initialization
        self.load_state()

    def on_tick(self):
        # Save state if enabled
        if self.enabled_var.get():
            state = {
                "hunger": self.game.hunger,
                "happiness": self.game.happiness,
                "energy": self.game.energy,
                "hygiene": self.game.hygiene,
                "is_sleeping": self.game.is_sleeping,
                "is_alive": self.game.is_alive
            }
            try:
                with open(self.SAVE_FILE, "w") as f:
                    json.dump(state, f)
            except Exception as e:
                print(f"Failed to auto-save state: {e}")

    def load_state(self):
        if os.path.exists(self.SAVE_FILE):
            try:
                with open(self.SAVE_FILE, "r") as f:
                    state = json.load(f)
                    self.game.hunger = state.get("hunger", 100)
                    self.game.happiness = state.get("happiness", 100)
                    self.game.energy = state.get("energy", 100)
                    self.game.hygiene = state.get("hygiene", 100)
                    self.game.is_sleeping = state.get("is_sleeping", False)
                    self.game.is_alive = state.get("is_alive", True)
                    
                    # Update buttons and labels to match the loaded sleeping state
                    if self.game.is_sleeping:
                        self.game.sleep_button.config(text="Wake Up")
                        self.game.status_msg_label.config(text="Shhh... The pet is sleeping.")
                    else:
                        self.game.sleep_button.config(text="Go to Sleep")
                        
                    # If loaded as dead, disable controls
                    if not self.game.is_alive:
                        self.game.disable_all_buttons()
                        self.game.status_msg_label.config(text="Oh no! Your pet has died.")

                    # Update GUI and pet appearance immediately
                    self.game.update_gui()
                    self.game.update_pet_appearance()
            except Exception as e:
                print(f"Failed to load state: {e}")
