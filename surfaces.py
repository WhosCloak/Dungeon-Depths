import pygame as pg

image_load = pg.image.load

def load_anim(path, width, height):
    anim_surf = pg.image.load(path).convert_alpha()
    anim_list = [
        anim_surf.subsurface((x, 0, width, height))
        for x in range(0, anim_surf.width, width)
    ]
    return anim_list