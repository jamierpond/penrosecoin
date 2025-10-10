import numpy as np
import matplotlib.pyplot as plt
from typing import List
from main import (
    get_penrose_coin_shapes,
)


def plot_shapes(
    decagon: np.ndarray,
    kites: List[np.ndarray],
    darts: List[np.ndarray],
    filename: str = "test_output.png",
    title: str = "Shapes",
    kite_colors: List[str] | None = None,
    dart_colors: List[str] | None = None,
):
    """Helper function to plot decagon, kites, and darts

    Args:
        decagon: Vertices for the decagon background
        kites: List of kite vertices
        darts: List of dart vertices
        filename: Output filename
        title: Plot title
        kite_colors: List of colors for each kite (one per kite). If None, uses default pastel colors.
        dart_colors: List of colors for each dart (one per dart). If None, uses default pastel colors.
    """
    plt.figure(figsize=(6, 6))

    # Default pastel colors for shapes (non-transparent)
    default_pastel_colors = [
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

    # Use provided colors or default to pastel colors
    if kite_colors is None:
        kite_colors = [default_pastel_colors[i % len(default_pastel_colors)] for i in range(len(kites))]
    if dart_colors is None:
        dart_colors = [default_pastel_colors[(i + len(kites)) % len(default_pastel_colors)] for i in range(len(darts))]

    # Plot decagon background
    closed_vertices = np.vstack([decagon, decagon[0]])
    plt.fill(
        closed_vertices[:, 0],
        closed_vertices[:, 1],
        color="#333333",
        alpha=1.0,
        edgecolor="none",
    )

    # Plot kites with their colors
    for i, vertices in enumerate(kites):
        color = kite_colors[i % len(kite_colors)]
        closed_vertices = np.vstack([vertices, vertices[0]])
        plt.fill(
            closed_vertices[:, 0],
            closed_vertices[:, 1],
            color=color,
            alpha=1.0,
            edgecolor="none",
        )

    # Plot darts with their colors
    for i, vertices in enumerate(darts):
        color = dart_colors[i % len(dart_colors)]
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


def test_draw_square():
    cool_sf = 0.85
    decagon, kites, darts = get_penrose_coin_shapes(scale_factor=cool_sf)

    # Colors matching the reference image
    red = "#FF0000"
    green = "#00FF00"
    kite_colors = [green, red, green, green, red]  # Alternating green and red
    dart_colors = ["#8000FF"] * 5  # All darts are purple

    plot_shapes(
        decagon,
        kites,
        darts,
        filename="test_square.png",
        title="Penrose Coin Center",
        kite_colors=kite_colors,
        dart_colors=dart_colors,
    )

    first_tile = kites[0]  # first kite
    assert first_tile.shape == (4, 2)
