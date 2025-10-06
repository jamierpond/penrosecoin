import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class TileParams:
    """Parameters for Penrose tiling"""
    scale: float = 1.0
    margin: float = 0.00  # Gap between tiles
    green_color: str = '#00A000'
    red_color: str = '#D00000'
    purple_color: str = '#8800FF'
    background_color: str = '#FFFFFF'
    edge_color: str = '#DDDDDD'
    edge_width: float = 0.0


def get_rhombus_vertices(
    center: Tuple[float, float],
    angle: float,
    acute_angle: float,
    height: float = 1.0
) -> np.ndarray:
    """Calculate vertices for a rhombus with specified acute angle"""
    edge_length = 1.0

    # Half-diagonal from center to obtuse vertex
    d1 = edge_length * np.cos(np.radians(acute_angle / 2))
    # Half-diagonal from center to acute vertex
    d2 = edge_length * np.sin(np.radians(acute_angle / 2))

    # Canonical rhombus with long diagonal on x-axis
    vertices = np.array([
        [d1, 0],      # Right (obtuse)
        [0, d2],      # Top (acute)
        [-d1, 0],     # Left (obtuse)
        [0, -d2],     # Bottom (acute)
    ])

    # Rotate
    angle_rad = np.radians(angle)
    rotation = np.array([
        [np.cos(angle_rad), -np.sin(angle_rad)],
        [np.sin(angle_rad), np.cos(angle_rad)]
    ])
    vertices = vertices @ rotation.T

    # Calculate actual height after rotation
    actual_height = vertices[:, 1].max() - vertices[:, 1].min()
    height_scale = height / actual_height
    vertices *= height_scale

    # Translate
    vertices += np.array(center)

    return vertices


def get_tile_vertices(
    center: Tuple[float, float],
    angle: float,
) -> np.ndarray:
    """Calculate vertices for a Penrose tile (fat rhombus with 72° acute angles)"""
    return get_rhombus_vertices(center, angle, 72)


def create_tile_polygon(
    tile_type: str,
    center: Tuple[float, float],
    angle: float,
    params: TileParams
) -> Polygon:
    """Create a matplotlib Polygon for a Penrose tile"""
    vertices = get_tile_vertices(center, angle)

    # Apply margin by shrinking towards centroid
    if params.margin > 0:
        centroid = vertices.mean(axis=0)
        vertices = centroid + (vertices - centroid) * (1 - params.margin)

    # Scale
    vertices *= params.scale

    color_map = {
        'green': params.green_color,
        'red': params.red_color,
        'purple': params.purple_color,
    }
    color = color_map.get(tile_type, '#000000')
    return Polygon(
        vertices,
        facecolor=color,
        edgecolor=params.edge_color,
        linewidth=params.edge_width
    )


class PenroseCoin:
    """Generate Penrose tiling pattern for a coin"""

    def __init__(self, params: TileParams | None = None):
        self.params = params or TileParams()
        self.tiles: List[Tuple[str, Tuple[float, float], float]] = []

    def add_tile(self, tile_type: str, center: Tuple[float, float], angle: float):
        """Add a tile to the coin"""
        self.tiles.append((tile_type, center, angle))

    def create_pattern(self):
        """Creates a single tile"""
        self.tiles = []

        # Draw one green tile at the origin with 0 rotation
        self.add_tile('green', (0, 0), np.radians(18))


    def plot(self, figsize: Tuple[int, int] = (10, 10), show_grid: bool = False):
        """Plot the coin design"""
        fig, ax = plt.subplots(figsize=figsize)

        # Draw tiles
        for tile_type, center, angle in self.tiles:
            polygon = create_tile_polygon(tile_type, center, angle, self.params)
            ax.add_patch(polygon)

        # Set aspect and limits - auto-scale based on tiles
        all_vertices = []
        for tile_type, center, angle in self.tiles:
            vertices = get_tile_vertices(center, angle)
            vertices *= self.params.scale
            all_vertices.extend(vertices)
        if all_vertices:
            vertices_array = np.array(all_vertices)
            max_coord = np.max(np.abs(vertices_array)) * 1.1
            ax.set_xlim(-max_coord, max_coord)
            ax.set_ylim(-max_coord, max_coord)

        ax.set_aspect('equal')

        if show_grid:
            ax.grid(True, alpha=0.3)
        else:
            ax.axis('off')

        plt.title('Penrose Pattern Coin Design', fontsize=16, pad=20)
        plt.tight_layout()

        return fig, ax


# Example usage
if __name__ == "__main__":
    # Create coin with custom parameters
    params = TileParams(
        scale=0.3,
        margin=0.00,
        edge_color='#000000',
        edge_width=0.0
    )

    coin = PenroseCoin(params)

    # Create the exact pattern from the image
    coin.create_pattern()

    # Plot and show
    fig, ax = coin.plot(figsize=(12, 12), show_grid=False)
    plt.savefig('penrose_coin.png', dpi=300, bbox_inches='tight', facecolor=params.background_color)
    plt.show()

    print("Coin design saved to 'penrose_coin.png'")
    print(f"Number of tiles: {len(coin.tiles)}")
