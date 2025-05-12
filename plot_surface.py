import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def plot_volatility_surface(grid_x, grid_y, surface):
    """Plot 3D volatility surface."""
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(grid_x, grid_y, surface, cmap='viridis')
    ax.set_xlabel('Strike')
    ax.set_ylabel('Expiration')
    ax.set_zlabel('Implied Volatility')
    plt.show()
