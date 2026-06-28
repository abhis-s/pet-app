import tkinter as tk
from .hard_mode import HardModeFeature
from .danger_alert import DangerAlertFeature
from .recommendations import RecommendationsFeature

from .persistence import PersistenceFeature

# List of active features to load.
# To add or remove features modularly, simply update this list.
ACTIVE_FEATURES = [
    HardModeFeature,
    DangerAlertFeature,
    RecommendationsFeature,
    PersistenceFeature
]

def register(game):
    """Registers features module on the game instance."""
    # Instantiate active features
    game.features = [FeatureClass(game) for FeatureClass in ACTIVE_FEATURES]
    
    if game.features:
        # Resize window for features
        game.root.geometry("350x550")
        
        # Build UI for optional features
        game.options_frame = tk.LabelFrame(game.root, text="Optional Features", padx=10, pady=5)
        game.options_frame.pack(pady=10)
        
        game.feature_checks = []
        for i, feature in enumerate(game.features):
            chk = tk.Checkbutton(game.options_frame, text=feature.name, variable=feature.enabled_var)
            chk.grid(row=i // 2, column=i % 2, padx=5, pady=2, sticky="w")
            game.feature_checks.append(chk)
            
        # Hook on tick
        game.on_tick_hooks.append(run_features)

        # Force theme re-application to style the newly created options frame
        if hasattr(game, "current_applied_theme"):
            game.current_applied_theme = None
            try:
                import theme
                theme.apply_theme(game)
            except ImportError:
                pass
    else:
        game.root.geometry("350x480")

def run_features(game):
    for feature in game.features:
        feature.on_tick()
