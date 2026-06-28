import tkinter as tk
from tkinter import messagebox
import importlib

class TamagotchiGame:
    def __init__(self, root):
        self.root = root # Main window of the app
        self.root.title("Catagotchi")
        
        # --- DEFAULT GEOMETRY ---
        self.root.geometry("350x500")
        
        # --- PET STATS ---
        # Range 0-100
        self.hunger = 100
        self.happiness = 100
        self.energy = 100
        self.hygiene = 100
        
        # Game state variables
        self.is_alive = True
        self.is_sleeping = False

        # --- FALLBACK ASSETS (EMOJIS) ---
        self.asset_happy = "😸"
        self.asset_sad = "😿"
        self.asset_sleeping = "😴"
        self.asset_dirty = "🤢"
        self.asset_hungry = "🤤"
        self.asset_dead = "💀"

        # --- LOAD IMAGE ASSETS ---
        try:
            self.img_happy = tk.PhotoImage(file="assets/happy.png")
            self.img_sad = tk.PhotoImage(file="assets/sad.png")
            self.img_sleeping = tk.PhotoImage(file="assets/sleeping.png")
            self.img_dirty = tk.PhotoImage(file="assets/dirty.png")
            self.img_hungry = tk.PhotoImage(file="assets/hungry.png")
            self.img_dead = tk.PhotoImage(file="assets/dead.png")
            self.use_images = True
        except Exception as e:
            print(f"Failed to load image assets, using emojis as fallback: {e}")
            self.use_images = False

        # --- CREATING GUI ELEMENTS ---
        
        # Title Label
        self.title_label = tk.Label(root, text="Catagotchi", font=("Montserrat", 16))
        self.title_label.pack(pady=10)

        # Pet Display Label
        if self.use_images:
            self.pet_label = tk.Label(root, image=self.img_happy)
        else:
            self.pet_label = tk.Label(root, text=self.asset_happy, font=("Montserrat", 72))
        self.pet_label.pack(pady=10)

        # Status Message Label
        self.status_msg_label = tk.Label(root, text="Your pet is happy and healthy!", font=("Montserrat", 11), fg="blue")
        self.status_msg_label.pack(pady=5)

        # Stats Display Frame
        self.stats_frame = tk.Frame(root)
        self.stats_frame.pack(pady=10)

        self.hunger_label = tk.Label(self.stats_frame, text=f"Hunger: {self.hunger}/100", font=("Montserrat", 10))
        self.hunger_label.grid(row=0, column=0, padx=15, pady=2)

        self.happiness_label = tk.Label(self.stats_frame, text=f"Happiness: {self.happiness}/100", font=("Montserrat", 10))
        self.happiness_label.grid(row=0, column=1, padx=15, pady=2)

        self.energy_label = tk.Label(self.stats_frame, text=f"Energy: {self.energy}/100", font=("Montserrat", 10))
        self.energy_label.grid(row=1, column=0, padx=15, pady=2)

        self.hygiene_label = tk.Label(self.stats_frame, text=f"Hygiene: {self.hygiene}/100", font=("Montserrat", 10))
        self.hygiene_label.grid(row=1, column=1, padx=15, pady=2)

        # Action Buttons Frame
        self.buttons_frame = tk.Frame(root)
        self.buttons_frame.pack(pady=15)

        # Interaction Buttons
        self.feed_button = tk.Button(self.buttons_frame, text="Feed Pet", width=12, height=2, command=self.feed_pet)
        self.feed_button.grid(row=0, column=0, padx=5, pady=5)

        self.play_button = tk.Button(self.buttons_frame, text="Play Game", width=12, height=2, command=self.play_with_pet)
        self.play_button.grid(row=0, column=1, padx=5, pady=5)

        self.sleep_button = tk.Button(self.buttons_frame, text="Go to Sleep", width=12, height=2, command=self.toggle_sleep)
        self.sleep_button.grid(row=1, column=0, padx=5, pady=5)

        self.clean_button = tk.Button(self.buttons_frame, text="Clean Pet", width=12, height=2, command=self.clean_pet)
        self.clean_button.grid(row=1, column=1, padx=5, pady=5)

        # --- REGISTER LIFECYCLE HOOKS ---
        self.on_tick_hooks = []

        # --- DYNAMICALLY LOAD OPTIONAL MODULES ---
        for module_name in ["features", "theme"]:
            try:
                module = importlib.import_module(module_name)
                if hasattr(module, "register"):
                    module.register(self)
            except ImportError:
                pass

        # --- START GAME LOOP ---
        # Triggers the passive decay of stats over time
        self.game_loop()

    # --- ACTION FUNCTIONS ---

    def feed_pet(self):
        # Cannot feed a pet that is sleeping or dead
        if not self.is_alive or self.is_sleeping:
            return
        
        # Increase hunger (making it more full), capping it at 100
        self.hunger = self.hunger + 25
        if self.hunger > 100:
            self.hunger = 100
            
        # Eating food makes the pet slightly dirty
        self.hygiene = self.hygiene - 4
        if self.hygiene < 0:
            self.hygiene = 0

        self.status_msg_label.config(text="Yum! Your pet enjoyed the food.")
        self.update_gui()

    def play_with_pet(self):
        if not self.is_alive or self.is_sleeping:
            return

        # Make sure the pet has enough energy to play first
        if self.energy < 15:
            self.status_msg_label.config(text="Oops! Your pet is too tired to play!")
            return

        # Play increases happiness but decreases energy
        self.happiness = self.happiness + 20
        if self.happiness > 100:
            self.happiness = 100

        self.energy = self.energy - 15
        if self.energy < 0:
            self.energy = 0

        self.status_msg_label.config(text="Yay! That was a fun game!")
        self.update_gui()

    def toggle_sleep(self):
        if not self.is_alive:
            return

        # Change state and update button label text dynamically
        if self.is_sleeping:
            self.is_sleeping = False
            self.sleep_button.config(text="Go to Sleep")
            self.status_msg_label.config(text="Your pet woke up refreshed!")
        else:
            self.is_sleeping = True
            self.sleep_button.config(text="Wake Up")
            self.status_msg_label.config(text="Shhh... Your pet is sleeping.")

        self.update_gui()

    def clean_pet(self):
        if not self.is_alive or self.is_sleeping:
            return

        # Fully restores hygiene
        self.hygiene = 100
        self.status_msg_label.config(text="Your pet is sparkling clean!")
        self.update_gui()

    # --- GAME ENGINE & TIMERS ---

    def game_loop(self):
        # If the pet has died, stop running the loops
        if not self.is_alive:
            return

        # Stats slowly go down over time
        if self.is_sleeping:
            # Energy recovers, but hunger and hygiene decline slowly
            self.energy = self.energy + 10
            if self.energy > 100:
                self.energy = 100
            
            self.hunger = self.hunger - 1
            self.hygiene = self.hygiene - 1
        else:
            # Normal awake decay rates
            self.hunger = self.hunger - 4
            self.happiness = self.happiness - 3
            self.energy = self.energy - 2
            self.hygiene = self.hygiene - 3

        # Clamp stats to ensure they don't go below 0
        if self.hunger < 0: self.hunger = 0
        if self.happiness < 0: self.happiness = 0
        if self.energy < 0: self.energy = 0
        if self.hygiene < 0: self.hygiene = 0

        # Run custom tick hooks (e.g. features, theme updates)
        for hook in self.on_tick_hooks:
            hook(self)

        # Clamp stats again in case features modified them
        if self.hunger < 0: self.hunger = 0
        if self.happiness < 0: self.happiness = 0
        if self.energy < 0: self.energy = 0
        if self.hygiene < 0: self.hygiene = 0

        # Check for loss conditions
        if self.hunger <= 0 or self.energy <= 0 or self.hygiene <= 0:
            self.is_alive = False
            self.set_pet_display(self.asset_dead, self.img_dead)
            self.status_msg_label.config(text="Oh no! Your pet has died.")
            self.update_gui()
            self.disable_all_buttons()
            self.root.update_idletasks()
            if messagebox.askyesno("Game Over", "Your pet has passed away! Would you like to restart?"):
                self.restart_game()
            return

        # Update the pet's face/asset and stats display
        self.update_pet_appearance()
        self.update_gui()

        # Run this function again after 3000 milliseconds (3 seconds)
        self.root.after(3000, self.game_loop)

    def set_pet_display(self, emoji, image):
        if self.use_images:
            self.pet_label.config(image=image)
        else:
            self.pet_label.config(text=emoji)

    def update_pet_appearance(self):
        # Decide which visual asset to show
        if self.is_sleeping:
            self.set_pet_display(self.asset_sleeping, self.img_sleeping)
        elif self.hunger < 30:
            self.set_pet_display(self.asset_hungry, self.img_hungry)
            self.status_msg_label.config(text="Your pet is starving!")
        elif self.hygiene < 30:
            self.set_pet_display(self.asset_dirty, self.img_dirty)
            self.status_msg_label.config(text="Your pet is dirty!")
        elif self.happiness < 30:
            self.set_pet_display(self.asset_sad, self.img_sad)
            self.status_msg_label.config(text="Your pet feels lonely.")
        else:
            self.set_pet_display(self.asset_happy, self.img_happy)

    def update_gui(self):
        # Refreshes the numbers displayed on screen
        self.hunger_label.config(text=f"Hunger: {self.hunger}/100")
        self.happiness_label.config(text=f"Happiness: {self.happiness}/100")
        self.energy_label.config(text=f"Energy: {self.energy}/100")
        self.hygiene_label.config(text=f"Hygiene: {self.hygiene}/100")

    def disable_all_buttons(self):
        # Disables all buttons when the game is over
        self.feed_button.config(state="disabled")
        self.play_button.config(state="disabled")
        self.sleep_button.config(state="disabled")
        self.clean_button.config(state="disabled")

    def enable_all_buttons(self):
        # Enables all buttons when the game restarts
        self.feed_button.config(state="normal")
        self.play_button.config(state="normal")
        self.sleep_button.config(state="normal")
        self.clean_button.config(state="normal")

    def restart_game(self):
        # Reset stats
        self.hunger = 100
        self.happiness = 100
        self.energy = 100
        self.hygiene = 100
        
        # Reset states
        self.is_alive = True
        self.is_sleeping = False
        
        # Reset GUI labels
        self.sleep_button.config(text="Go to Sleep")
        self.status_msg_label.config(text="Your pet is happy and healthy!")
        
        # Re-enable buttons and update UI
        self.enable_all_buttons()
        self.update_pet_appearance()
        self.update_gui()
        
        # Restart game loop
        self.game_loop()


# --- INITIALIZE AND START ---
if __name__ == "__main__":
    root = tk.Tk() # Create the main window
    app = TamagotchiGame(root) # Create the game instance
    root.mainloop() # Start the GUI event loop