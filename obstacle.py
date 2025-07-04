import pyxel
import random
from explosion import Explosion

class Obstacle:
    def __init__(self, x, y, vx, vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.width = 8
        self.height = 8

    def update(self):
        self.x += self.vx
        self.y += self.vy

    def draw(self):
        pyxel.blt(self.x, self.y, 0, 16, 0, self.width, self.height, 0)

def update_obstacles(obstacles, score, explosions):
    difficulty_factor = 1 + score / 1800
    current_spawn_timer = max(10, 40 - score // 120)

    new_obstacles = []
    for obs in obstacles:
        obs.update()

        # Check if obstacle hits the ground
        if obs.y >= pyxel.height - 16 - 8: # Obstacle bottom reaches ground level
            explosions.append(Explosion(obs.x - 12, pyxel.height - 16 - 24, 10)) # x, y, timer (adjusted for 32x32 explosion)
        elif -obs.width <= obs.x <= pyxel.width and -obs.height <= obs.y <= pyxel.height:
            new_obstacles.append(obs)
    obstacles[:] = new_obstacles

    if pyxel.frame_count % int(current_spawn_timer) == 0:
        if random.random() > 0.3:
            obs_x = random.randint(0, pyxel.width - 8)
            obs_y = -8
            obs_vx = random.uniform(-0.5, 0.5) * difficulty_factor
            obs_vy = random.uniform(1.0, 2.5) * difficulty_factor
            obstacles.append(Obstacle(obs_x, obs_y, obs_vx, obs_vy))
        else:
            side = random.choice([-8, pyxel.width])
            obs_x = side
            obs_y = random.randint(0, pyxel.height - 80) 
            obs_vx = (-2 if side > 0 else 2) * difficulty_factor
            obs_vy = random.uniform(-0.5, 0.5) * difficulty_factor
            obstacles.append(Obstacle(obs_x, obs_y, obs_vx, obs_vy))
