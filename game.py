import pyxel
import random
from assets import create_game_assets
from player import Player
from obstacle import Obstacle, update_obstacles
from explosion import Explosion, update_explosions

from enum import Enum

class GameState(Enum):
    TITLE = 0
    PLAYING = 1
    GAME_OVER = 2

class Game:
    def __init__(self):
        pyxel.init(256, 256, title="Dodge It!", fps=60)
        
        create_game_assets()
        self.game_state = GameState.TITLE
        self.score = 0
        self.player = Player(120, pyxel.height - 16 - 8)
        self.obstacles = []
        self.explosions = []

        pyxel.run(self.update, self.draw)

    def setup(self):
        self.player = Player(120, pyxel.height - 16 - 8)
        self.obstacles = []
        self.explosions = []
        self.score = 0
        # self.is_game_over is now managed by game_state

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        if self.game_state == GameState.TITLE:
            if pyxel.btnp(pyxel.KEY_RETURN):
                self.game_state = GameState.PLAYING
        elif self.game_state == GameState.PLAYING:
            self.player.update()
            update_obstacles(self.obstacles, self.score, self.explosions)
            update_explosions(self.explosions)
            self.check_collisions()
            self.score += 1
        elif self.game_state == GameState.GAME_OVER:
            if pyxel.btnp(pyxel.KEY_RETURN):
                self.setup()
                self.game_state = GameState.PLAYING

    def check_collisions(self):
        player_box = (self.player.x, self.player.y, self.player.width, self.player.height)
        for obs in self.obstacles:
            obs_box = (obs.x, obs.y, obs.width, obs.height)
            if (player_box[0] < obs_box[0] + obs_box[2] and
                player_box[0] + player_box[2] > obs_box[0] and
                player_box[1] < obs_box[1] + obs_box[3] and
                player_box[1] + player_box[3] > obs_box[1]):
                self.game_state = GameState.GAME_OVER
                pyxel.play(0, 0)
        
        for exp in self.explosions:
            exp_box = (exp.x, exp.y, exp.width, exp.height)
            if (player_box[0] < exp_box[0] + exp_box[2] and
                player_box[0] + player_box[2] > exp_box[0] and
                player_box[1] < exp_box[1] + exp_box[3] and
                player_box[1] + player_box[3] > exp_box[1]):
                self.game_state = GameState.GAME_OVER
                pyxel.play(0, 0)

    def draw(self):
        pyxel.cls(12)

        ground_y = pyxel.height - 16
        for x in range(0, pyxel.width, 8):
            pyxel.blt(x, ground_y, 0, 0, 8, 8, 8) # Grass tile
            pyxel.blt(x, ground_y + 8, 0, 8, 8, 8, 8) # Dirt tile

        self.player.draw()

        if self.game_state == GameState.TITLE:
            title_text = "Dodge - it !"
            title_text_width = len(title_text) * 4
            box_x = pyxel.width / 2 - title_text_width / 2 - 5
            box_y = 100 - 5
            box_width = title_text_width + 10
            box_height = 8 + 10
            pyxel.rect(box_x, box_y, box_width, box_height, 1)
            pyxel.text(pyxel.width / 2 - title_text_width / 2, 100, title_text, 7)
            press_enter_text = "Press Enter"
            press_enter_text_width = len(press_enter_text) * 4
            pyxel.text(pyxel.width / 2 - press_enter_text_width / 2, 120, press_enter_text, 7)
        else:
            for obs in self.obstacles:
                obs.draw()

            for exp in self.explosions:
                exp.draw()

            score_text = f"Score: {self.score}"
            pyxel.text(5, 5, score_text, 7)

            if self.game_state == GameState.GAME_OVER:
                text_width = len("GAME OVER") * 4
                pyxel.text(pyxel.width / 2 - text_width / 2, 110, "GAME OVER", 8)
                restart_text = "Press Enter to Restart"
                text_width = len(restart_text) * 4
                pyxel.text(pyxel.width / 2 - text_width / 2, 125, restart_text, 7)
