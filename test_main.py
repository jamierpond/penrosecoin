import numpy as np
import matplotlib.pyplot as plt
from typing import List
from main import (
    calculate_edge_length_of_unit_height_rhombus,
    get_penrose_coin_shapes,
)


def plot_shapes(
    shapes: List[np.ndarray], filename: str = "test_output.png", title: str = "Shapes"
):
    """Helper function to plot multiple shapes from vertex arrays"""
    plt.figure(figsize=(6, 6))

    # Pastel colors for shapes (non-transparent)
    pastel_colors = [
        "#FFB3BA",  # Light pink
        "#BFDBFE",  # Light blue
        "#BAE1D3",  # Light mint
        "#E0BBE4",  # Light lavender
        "#FFE4B5",  # Light peach
        "#D4F1F4",  # Light cyan
        "#F4D4BA",  # Light tan
        "#D4BAF4",  # Light purple
        "#FFF5BA",  # Light yellow
        "#C7E9C0",  # Light green
    ]

    for i, vertices in enumerate(shapes):
        # First shape (decagon) is dark grey
        if i == 0:
            color = "#3A3A3A"
        else:
            # Use pastel colors for other shapes
            color = pastel_colors[(i - 1) % len(pastel_colors)]

        # Close the polygon by appending first vertex
        closed_vertices = np.vstack([vertices, vertices[0]])
        plt.fill(
            closed_vertices[:, 0],
            closed_vertices[:, 1],
            color=color,
            alpha=1.0,
            edgecolor="none",
        )

    plt.xlim(-1, 1)
    plt.ylim(-1, 1)
    plt.gca().set_aspect("equal")
    plt.grid(True, alpha=0.3)
    plt.title(title)

    plt.savefig(filename, dpi=150, bbox_inches="tight")
    plt.show()
    plt.close()


def test_calculate_edge_length_of_unit_height_rhombus():
    """Test the calculation of edge length for a rhombus with unit height"""
    acute_angle = 72
    edge_length = calculate_edge_length_of_unit_height_rhombus(acute_angle)
    print(
        f"Edge length for rhombus with {acute_angle}° acute angle and unit height: {edge_length}"
    )
    # Expected value can be calculated or looked up; here we just check it's positive
    assert edge_length > 0

    # probs todo more actual test lol


def test_draw_square():
    decagon, kites, darts = get_penrose_coin_shapes(scale_factor=0.85)
    shapes = [decagon] + kites + darts

    plot_shapes(shapes, filename="test_square.png", title="Penrose Coin Center")

    first_tile = kites[0]  # first kite
    assert first_tile.shape == (4, 2)
