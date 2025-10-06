import numpy as np
import matplotlib.pyplot as plt
from typing import List
from main import (
    calculate_edge_length_of_unit_height_rhombus,
    get_penrose_coin_shapes,
)


def plot_shapes(
    decagon: np.ndarray,
    kites: List[np.ndarray],
    darts: List[np.ndarray],
    filename: str = "test_output.png",
    title: str = "Shapes",
):
    """Helper function to plot decagon, kites, and darts"""
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

    # Plot decagon in dark grey
    closed_vertices = np.vstack([decagon, decagon[0]])
    plt.fill(
        closed_vertices[:, 0],
        closed_vertices[:, 1],
        color="#3A3A3A",
        alpha=1.0,
        edgecolor="none",
    )

    # Plot kites and darts with pastel colors
    color_idx = 0
    for vertices in kites + darts:
        color = pastel_colors[color_idx % len(pastel_colors)]
        color_idx += 1

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

    plot_shapes(
        decagon, kites, darts, filename="test_square.png", title="Penrose Coin Center"
    )

    first_tile = kites[0]  # first kite
    assert first_tile.shape == (4, 2)
