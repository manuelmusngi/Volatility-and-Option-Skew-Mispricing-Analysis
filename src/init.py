"""
Volatility and Option Skew Mispricing Analysis

This package provides tools for fetching financial data, calculating option prices using the Black-Scholes model,
modeling volatility with GARCH, constructing volatility surfaces, and visualizing option skew and volatility surfaces.

Modules:
- fetch_data: Fetch historical asset and option chain data.
- bs_model: Black-Scholes pricing and Greeks.
- garch_model: Volatility modeling with GARCH.
- surface_builder: Construct implied volatility surfaces.
- plot_surface: Visualize volatility surfaces.

Example usage:
    from src import fetch_data, bs_model, garch_model, surface_builder, plot_surface
"""

# Enable package-level imports for convenience
from .fetch_data import *
from .bs_model import *
from .garch_model import *
from .surface_builder import *
from .plot_surface import *
