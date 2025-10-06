import numpy as np
import matplotlib.pyplot as plt
from typing import List
from main import (
    get_rhombus_vertices,
)


def plot_shapes(shapes: List[np.ndarray], filename: str = 'test_output.png', title: str = 'Shapes'):
    """Helper function to plot multiple shapes from vertex arrays"""
    plt.figure(figsize=(6, 6))

    for vertices in shapes:
        # Close the polygon by appending first vertex
        closed_vertices = np.vstack([vertices, vertices[0]])
        plt.fill(closed_vertices[:, 0], closed_vertices[:, 1], 'blue', alpha=0.3)

    plt.xlim(-1, 1)
    plt.ylim(-1, 1)
    plt.gca().set_aspect('equal')
    plt.grid(True, alpha=0.3)
    plt.title(title)

    plt.savefig(filename, dpi=150, bbox_inches='tight')
    plt.show()
    plt.close()


def test_square_tile():
    """Test creating a square tile using get_rhombus_vertices with 90° acute angle"""
    # A rhombus with 90° acute angle is a square
    first_tile = get_rhombus_vertices((0, 0), 0, 90)

    # Check we have 4 vertices
    assert first_tile.shape == (4, 2)
    print(first_tile)

    # Check it's centered at origin
    centroid = first_tile.mean(axis=0)
    np.testing.assert_array_almost_equal(centroid, [0, 0])

    # For a square with edge_length = 1 and 90° acute angle:
    # d1 = d2 = cos(45°) = sin(45°) ≈ 0.707
    expected_half_diag = np.cos(np.radians(45))

    expected_vertices = np.array([
        [expected_half_diag, 0],
        [0, expected_half_diag],
        [-expected_half_diag, 0],
        [0, -expected_half_diag]
    ])

    np.testing.assert_array_almost_equal(first_tile, expected_vertices, decimal=5)


def test_draw_square():
    """Test drawing a square using get_rhombus_vertices"""
    first_tile = get_rhombus_vertices((0.0, 0.5), 90, 72)

    # second_tile = get_rhombus_vertices((0, 0.5), 90 + 5, 72)

    plot_shapes([
        first_tile,
        # second_tile,
    ], filename='test_square.png', title='Square from get_rhombus_vertices (90°)')

    assert first_tile.shape == (4, 2)
