import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class TileParams:
    """Parameters for Penrose tiling"""
    scale: float = 1.0
    margin: float = 0.02  # Gap between tiles
    green_color: str = '#00A000'
    red_color: str = '#D00000'
    purple_color: str = '#8800FF'
    background_color: str = '#FFFFFF'
    edge_color: str = '#DDDDDD'
    edge_width: float = 2.0


class PenroseTile:
    """Represents a single Penrose tile (always a fat rhombus for this pattern)"""

    def __init__(self, tile_type: str, center: Tuple[float, float],
                 angle: float, params: TileParams):
        """
        tile_type: 'green', 'red', or 'purple'
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
        # All tiles are fat rhombi: 72° acute angles, 108° obtuse angles
        edge_length = 1.0
        acute = 72
        
        # Half-diagonal from center to obtuse vertex
        d1 = edge_length * np.cos(np.radians(acute / 2))  # cos(36)
        # Half-diagonal from center to acute vertex
        d2 = edge_length * np.sin(np.radians(acute / 2))  # sin(36)

        # Canonical rhombus with long diagonal on x-axis
        vertices = np.array([
            [d1, 0],      # Right (obtuse)
            [0, d2],      # Top (acute)
            [-d1, 0],     # Left (obtuse)
            [0, -d2],     # Bottom (acute)
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
        color_map = {
            'green': self.params.green_color,
            'red': self.params.red_color,
            'purple': self.params.purple_color,
        }
        color = color_map.get(self.tile_type, '#000000')
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

    def create_pattern(self):
        """Creates the 2D projection of the rhombic triacontahedron"""
        self.tiles = []
        
        # Geometric constants based on the golden ratio for the fat rhombus
        edge_length = 1.0
        acute_angle = 72
        d1 = edge_length * np.cos(np.radians(acute_angle / 2))  # cos(36)

        # Define the pattern as a list of tiles (type, center, angle)
        # The pattern is constructed from layers, starting from a central star.
        
        # Layer 1: Central Star (5 rhombi)
        # Colors are ordered to match the image, starting from the top and going clockwise.
        central_colors = ['green', 'red', 'green', 'green', 'red']
        for i in range(5):
            angle = 90 - i * 72
            center_vec = np.array([d1, 0])
            
            # Rotate the center vector to position each rhombus of the star
            rot_rad = np.radians(angle)
            rotation = np.array([[np.cos(rot_rad), -np.sin(rot_rad)],
                                 [np.sin(rot_rad), np.cos(rot_rad)]])
            center = center_vec @ rotation.T
            
            self.add_tile(central_colors[i], tuple(center), angle)

        # Layer 2: Middle Belt (5 "purple" rhombi)
        # These are positioned relative to the central star
        for i in range(5):
            angle = 54 - i * 72
            # This center calculation is derived from geometric construction
            center_vec = np.array([2 * d1 * np.cos(np.radians(36)), 0])
            
            rot_rad = np.radians(angle + 18) # Additional rotation for positioning
            rotation = np.array([[np.cos(rot_rad), -np.sin(rot_rad)],
                                 [np.sin(rot_rad), np.cos(rot_rad)]])
            center = center_vec @ rotation.T

            self.add_tile('purple', tuple(center), angle)

        # Layer 3: Outer Belt (5 rhombi)
        outer_colors = ['green', 'red', 'green', 'red', 'green'] # Symmetrical coloring
        for i in range(5):
            angle = 90 - i * 72
            # Positioned further out
            center_vec = np.array([d1 + 2 * d1 * np.cos(np.radians(72)), 
                                   2 * d1 * np.sin(np.radians(72))])

            rot_rad = np.radians(angle - 90)
            rotation = np.array([[np.cos(rot_rad), -np.sin(rot_rad)],
                                 [np.sin(rot_rad), np.cos(rot_rad)]])
            center = center_vec @ rotation.T
            
            self.add_tile(outer_colors[i], tuple(center), angle)


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
        scale=0.4,
        margin=0.015,
        edge_color='#FFFFFF',
        edge_width=2.5
    )

    coin = PenroseCoin(params)

    # Create the exact pattern from the image
    coin.create_pattern()

    # Plot and show
    fig, ax = coin.plot(figsize=(12, 12), show_grid=False, show_background=True)
    plt.savefig('penrose_coin.png', dpi=300, bbox_inches='tight', facecolor=params.background_color)
    plt.show()

    print("Coin design saved to 'penrose_coin.png'")
    print(f"Number of tiles: {len(coin.tiles)}")
