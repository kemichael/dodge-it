import pyxel

class Explosion:
    def __init__(self, x, y, timer):
        self.x = x
        self.y = y
        self.timer = timer
        self.width = 32
        self.height = 32

    def update(self):
        self.timer -= 1

    def draw(self):
        pyxel.blt(self.x, self.y, 0, 24, 0, self.width, self.height, 0)

def update_explosions(explosions):
    new_explosions = []
    for exp in explosions:
        exp.update()
        if exp.timer > 0:
            new_explosions.append(exp)
    explosions[:] = new_explosions
