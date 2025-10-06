import numpy as np
from typing import Tuple, List


def rotate_shape_about_origin(vertices: np.ndarray, angle: float) -> np.ndarray:
    """Rotate vertices about the origin by the given angle in degrees"""
    angle_rad = np.radians(angle)
    rotation = np.array(
        [
            [np.cos(angle_rad), -np.sin(angle_rad)],
            [np.sin(angle_rad), np.cos(angle_rad)],
        ]
    )
    return vertices @ rotation.T


def get_decagon_vertices(
    center: Tuple[float, float] = (0.0, 0.0),
    scale_factor: float = 1.0,
) -> np.ndarray:
    """Generate vertices for a unit regular decagon (10-sided polygon)"""
    n_sides = 10
    angles = np.linspace(0, 2 * np.pi, n_sides, endpoint=False)

    # Start with first vertex at top (90 degrees)
    angles = angles + np.pi / 2

    vertices = (
        np.array([[np.cos(angle), np.sin(angle)] for angle in angles]) * scale_factor
    )

    center_array = np.array(center)
    vertices += center_array

    return vertices


def get_rhombus_vertices(
    center: Tuple[float, float],
    angle: float,
    acute_angle: float,
    height: float = 1.0,
    initial_rotation: float = 0.0,
    scale_factor: float = 1.0,
) -> np.ndarray:
    """Calculate vertices for a rhombus with specified acute angle"""
    edge_length = 1.0

    # Half-diagonal from center to obtuse vertex
    d1 = edge_length * np.cos(np.radians(acute_angle / 2))
    # Half-diagonal from center to acute vertex
    d2 = edge_length * np.sin(np.radians(acute_angle / 2))

    # Canonical rhombus with long diagonal on x-axis
    vertices = np.array(
        [
            [d1, 0],  # Right (obtuse)
            [0, d2],  # Top (acute)
            [-d1, 0],  # Left (obtuse)
            [0, -d2],  # Bottom (acute)
        ]
    )

    # Normalize vertical height (before rotation)
    actual_height = 2 * d2  # vertical height of unrotated rhombus
    height_scale = height / actual_height
    vertices *= height_scale * scale_factor

    vertices = rotate_shape_about_origin(vertices, initial_rotation)

    # Translate to center
    center_array = np.array(center)
    vertices += center_array

    # Rotate about the origin by `angle`
    vertices = rotate_shape_about_origin(vertices, angle)

    return vertices


def calculate_edge_length_of_unit_height_rhombus(acute_angle: float) -> float:
    alpha = acute_angle / 2
    return 0.5 / np.cos(np.radians(alpha))


def get_penrose_coin_shapes(scale_factor: float = 0.85) -> List[np.ndarray]:

    KITE_ACUTE_ANGLE = 72
    KITE_OBTUSE_ANGLE = 180 - KITE_ACUTE_ANGLE  # 108 degrees

    DART_ACUTE_ANGLE = 36

    first_tile = get_rhombus_vertices(
        (0.0, 0.5), 0, KITE_OBTUSE_ANGLE, scale_factor=scale_factor
    )
    second_tile = get_rhombus_vertices(
        (0.0, 0.5), 72, KITE_OBTUSE_ANGLE, scale_factor=scale_factor
    )
    third_tile = get_rhombus_vertices(
        (0.0, 0.5), 144, KITE_OBTUSE_ANGLE, scale_factor=scale_factor
    )
    fourth_tile = get_rhombus_vertices(
        (0.0, 0.5), 216, KITE_OBTUSE_ANGLE, scale_factor=scale_factor
    )
    fifth_tile = get_rhombus_vertices(
        (0.0, 0.5), 288, KITE_OBTUSE_ANGLE, scale_factor=scale_factor
    )

    edge_length = calculate_edge_length_of_unit_height_rhombus(KITE_ACUTE_ANGLE)

    dart_long_length = (
        2 * edge_length * np.cos(np.radians(DART_ACUTE_ANGLE / 2))
    )  # long edge of dart
    dart_sf = dart_long_length * scale_factor

    half_width_dart = edge_length * np.sin(np.radians(DART_ACUTE_ANGLE / 2))
    dart_center = edge_length + half_width_dart

    first_dart = get_rhombus_vertices(
        (0.0, dart_center), 36, 144, scale_factor=dart_sf, initial_rotation=90
    )
    second_dart = get_rhombus_vertices(
        (0.0, dart_center), 108, 144, scale_factor=dart_sf, initial_rotation=90
    )
    third_dart = get_rhombus_vertices(
        (0.0, dart_center), 180, 144, scale_factor=dart_sf, initial_rotation=90
    )
    fourth_dart = get_rhombus_vertices(
        (0.0, dart_center), 252, 144, scale_factor=dart_sf, initial_rotation=90
    )
    fifth_dart = get_rhombus_vertices(
        (0.0, dart_center), 324, 144, scale_factor=dart_sf, initial_rotation=90
    )

    # Create decagon background (drawn first, so it appears behind)
    # the outer radius should be half the pipe width
    decagon_sf = 1.0
    decagon = get_decagon_vertices(center=(0.0, 0.0), scale_factor=decagon_sf)

    return [
        # decagon background
        decagon,
        # kites
        first_tile,
        second_tile,
        third_tile,
        fourth_tile,
        fifth_tile,
        # darts
        first_dart,
        second_dart,
        third_dart,
        fourth_dart,
        fifth_dart,
    ]
