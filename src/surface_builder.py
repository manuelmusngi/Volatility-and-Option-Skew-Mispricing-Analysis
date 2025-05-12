import numpy as np
from scipy.interpolate import griddata

def build_volatility_surface(strikes, expirations, volatilities):
    """Build implied volatility surface."""
    grid_x, grid_y = np.meshgrid(
        np.linspace(min(strikes), max(strikes), 100),
        np.linspace(min(expirations), max(expirations), 100)
    )
    surface = griddata((strikes, expirations), volatilities, (grid_x, grid_y), method='cubic')
    return grid_x, grid_y, surface
