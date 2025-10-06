import numpy as np
import matplotlib.pyplot as plt
from typing import List
from main import (
    get_rhombus_vertices,
    get_decagon_vertices,
)


def plot_shapes(shapes: List[np.ndarray], filename: str = 'test_output.png', title: str = 'Shapes'):
    """Helper function to plot multiple shapes from vertex arrays"""
    plt.figure(figsize=(6, 6))

    # Pastel colors for shapes (non-transparent)
    pastel_colors = [
        '#FFB3BA',  # Light pink
        '#BFDBFE',  # Light blue
        '#BAE1D3',  # Light mint
        '#E0BBE4',  # Light lavender
        '#FFE4B5',  # Light peach
        '#D4F1F4',  # Light cyan
        '#F4D4BA',  # Light tan
        '#D4BAF4',  # Light purple
        '#FFF5BA',  # Light yellow
        '#C7E9C0',  # Light green
    ]

    for i, vertices in enumerate(shapes):
        # First shape (decagon) is dark grey
        if i == 0:
            color = '#3A3A3A'
        else:
            # Use pastel colors for other shapes
            color = pastel_colors[(i - 1) % len(pastel_colors)]

        # Close the polygon by appending first vertex
        closed_vertices = np.vstack([vertices, vertices[0]])
        plt.fill(closed_vertices[:, 0], closed_vertices[:, 1], color=color, alpha=1.0, edgecolor='none')

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
    return 0.5 / np.cos(np.radians(alpha))


def test_calculate_edge_length_of_unit_height_rhombus():
    """Test the calculation of edge length for a rhombus with unit height"""
    acute_angle = 72
    edge_length = calculate_edge_length_of_unit_height_rhombus(acute_angle)
    print(f"Edge length for rhombus with {acute_angle}° acute angle and unit height: {edge_length}")
    # Expected value can be calculated or looked up; here we just check it's positive
    assert edge_length > 0


def get_penrose_coin_shapes(scale_factor: float = 0.85) -> List[np.ndarray]:
    KITE_ACUTE_ANGLE = 72
    KITE_OBTUSE_ANGLE = 180 - KITE_ACUTE_ANGLE  # 108 degrees

    DART_ACUTE_ANGLE = 36

    first_tile = get_rhombus_vertices((0.0, 0.5), 0, KITE_OBTUSE_ANGLE, scale_factor=scale_factor)
    second_tile = get_rhombus_vertices((0.0, 0.5), 72, KITE_OBTUSE_ANGLE, scale_factor=scale_factor)
    third_tile = get_rhombus_vertices((0.0, 0.5), 144, KITE_OBTUSE_ANGLE, scale_factor=scale_factor)
    fourth_tile = get_rhombus_vertices((0.0, 0.5), 216, KITE_OBTUSE_ANGLE, scale_factor=scale_factor)
    fifth_tile = get_rhombus_vertices((0.0, 0.5), 288, KITE_OBTUSE_ANGLE, scale_factor=scale_factor)

    edge_length = calculate_edge_length_of_unit_height_rhombus(KITE_ACUTE_ANGLE)

    dart_long_length = 2 * edge_length * np.cos(np.radians(DART_ACUTE_ANGLE / 2))  # long edge of dart
    dart_sf = dart_long_length * scale_factor

    half_width_dart = edge_length * np.sin(np.radians(DART_ACUTE_ANGLE / 2))
    dart_center = edge_length + half_width_dart

    first_dart = get_rhombus_vertices((0.0, dart_center), 36, 144, scale_factor=dart_sf, initial_rotation=90)
    second_dart = get_rhombus_vertices((0.0, dart_center), 108, 144, scale_factor=dart_sf, initial_rotation=90)
    third_dart = get_rhombus_vertices((0.0, dart_center), 180, 144, scale_factor=dart_sf, initial_rotation=90)
    fourth_dart = get_rhombus_vertices((0.0, dart_center), 252, 144, scale_factor=dart_sf, initial_rotation=90)
    fifth_dart = get_rhombus_vertices((0.0, dart_center), 324, 144, scale_factor=dart_sf, initial_rotation=90)

    # Create decagon background (drawn first, so it appears behind)
    # the outer radius should be half the pipe width
    decagon_sf = 1.0
    decagon = get_decagon_vertices(center=(0.0, 0.0), scale_factor=decagon_sf)

    return [
        # decagon background
        decagon,

        # kites
        first_tile,
        second_tile,
        third_tile,
        fourth_tile,
        fifth_tile,

        # darts
        first_dart,
        second_dart,
        third_dart,
        fourth_dart,
        fifth_dart,
    ]


def test_draw_square():
    shapes = get_penrose_coin_shapes(scale_factor=0.85)
    first_tile = shapes[1]  # first kite

    plot_shapes(shapes, filename='test_square.png', title='Penrose Coin Center')

    assert first_tile.shape == (4, 2)
