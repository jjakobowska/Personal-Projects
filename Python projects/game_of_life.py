'''
This is my approach to classic game of life. 
You can: 
- see the evolution of a game on a grid,
- pause and resume the evolution 
- alter the state of the game by clicking on a grid (thus adding specimen to the population or subtracting one)
- restart the game with a button placed on a grid
'''
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from scipy.signal import convolve2d

class GameOfLife:
    def __init__(self, N=100, initial_state='random', update_interval=50, ruleset='conway'):
        self.N = N
        self.update_interval = update_interval
        self.grid = self.initial_grid(initial_state)
        self.ruleset = ruleset
        self.fig, self.ax = plt.subplots()
        self.img = self.ax.imshow(self.grid, interpolation='nearest')
        self.ani = None
        self.paused = False  # Keep track of pause state

    def initial_grid(self, initial_state):
        if initial_state == 'random':
            return np.random.choice([1, 0], size=(self.N, self.N), p=[0.2, 0.8])
        elif isinstance(initial_state, np.ndarray):
            return initial_state
        else:
            raise ValueError("Unsupported initial state")

    def update(self, frame_num):
        if not self.paused:  # Only update if not paused
            kernel = np.array([[1, 1, 1],
                               [1, 0, 1],
                               [1, 1, 1]])
            neighbor_sum = convolve2d(self.grid, kernel, mode='same', boundary='wrap')

            self.grid = np.where((self.grid == 1) & ((neighbor_sum < 2) | (neighbor_sum > 3)), 0, self.grid)
            self.grid = np.where((self.grid == 0) & (neighbor_sum == 3), 1, self.grid)

        self.img.set_array(self.grid)
        return self.img,

    def onclick(self, event):
        if event.dblclick:  # Use double click to toggle cell state
            ix, iy = int(event.xdata), int(event.ydata)
            if ix >= 0 and iy >= 0 and ix < self.N and iy < self.N:
                self.grid[iy, ix] = 1 if self.grid[iy, ix] == 0 else 0
                self.img.set_array(self.grid)
                self.fig.canvas.draw()

    def onkeypress(self, event):
        if event.key == ' ':
            self.paused = not self.paused  # Space bar to pause/resume
        elif event.key == 'r':
            self.grid = self.initial_grid('random')  # 'r' to reset
            self.img.set_array(self.grid)
            self.fig.canvas.draw()

    def run(self):
        self.fig.canvas.mpl_connect('button_press_event', self.onclick)
        self.fig.canvas.mpl_connect('key_press_event', self.onkeypress)
        self.ani = animation.FuncAnimation(self.fig, self.update, interval=self.update_interval, blit=True)
        plt.show()

if __name__ == '__main__':
    game = GameOfLife(N=100, initial_state='random', update_interval=100, ruleset='conway')
    game.run()
