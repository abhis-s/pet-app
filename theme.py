import sys
import subprocess
import tkinter as tk

THEME_COLORS = {
    "light": {
        "bg": "#f0f0f0",
        "fg": "#000000",
        "status_fg": "#0000ff",
        "button_bg": "#e1e1e1",
        "button_fg": "#000000"
    },
    "dark": {
        "bg": "#1e1e1e",
        "fg": "#ffffff",
        "status_fg": "#4fc3f7",
        "button_bg": "#333333",
        "button_fg": "#ffffff"
    }
}

def get_system_theme():
    """Detects the system theme (dark or light) on macOS and Windows."""
    if sys.platform == "darwin":
        try:
            result = subprocess.run(
                ["defaults", "read", "-g", "AppleInterfaceStyle"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=1
            )
            if "Dark" in result.stdout:
                return "dark"
        except Exception:
            pass
    elif sys.platform == "win32":
        try:
            import winreg
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize")
            value, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
            if value == 0:
                return "dark"
        except Exception:
            pass
    return "light"

def apply_theme(game):
    """Applies the selected theme (or auto theme) to all GUI elements of the game."""
    theme = game.theme_var.get().lower()
    if theme == "auto":
        theme = get_system_theme()
    
    if theme == game.current_applied_theme:
        return
    
    game.current_applied_theme = theme
    colors = THEME_COLORS[theme]
    
    # Apply to root window
    game.root.config(bg=colors["bg"])
    
    # Apply to frames
    game.stats_frame.config(bg=colors["bg"])
    game.buttons_frame.config(bg=colors["bg"])
    game.theme_frame.config(bg=colors["bg"])
    
    # Apply to labels
    game.title_label.config(bg=colors["bg"], fg=colors["fg"])
    game.pet_label.config(bg=colors["bg"], fg=colors["fg"])
    game.status_msg_label.config(bg=colors["bg"], fg=colors["status_fg"])
    game.hunger_label.config(bg=colors["bg"], fg=colors["fg"])
    game.happiness_label.config(bg=colors["bg"], fg=colors["fg"])
    game.energy_label.config(bg=colors["bg"], fg=colors["fg"])
    game.hygiene_label.config(bg=colors["bg"], fg=colors["fg"])
    game.theme_label.config(bg=colors["bg"], fg=colors["fg"])
    
    # Apply to buttons
    is_mac = sys.platform == "darwin"
    for btn in [game.feed_button, game.play_button, game.sleep_button, game.clean_button]:
        if is_mac:
            btn.config(highlightbackground=colors["bg"])
        else:
            btn.config(
                bg=colors["button_bg"],
                fg=colors["button_fg"],
                activebackground=colors["button_bg"],
                activeforeground=colors["button_fg"],
                highlightbackground=colors["bg"]
            )
            
    # Apply to OptionMenu
    if is_mac:
        game.theme_menu.config(highlightbackground=colors["bg"])
    else:
        game.theme_menu.config(
            bg=colors["bg"],
            fg=colors["fg"],
            activebackground=colors["bg"],
            activeforeground=colors["fg"],
            highlightbackground=colors["bg"]
        )
    game.theme_menu["menu"].config(
        bg=colors["bg"],
        fg=colors["fg"],
        activebackground=colors["button_bg"],
        activeforeground=colors["fg"]
    )

    # Apply to optional features frame and checkboxes if they exist
    if hasattr(game, "options_frame") and game.options_frame.winfo_exists():
        if is_mac:
            game.options_frame.config(bg=colors["bg"], fg=colors["fg"])
            for chk in game.feature_checks:
                chk.config(bg=colors["bg"], fg=colors["fg"])
        else:
            game.options_frame.config(bg=colors["bg"], fg=colors["fg"])
            for chk in game.feature_checks:
                chk.config(
                    bg=colors["bg"],
                    fg=colors["fg"],
                    activebackground=colors["bg"],
                    activeforeground=colors["fg"],
                    selectcolor=colors["bg"]
                )


def register(game):
    """Registers the theme module on the game instance."""
    # Setup theme state
    game.current_applied_theme = None
    
    # Create Theme Selection Frame
    game.theme_frame = tk.Frame(game.root)
    game.theme_frame.pack(pady=10)
    
    game.theme_label = tk.Label(game.theme_frame, text="Theme:", font=("Montserrat", 10))
    game.theme_label.grid(row=0, column=0, padx=5)
    
    game.theme_var = tk.StringVar(value="Auto")
    game.theme_menu = tk.OptionMenu(game.theme_frame, game.theme_var, "Auto", "Light", "Dark", command=lambda _: apply_theme(game))
    game.theme_menu.config(font=("Montserrat", 10))
    game.theme_menu.grid(row=0, column=1)
    
    # Register update hook on tick
    game.on_tick_hooks.append(apply_theme)
    
    # Apply initial theme
    apply_theme(game)


