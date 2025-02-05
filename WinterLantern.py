import pygame as pg
from axis import Axis

# Winter Lantern Class
class Enemy2:
    def __init__(self, game, pos) -> None:
        self.game = game
        self.frames = [
            pg.image.load("sprites/WLidle.png").convert_alpha(),
            pg.image.load("sprites/WLmove.png").convert_alpha()
        ]
        self.image = self.frames[0]
        self.rect = self.image.get_frect(bottomright=pos)
        self.speed = 15
        self.velocity = pg.Vector2()
        self.radius = 100
        self.health = 1000
        self.damage = 10

        self.current_frame = 0
        self.frame_duration = 300 
        self.last_frame_time = pg.time.get_ticks()
        self.death_sound = pg.mixer.Sound("audio/enemydeath.mp3")
        self.death_sound.set_volume(1.0)

    # Enemy Chasing the Player
    def move_towards_target(self, target_pos):
        distance_to_target = target_pos.distance_to(self.rect.center)
        if distance_to_target < self.radius:
            direction = (target_pos - pg.Vector2(self.rect.center)).normalize()
            self.velocity = direction * self.speed * self.game.dt
            self.rect.x += self.velocity.x
            self.check_collision(Axis.X)
            self.rect.y += self.velocity.y
            self.check_collision(Axis.Y)

    # Enemy Collisions
    def check_collision(self, axis: Axis):
        for tile in self.game.wall_tiles:
            if not self.rect.colliderect(tile.rect):
                continue

            if axis == Axis.X:
                if self.velocity.x > 0:
                    self.rect.right = tile.rect.left
                elif self.velocity.x < 0:
                    self.rect.left = tile.rect.right
                self.velocity.x = 0
            elif axis == Axis.Y:
                if self.velocity.y > 0:
                    self.rect.bottom = tile.rect.top
                elif self.velocity.y < 0:
                    self.rect.top = tile.rect.bottom
                self.velocity.y = 0
            break

    # Enemy Animations
    def animate(self):
        current_time = pg.time.get_ticks()
        if current_time - self.last_frame_time > self.frame_duration:
            self.last_frame_time = current_time

            self.current_frame = (self.current_frame + 1) % 2
            self.image = self.frames[self.current_frame]


    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.die()


    def die(self):
        self.game.enemies.remove(self)
        self.death_sound.play()

    def draw(self):
        self.game.screen.blit(self.image, self.rect.move(-self.game.camera))

    def update(self, target_pos):
        self.move_towards_target(target_pos)
        self.animate()
        self.draw()
