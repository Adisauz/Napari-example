import napari
import numpy as np
from qtpy.QtCore import QTimer

HEIGHT, WIDTH = 100, 100
grid = np.random.choice([0, 1], size=(HEIGHT, WIDTH))

def step(grid):
    neighbors = sum(np.roll(np.roll(grid, i, 0), j, 1)
                    for i in (-1, 0, 1) for j in (-1, 0, 1)
                    if (i != 0 or j != 0))
    return (neighbors == 3) | ((grid == 1) & (neighbors == 2))

viewer = napari.Viewer()
layer = viewer.add_image(grid, name="Game of Life", colormap='gray', interpolation='nearest')

timer = QTimer()
timer.setInterval(100)

def update():
    global grid
    grid = step(grid).astype(np.uint8)
    layer.data = grid

timer.timeout.connect(update)

@viewer.bind_key('s')
def toggle_timer(viewer):
    if timer.isActive():
        timer.stop()
    else:
        timer.start()

@viewer.bind_key('r')
def reset_grid(viewer):
    global grid
    grid = np.random.choice([0, 1], size=(HEIGHT, WIDTH))
    layer.data = grid

napari.run()
