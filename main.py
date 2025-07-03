import pyxel
import random

import pyxel
import random

class Game:
    def __init__(self):
        pyxel.init(256, 256, title="Dodge It!", fps=60)
        
        self._create_game_assets()
        self.setup()

        pyxel.run(self.update, self.draw)

    def _create_game_assets(self):
        """Creates sprites for the player, obstacles, ground, and explosions."""
        # Player sprite (16x8) - uses colkey 0
        pyxel.images[0].set(0, 0, [
            "0000000880000000",
            "0000008888000000",
            "000000dddd000000",
            "00000d8d8d8d0000",
            "00000d88888d0000",
            "00000d08808d0000",
            "0000008008000000",
            "0000088008800000",
        ])
        # Obstacle sprite (8x8) - uses colkey 0
        pyxel.images[0].set(16, 0, [
            "0440",
            "4444",
            "4444",
            "0440",
        ])
        # Ground tiles (8x8)
        # Grass
        pyxel.images[0].set(0, 8, [
            "b7b7b7b7",
            "7b7b7b7b",
            "bbbbbbbb",
            "bbbbbbbb",
            "bbbbbbbb",
            "bbbbbbbb",
            "bbbbbbbb",
            "bbbbbbbb",
        ])
        # Dirt
        pyxel.images[0].set(8, 8, [
            "6e6e6e6e",
            "e6e6e6e6",
            "6e6e6e6e",
            "e6e6e6e6",
            "6e6e6e6e",
            "e6e6e6e6",
            "6e6e6e6e",
            "e6e6e6e6",
        ])
        # Explosion sprite (32x32) - uses colkey 0
        pyxel.images[0].set(24, 0, [
            "00000000000000000000000000000000",
            "00000000000000000000000000000000",
            "00000000000000000000000000000000",
            "00000000000000000000000000000000",
            "00000000000000000000000000000000",
            "00000000000000000000000000000000",
            "00000000000000000000000000000000",
            "00000000000000000000000000000000",
            "00000000000000000000000000000000",
            "00000000000000000000000000000000",
            "00000000000000000000000000000000",
            "00000000000000000000000000000000",
            "00000000000000000000000000000000",
            "00000000000000000000000000000000",
            "00000000000000000000000000000000",
            "00000000000000000000000000000000",
            "00000000000000000000000000000000",
            "00000000000000000000000000000000",
            "00000000000000000000000000000000",
            "00000000000000000000000000000000",
            "00000000000000000000000000000000",
            "00000000000000000000000000000000",
            "00000000000000000000000000000000",
            "00000000000000000000000000000000",
            "00000000000000000000000000000000",
            "00000000000000000000000000000000",
            "00000000000000000000000000000000",
            "00000000000000000000000000000000",
            "00000000000000000000000000000000",
            "00000000000000000000000000000000",
            "00000000000000000000000000000000",
            "00000000000000000000000000000000",
        ])

        pyxel.sounds[0].set("a3c1", "t", "7", "vffn", 12)

    def setup(self):
        self.player_x = 120
        self.player_y = pyxel.height - 16 - 8 # Player stands on the 16px high ground
        self.obstacles = []
        self.explosions = [] # Initialize explosions list
        self.score = 0
        self.is_game_over = False

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        if self.is_game_over:
            if pyxel.btnp(pyxel.KEY_RETURN):
                self.setup()
            return

        self.update_player()
        self.update_obstacles()
        self.update_explosions() # New: Update explosions
        self.check_collisions()
        self.score += 1

    def update_player(self):
        if pyxel.btn(pyxel.KEY_LEFT):
            self.player_x = max(self.player_x - 3, 0)
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.player_x = min(self.player_x + 3, pyxel.width - 16)

    def update_obstacles(self):
        difficulty_factor = 1 + self.score / 1800
        current_spawn_timer = max(10, 40 - self.score // 120)

        new_obstacles = []
        for obs in self.obstacles:
            obs[0] += obs[2]
            obs[1] += obs[3]

            # Check if obstacle hits the ground
            if obs[1] >= pyxel.height - 16 - 8: # Obstacle bottom reaches ground level
                self.explosions.append([obs[0] - 12, pyxel.height - 16 - 24, 10]) # x, y, timer (adjusted for 32x32 explosion)
            elif -8 <= obs[0] <= pyxel.width and -8 <= obs[1] <= pyxel.height:
                new_obstacles.append(obs)
        self.obstacles = new_obstacles

        if pyxel.frame_count % int(current_spawn_timer) == 0:
            if random.random() > 0.3:
                obs_x = random.randint(0, pyxel.width - 8)
                obs_y = -8
                obs_vx = random.uniform(-0.5, 0.5) * difficulty_factor
                obs_vy = random.uniform(1.0, 2.5) * difficulty_factor
                self.obstacles.append([obs_x, obs_y, obs_vx, obs_vy])
            else:
                side = random.choice([-8, pyxel.width])
                obs_x = side
                obs_y = random.randint(0, pyxel.height - 80) 
                obs_vx = (-2 if side > 0 else 2) * difficulty_factor
                obs_vy = random.uniform(-0.5, 0.5) * difficulty_factor
                self.obstacles.append([obs_x, obs_y, obs_vx, obs_vy])

    def update_explosions(self):
        new_explosions = []
        for exp in self.explosions:
            exp[2] -= 1 # Decrement timer
            if exp[2] > 0:
                new_explosions.append(exp)
        self.explosions = new_explosions

    def check_collisions(self):
        player_box = (self.player_x, self.player_y, 16, 8)
        for obs in self.obstacles:
            obs_box = (obs[0], obs[1], 8, 8)
            if (player_box[0] < obs_box[0] + obs_box[2] and
                player_box[0] + player_box[2] > obs_box[0] and
                player_box[1] < obs_box[1] + obs_box[3] and
                player_box[1] + player_box[3] > obs_box[1]):
                self.is_game_over = True
                pyxel.play(0, 0)
        
        # New: Check collision with explosions
        for exp in self.explosions:
            exp_box = (exp[0], exp[1], 32, 32) # Explosion hitbox (32x32)
            if (player_box[0] < exp_box[0] + exp_box[2] and
                player_box[0] + player_box[2] > exp_box[0] and
                player_box[1] < exp_box[1] + exp_box[3] and
                player_box[1] + player_box[3] > exp_box[1]):
                self.is_game_over = True
                pyxel.play(0, 0) # Play sound on hit

    def draw(self):
        pyxel.cls(12)  # Clear screen with light blue

        # Draw the ground
        ground_y = pyxel.height - 16
        for x in range(0, pyxel.width, 8):
            pyxel.blt(x, ground_y, 0, 0, 8, 8, 8) # Grass tile
            pyxel.blt(x, ground_y + 8, 0, 8, 8, 8, 8) # Dirt tile

        # Draw game elements with transparency
        for obs in self.obstacles:
            pyxel.blt(obs[0], obs[1], 0, 16, 0, 8, 8, 0)
        pyxel.blt(self.player_x, self.player_y, 0, 0, 0, 16, 8, 0)

        # New: Draw explosions
        for exp in self.explosions:
            pyxel.blt(exp[0], exp[1], 0, 24, 0, 32, 32, 0) # Draw 32x32 explosion

        # Draw UI
        score_text = f"Score: {self.score}"
        pyxel.text(5, 5, score_text, 7)

        if self.is_game_over:
            text_width = len("GAME OVER") * 4
            pyxel.text(pyxel.width / 2 - text_width / 2, 110, "GAME OVER", 8)
            restart_text = "Press Enter to Restart"
            text_width = len(restart_text) * 4
            pyxel.text(pyxel.width / 2 - text_width / 2, 125, restart_text, 7)

if __name__ == "__main__":
    Game()

if __name__ == "__main__":
    Game()