import numpy as np
import matplotlib.pyplot as plt
from typing import List
from main import (
    get_rhombus_vertices,
)


def plot_shapes(shapes: List[np.ndarray], filename: str = 'test_output.png', title: str = 'Shapes'):
    """Helper function to plot multiple shapes from vertex arrays"""
    plt.figure(figsize=(6, 6))

    for i, vertices in enumerate(shapes):
        # Generate deterministic random color based on index
        rng = np.random.RandomState(i)
        color = rng.rand(3)  # RGB values between 0 and 1

        # Close the polygon by appending first vertex
        closed_vertices = np.vstack([vertices, vertices[0]])
        plt.fill(closed_vertices[:, 0], closed_vertices[:, 1], color=color, alpha=0.3, edgecolor='none')

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

def calculate_edge_length_of_unit_height_rhombus(acute_angle: float) -> float:
    alpha = acute_angle / 2
    return 2 * np.cos(np.radians(alpha))


def test_calculate_edge_length_of_unit_height_rhombus():
    """Test the calculation of edge length for a rhombus with unit height"""
    acute_angle = 72
    edge_length = calculate_edge_length_of_unit_height_rhombus(acute_angle)
    print(f"Edge length for rhombus with {acute_angle}° acute angle and unit height: {edge_length}")
    # Expected value can be calculated or looked up; here we just check it's positive
    assert edge_length > 0


def test_draw_square():
    """Test drawing a square using get_rhombus_vertices"""
    scale_factor = 1.0

    acute_angle = 72
    obtuse_angle = 180 - acute_angle  # 108 degrees

    first_tile = get_rhombus_vertices((0.0, 0.5), 0, obtuse_angle, scale_factor=scale_factor)
    second_tile = get_rhombus_vertices((0.0, 0.5), 72, obtuse_angle, scale_factor=scale_factor)
    third_tile = get_rhombus_vertices((0.0, 0.5), 144, obtuse_angle, scale_factor=scale_factor)
    fourth_tile = get_rhombus_vertices((0.0, 0.5), 216, obtuse_angle, scale_factor=scale_factor)
    fifth_tile = get_rhombus_vertices((0.0, 0.5), 288, obtuse_angle, scale_factor=scale_factor)

    edge_length = calculate_edge_length_of_unit_height_rhombus(acute_angle)


    dart_long_length = edge_length * np.cos(np.radians(acute_angle / 2))
    dart_sf = dart_long_length * scale_factor

    first_dart = get_rhombus_vertices((0.0, 0.85), 36, 144, scale_factor=dart_sf, initial_rotation=90)

    print(f"Edge length for rhombus with 108° acute angle and unit height: {edge_length}")

    # second_tile = get_rhombus_vertices((0, 0.5), 90 + 72, 72)

    plot_shapes([
        # kites
        first_tile,
        second_tile,
        third_tile,
        fourth_tile,
        fifth_tile,

        # darts
        first_dart,
    ], filename='test_square.png', title='Square from get_rhombus_vertices (90°)')

    assert first_tile.shape == (4, 2)
