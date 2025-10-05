import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
from dataclasses import dataclass
from typing import List, Tuple
import math


@dataclass
class TileParams:
    """Parameters for Penrose tiling"""
    scale: float = 1.0
    margin: float = 0.02  # Gap between tiles
    inner_radius: float = 1.5  # Distance from center to inner rhombi
    outer_radius: float = 3.5  # Distance from center to outer rhombi
    kite_color: str = '#00FF00'  # Green (rhombus/kite)
    dart_color: str = '#FF0000'  # Red (dart)
    background_color: str = '#8800FF'  # Purple
    edge_color: str = '#DDDDDD'  # Light gray
    edge_width: float = 2.0


class PenroseTile:
    """Represents a single Penrose tile (kite or dart)"""

    # Golden ratio
    PHI = (1 + np.sqrt(5)) / 2

    def __init__(self, tile_type: str, center: Tuple[float, float],
                 angle: float, params: TileParams):
        """
        tile_type: 'kite' or 'dart'
        center: (x, y) position
        angle: rotation in degrees
        params: TileParams object
        """
        self.tile_type = tile_type
        self.center = np.array(center)
        self.angle = angle
        self.params = params

    def get_vertices(self) -> np.ndarray:
        """Calculate vertices for the tile with margin"""
        # Both rhombi have the same edge length
        edge_length = 1.0

        if self.tile_type == 'kite':
            # Fat rhombus: 72° acute angles, 108° obtuse angles
            # For rhombus with all edges = a and acute angle α:
            # Half-diagonal from center to acute vertex: d1 = a * sin((180-α)/2)
            # Half-diagonal from center to obtuse vertex: d2 = a * sin(α/2)

            acute = 72
            d1 = edge_length * np.sin(np.radians((180 - acute) / 2))  # to obtuse vertices
            d2 = edge_length * np.sin(np.radians(acute / 2))  # to acute vertices

            vertices = np.array([
                [0, d2],           # Top (acute 72°)
                [d1, 0],           # Right (obtuse 108°)
                [0, -d2],          # Bottom (acute 72°)
                [-d1, 0],          # Left (obtuse 108°)
            ])
        else:  # dart
            # Thin rhombus: 36° acute angles, 144° obtuse angles
            # Same edge length as kite, different angles

            acute = 36
            d1 = edge_length * np.sin(np.radians((180 - acute) / 2))  # to obtuse vertices
            d2 = edge_length * np.sin(np.radians(acute / 2))  # to acute vertices

            vertices = np.array([
                [0, d2],           # Top (acute 36°)
                [d1, 0],           # Right (obtuse 144°)
                [0, -d2],          # Bottom (acute 36°)
                [-d1, 0],          # Left (obtuse 144°)
            ])

        # Apply margin by shrinking towards centroid
        if self.params.margin > 0:
            centroid = vertices.mean(axis=0)
            vertices = centroid + (vertices - centroid) * (1 - self.params.margin)

        # Scale
        vertices *= self.params.scale

        # Rotate
        angle_rad = np.radians(self.angle)
        rotation = np.array([
            [np.cos(angle_rad), -np.sin(angle_rad)],
            [np.sin(angle_rad), np.cos(angle_rad)]
        ])
        vertices = vertices @ rotation.T

        # Translate
        vertices += self.center

        return vertices

    def get_polygon(self) -> Polygon:
        """Get matplotlib Polygon object"""
        vertices = self.get_vertices()
        color = self.params.kite_color if self.tile_type == 'kite' else self.params.dart_color
        return Polygon(vertices, facecolor=color, edgecolor=self.params.edge_color,
                      linewidth=self.params.edge_width)


class PenroseCoin:
    """Generate Penrose tiling pattern for a coin"""

    def __init__(self, params: TileParams = None):
        self.params = params or TileParams()
        self.tiles: List[PenroseTile] = []

    def add_tile(self, tile_type: str, center: Tuple[float, float], angle: float):
        """Add a tile to the coin"""
        tile = PenroseTile(tile_type, center, angle, self.params)
        self.tiles.append(tile)
        return tile

    def create_radial_pattern(self):
        """Create exact pattern: 5 fat rhombi (green) + 5 thin rhombi (red) = 10 total
        All tiles meet at center with acute angles pointing inward"""
        self.tiles = []

        angle_step = 72  # 360 / 5

        # 5 fat rhombi (kites/green) - acute angles at center
        for i in range(5):
            angle = i * angle_step
            # Position at center, rotated so acute angle points to center
            self.add_tile('kite', (0, 0), angle + 90)

#         # 5 thin rhombi (darts/red) - acute angles at center, between the fat ones
#         for i in range(5):
#             angle = i * angle_step + angle_step / 2  # Offset by 36°
#             self.add_tile('dart', (0, 0), angle + 90)

    def create_pattern_from_spec(self, tile_specs: List[Tuple[str, Tuple[float, float], float]]):
        """Create pattern from list of (type, center, angle) specifications"""
        self.tiles = []
        for tile_type, center, angle in tile_specs:
            self.add_tile(tile_type, center, angle)

    def plot(self, figsize: Tuple[int, int] = (10, 10),
             show_grid: bool = False, show_background: bool = True):
        """Plot the coin design"""
        fig, ax = plt.subplots(figsize=figsize)

        if show_background:
            ax.set_facecolor(self.params.background_color)

        # Draw tiles
        for tile in self.tiles:
            polygon = tile.get_polygon()
            ax.add_patch(polygon)

        # Set aspect and limits - auto-scale based on tiles
        all_vertices = []
        for tile in self.tiles:
            all_vertices.extend(tile.get_vertices())
        if all_vertices:
            vertices_array = np.array(all_vertices)
            max_coord = np.max(np.abs(vertices_array)) * 1.2
            ax.set_xlim(-max_coord, max_coord)
            ax.set_ylim(-max_coord, max_coord)

        ax.set_aspect('equal')

        if show_grid:
            ax.grid(True, alpha=0.3)
        else:
            ax.axis('off')

        plt.title('Penrose Challenge Coin Design', fontsize=16, pad=20)
        plt.tight_layout()

        return fig, ax


# Example usage
if __name__ == "__main__":
    # Create coin with custom parameters
    params = TileParams(
        scale=1.2,
        margin=0.03,
        inner_radius=1.0,  # Closer together - distance from center to inner rhombi
        outer_radius=2.2,  # Closer together - distance from center to outer rhombi
        kite_color='#00FF00',
        dart_color='#FF0000',
        background_color='#8800FF',
        edge_color='#FFFFFF',
        edge_width=2.5
    )

    coin = PenroseCoin(params)

    # Create the exact pattern: 5 inner + 5 outer fat rhombi + 10 thin rhombi
    coin.create_radial_pattern()

    # Option 2: Manually specify tiles (commented out)
    # custom_tiles = [
    #     ('kite', (0, 1), 0),
    #     ('dart', (1.5, 0), 45),
    #     ('kite', (0, -1), 180),
    #     ('dart', (-1.5, 0), 225),
    # ]
    # coin.create_pattern_from_spec(custom_tiles)

    # Plot and save (no interactive window)
    fig, ax = coin.plot(figsize=(12, 12), show_grid=False, show_background=True)
    plt.savefig('penrose_coin.png', dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()

    print("Coin design saved to 'penrose_coin.png'")
    print(f"Number of tiles: {len(coin.tiles)}")
