import pygame as pg
from settings import SCN_SIZE
from axis import Axis


# Sword Effects Class
class AttackEffect:
    def __init__(self, position):
        self.image = pg.image.load("sprites/sword_slash.png").convert_alpha()
        self.rect = self.image.get_rect(center=position)
        self.lifetime = 200
        self.start_time = pg.time.get_ticks()

    def update(self):
        current_time = pg.time.get_ticks()
        return current_time - self.start_time <= self.lifetime

    def draw(self, screen, camera):
        screen.blit(self.image, self.rect.move(-camera))


# Player Class
class Player:
    def __init__(self, game) -> None:
        self.game = game
        self.image = pg.image.load("sprites/mainidle.png").convert_alpha()
        self.init_position = pg.Vector2(100, 250)
        self.rect = self.image.get_rect(center=self.init_position)
        self.draw_rect = self.image.get_frect(center=self.init_position)
        self.speed = 100
        self.velocity = pg.Vector2()
        self.health = 100
        self.damage = 25
        self.attack_range = 50
        self.attack_cooldown = 10
        self.last_attack_time = 0
        self.sword_sound = pg.mixer.Sound("audio/sword.mp3")
        self.footstep_sound = pg.mixer.Sound("audio/footsteps.mp3")
        self.is_moving = False
        self.effects = []

    # Player Movement
    def move(self):
        direction = pg.Vector2(
            self.game.keys[pg.K_d] - self.game.keys[pg.K_a],
            self.game.keys[pg.K_s] - self.game.keys[pg.K_w]
        )
        if direction.length() > 0:
            direction.normalize_ip()

        self.velocity = direction * self.speed * self.game.dt
        self.rect.x += self.velocity.x
        self.handle_collision(Axis.X)
        self.rect.y += self.velocity.y
        self.handle_collision(Axis.Y)

        self.draw_rect.center = self.rect.center
        self.game.camera = self.rect.center - pg.Vector2(SCN_SIZE) / 2
      
        if self.velocity.length() > 0:
            if not self.is_moving:
                self.footstep_sound.play(loops=-1)  
                self.is_moving = True
        else:
            if self.is_moving:
                self.footstep_sound.stop() 
                self.is_moving = False
    # Player Collisions
    def handle_collision(self, axis: Axis):
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
    # Player Attack
    def attack(self):
        current_time = pg.time.get_ticks()
        if self.game.keys[pg.K_f] and current_time - self.last_attack_time >= self.attack_cooldown:
            self.last_attack_time = current_time
            self.sword_sound.play()
            attack_rect = self.rect.inflate(self.attack_range, self.attack_range)
            effect_position = self.rect.center + pg.Vector2(self.attack_range, 0)
            self.effects.append(AttackEffect(effect_position))

            for enemy in self.game.enemies:
                if attack_rect.colliderect(enemy.rect):
                    enemy.health -= self.damage
                    if enemy.health <= 0:
                        enemy.health = 0
                        enemy.die()
    # Player Animations
    def animate(self):
        if self.velocity.length() > 0:
            self.image = pg.image.load("sprites/mainwalk.png").convert_alpha()
        else:
            self.image = pg.image.load("sprites/mainidle.png").convert_alpha()

    # Ending the Game
    def check_end_door_collision(self):
        for tile in self.game.end_door:
            if self.rect.colliderect(tile.rect):
                print("Player reached the end door!")
                self.gameend()
                break

    # Victory Sound
    def gameend(self):
        print("Game Over - You Win!")
        victory_sound = pg.mixer.Sound("audio/victory.mp3")
        victory_sound.play()
        pg.time.delay(4500)
        pg.quit()
        exit()


    def draw(self):
        self.game.screen.blit(self.image, self.draw_rect.move(-self.game.camera))
        for effect in self.effects:
            effect.draw(self.game.screen, self.game.camera)

    def update(self):
        self.move()
        self.attack()
        self.animate()
        self.check_end_door_collision()
        self.effects = [effect for effect in self.effects if effect.update()]
        self.draw()
