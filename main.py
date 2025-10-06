import numpy as np
from typing import Tuple


def rotate_shape_about_origin(vertices: np.ndarray, angle: float) -> np.ndarray:
    """Rotate vertices about the origin by the given angle in degrees"""
    angle_rad = np.radians(angle)
    rotation = np.array([
        [np.cos(angle_rad), -np.sin(angle_rad)],
        [np.sin(angle_rad), np.cos(angle_rad)]
    ])
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

    vertices = np.array([
        [np.cos(angle), np.sin(angle)]
        for angle in angles
    ]) * scale_factor

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
    vertices = np.array([
        [d1, 0],      # Right (obtuse)
        [0, d2],      # Top (acute)
        [-d1, 0],     # Left (obtuse)
        [0, -d2],     # Bottom (acute)
    ])

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


