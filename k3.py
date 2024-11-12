import os

import numpy as np
import plotly.graph_objects as go


# Function to generate Klein Bottle coordinates
def klein_bottle(u, v):
    x = (2/15) * (3 * np.cos(u) + np.cos(3 * u)) * (2 + np.sin(v))
    y = (2/15) * (3 * np.sin(u) - np.sin(3 * u)) * (2 + np.sin(v))
    z = (1/5) * (np.sin(v) + 2 * np.sin(u))
    return x, y, z

# Create u and v values
u = np.linspace(0, 2 * np.pi, 100)
v = np.linspace(0, 2 * np.pi, 50)
u, v = np.meshgrid(u, v)

# Get the Klein Bottle coordinates
x, y, z = klein_bottle(u, v)

# Create a 3D surface plot with Plotly
fig = go.Figure(data=[go.Surface(
    z=z,
    x=x,
    y=y,
    colorscale='Viridis',  # You can change the color scale for customization
    opacity=0.8
)])

# Update layout for better visualization
fig.update_layout(
    title='Artistic Klein Bottle',
    scene=dict(
        xaxis_title='X-axis',
        yaxis_title='Y-axis',
        zaxis_title='Z-axis',
        camera=dict(
            eye=dict(x=1.5, y=1.5, z=1.5)
        )
    ),
    margin=dict(l=0, r=0, b=0, t=40)
)

# Create img folder if it doesn't exist
os.makedirs('img', exist_ok=True)

# Save the figure as an HTML file
fig.write_html('img/k3.html')

print("Klein Bottle image saved in the 'img' folder as an HTML file.")

