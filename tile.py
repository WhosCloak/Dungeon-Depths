import pygame as pg


class Tile:
    def __init__(self, pos: pg.Vector2, image: pg.Surface, name: str):
        self.name = name
        self.image = image
        self.rect = image.get_frect(bottomleft=pos)

    def draw(self, screen, camera):
        draw_rect = self.rect.move(-camera)
        if screen.get_rect().colliderect(draw_rect):
            screen.blit(self.image, draw_rect)