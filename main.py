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


def get_rhombus_vertices(
    center: Tuple[float, float],
    angle: float,
    acute_angle: float,
    height: float = 1.0,
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

    # Translate to center
    center_array = np.array(center)
    vertices += center_array

    # Rotate about the origin by `angle`
    vertices = rotate_shape_about_origin(vertices, angle)

    return vertices


