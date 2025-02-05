import pygame as pg

from utils import load_tmx_layer
from pytmx import load_pygame
from settings import *
from player import Player
from Inky import Enemy
from WinterLantern import Enemy2

pg.mixer.init()


# Game Class
class Game:
    def __init__(self) -> None:
        pg.init()
        pg.display.set_caption("Dungeon Depths")
        self.screen = pg.display.set_mode(SCN_SIZE, pg.SCALED)
        self.clock = pg.Clock()
        self.running = True
        self.dt = 0
        self.keys = {}

        # Tile Map Load 
        tile_map = load_pygame("assets/dungeondepths.tmx")
        self.floor_tiles = []
        self.wall_tiles = []
        self.torch_tiles = []
        self.end_door = []
        self.enemy_spawn = []
        load_tmx_layer(tile_map, "floor", self.floor_tiles)
        load_tmx_layer(tile_map, "wall", self.wall_tiles)
        load_tmx_layer(tile_map, "torch", self.torch_tiles)
        load_tmx_layer(tile_map, "enemy_spawn", self.enemy_spawn)
        load_tmx_layer(tile_map, "end_door", self.end_door)

        self.camera = pg.Vector2()
        self.player = Player(self)
        self.enemies = self.spawn_enemies()
    # Enemy Spawner
    def spawn_enemies(self):
        enemies = []
        for i, enemy_spawn in enumerate(self.enemy_spawn):
            pos = pg.Vector2(enemy_spawn.rect.topleft)
            if i % 2 == 0:
                # Spawn Enemy type 1 (Inky)
                enemies.append(Enemy(self, pos))
            else:
                # Spawn Enemy type 2 (Winter Lantern)
                enemies.append(Enemy2(self, pos))
        return enemies
   # Window Loop
    def run(self):
        while self.running:
            self.dt = self.clock.tick(60) / 1000
            self.keys = pg.key.get_pressed()
            
            for ev in pg.event.get():
                if ev.type == pg.QUIT:
                    self.running = False
                elif ev.type == pg.KEYDOWN:
                    if ev.key == pg.K_ESCAPE:
                        self.running = False

            self.screen.fill("black")
            for tile in self.floor_tiles + self.wall_tiles + self.torch_tiles + self.end_door:
                tile.draw(self.screen, self.camera)
            self.player.update()
            for enemy in self.enemies:
                enemy.update(pg.Vector2(self.player.rect.center))

            pg.display.flip()

# Background Music
#pg.mixer.music.load("audio/mainmenu.wav")
pg.mixer.music.set_volume(0.25)
#pg.mixer.music.play(-1, 0.0)

if __name__ == "__main__":
    Game().run()
