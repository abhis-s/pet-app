import sys
import tkinter as tk

class RecommendationsFeature:
    name = "Recommendations"
    
    def __init__(self, game):
        self.game = game
        self.enabled_var = tk.BooleanVar(value=False)
        # Keep track of which buttons are currently highlighted
        self.highlighted_buttons = set()

        # Cache default colors for macOS and general restoration
        self.default_active_fg = game.feed_button.cget("activeforeground")
        self.default_active_bg = game.feed_button.cget("activebackground")
        self.original_fgs = {
            game.feed_button: game.feed_button.cget("fg"),
            game.play_button: game.play_button.cget("fg"),
            game.sleep_button: game.sleep_button.cget("fg"),
            game.clean_button: game.clean_button.cget("fg")
        }

    def on_tick(self):
        try:
            import theme
        except ImportError:
            theme = None

        if theme and hasattr(self.game, "current_applied_theme") and self.game.current_applied_theme in theme.THEME_COLORS:
            colors = theme.THEME_COLORS[self.game.current_applied_theme]
            normal_bg = colors["button_bg"]
            normal_fg = colors["button_fg"]
            normal_highlight = colors["bg"]
            normal_active_bg = colors["button_bg"]
            normal_active_fg = colors["button_fg"]
        else:
            normal_bg = "SystemButtonFace"
            normal_fg = "SystemButtonText"
            normal_highlight = self.game.root.cget("bg")
            normal_active_bg = self.default_active_bg
            normal_active_fg = self.default_active_fg

        is_mac = sys.platform == "darwin"

        # Map buttons to their concerned stats
        other_stats_low = (
            self.game.hunger < 30 or
            self.game.happiness < 30 or
            self.game.hygiene < 30
        )
        recommend_wake_up = self.game.is_sleeping and (self.game.energy >= 100 or other_stats_low)

        recommendations = {
            self.game.feed_button: self.game.hunger < 30 and not self.game.is_sleeping,
            self.game.play_button: self.game.happiness < 30 and not self.game.is_sleeping,
            self.game.sleep_button: (self.game.energy < 30 and not self.game.is_sleeping) or recommend_wake_up,
            self.game.clean_button: self.game.hygiene < 30 and not self.game.is_sleeping
        }

        for btn, is_low in recommendations.items():
            if self.enabled_var.get() and self.game.is_alive and is_low:
                # Highlight the button
                if is_mac:
                    btn.config(fg="red", activeforeground="red", highlightbackground="yellow")
                else:
                    btn.config(bg="yellow", fg="red", activebackground="yellow", activeforeground="red")
                self.highlighted_buttons.add(btn)
            else:
                # Restore the button if it was highlighted
                if btn in self.highlighted_buttons:
                    if is_mac:
                        btn.config(
                            fg=self.original_fgs[btn],
                            activeforeground=self.default_active_fg,
                            activebackground=self.default_active_bg,
                            highlightbackground=normal_highlight
                        )
                    else:
                        btn.config(
                            bg=normal_bg,
                            fg=normal_fg,
                            activebackground=normal_active_bg,
                            activeforeground=normal_active_fg,
                            highlightbackground=normal_highlight
                        )
                    self.highlighted_buttons.discard(btn)
