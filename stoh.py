import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.offline as pyo

def midpoint_displacement(height_map, x_min, x_max, y_min, y_max, roughness, random_seed=None):
    np.random.seed(random_seed)

    def midpoint(x, y):
        return (x + y) / 2.0

    def generate(height_map, x_min, x_max, y_min, y_max, roughness, random_seed=None):
        if random_seed is not None:
            np.random.seed(random_seed)

        x_mid = (x_min + x_max) // 2
        y_mid = (y_min + y_max) // 2

        height_map[y_mid, x_mid] = midpoint(
            height_map[y_min, x_min],
            height_map[y_max, x_min]
        )

        height_map[y_mid, x_max] = midpoint(
            height_map[y_min, x_max],
            height_map[y_max, x_max]
        )

        height_map[y_min, x_mid] = midpoint(
            height_map[y_min, x_min],
            height_map[y_min, x_max]
        )

        height_map[y_max, x_mid] = midpoint(
            height_map[y_max, x_min],
            height_map[y_max, x_max]
        )

        center_value = midpoint(
            height_map[y_min, x_min],
            height_map[y_max, x_max]
        )

        height_map[y_mid, x_mid] = midpoint(
            center_value,
            (center_value + np.random.uniform(-roughness, roughness))
        )

        if x_max - x_min > 1 or y_max - y_min > 1:
            size_local = (x_max - x_min) // 2
            generate(height_map, x_min, x_mid, y_min, y_mid, roughness / 2, random_seed)
            generate(height_map, x_mid, x_max, y_min, y_mid, roughness / 2, random_seed)
            generate(height_map, x_min, x_mid, y_mid, y_max, roughness / 2, random_seed)
            generate(height_map, x_mid, x_max, y_mid, y_max, roughness / 2, random_seed)

    size = height_map.shape[0] - 1
    generate(height_map, 0, size, 0, size, roughness, random_seed)

    return height_map

def plot_smooth_terrain_fractal(size, roughness, random_seed=None):
    height_map = midpoint_displacement(np.zeros((size + 1, size + 1)), 0, size, 0, size, roughness, random_seed)

    fig = make_subplots(rows=1, cols=1, specs=[[{'type': 'surface'}]])

    fig.add_trace(go.Surface(z=height_map, colorscale='Viridis'))

    fig.update_layout(scene=dict(
        xaxis_title='X',
        yaxis_title='Y',
        zaxis_title='Elevation'
    ))

    fig.update_layout(title='Smooth Terrain-Like Fractal')

    # Save the plot offline
    pyo.plot(fig, filename='smooth_terrain_fractal.html', auto_open=False)

if __name__ == "__main__":
    size = 255  # Adjust the size of the fractal (should be 2^n + 1 for simplicity)
    roughness = 0.000002  # Adjust the roughness of the terrain (0.0 to 1.0)

    plot_smooth_terrain_fractal(size, roughness)
 