import pyxel

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 16
        self.height = 8

    def update(self):
        if pyxel.btn(pyxel.KEY_LEFT):
            self.x = max(self.x - 3, 0)
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.x = min(self.x + 3, pyxel.width - self.width)

    def draw(self):
        pyxel.blt(self.x, self.y, 0, 0, 0, self.width, self.height, 0)
