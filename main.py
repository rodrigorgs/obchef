import pyglet
from obchef import Cozinheiro, Tilemap, Cozinha

class MainWindow(pyglet.window.Window):
  def __init__(self):
    super(MainWindow, self).__init__(960, 540, resizable=False)
    self.cozinha = Cozinha()

  def on_draw(self):
    self.clear()
    self.cozinha.draw()

  def on_key_press(self, symbol, modifiers):
    if symbol == pyglet.window.key.ESCAPE:
        pyglet.app.exit()
    self.cozinha.on_key_press(symbol, modifiers)

if __name__ == '__main__':
    window = MainWindow()
    pyglet.app.run()