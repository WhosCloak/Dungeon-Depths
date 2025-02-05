import pygame as pg
from pytmx import TiledMap
from tile import Tile
from settings import TILE_WIDTH, TILE_HEIGHT

def load_tmx_layer(
    data: TiledMap,
    layer_name: str,
    targets: tuple[list, ...] | list,
) -> None:
    if isinstance(targets, tuple) and not targets:
        return

    layers = [
        layer
        for layer in data.visible_layers
        if hasattr(layer, "data")
        and layer.name == layer_name
    ]
    
    if not layers:
        print(f"ERROR: Layer '{layer_name}' not found in '{data.filename}'")
        return

    for layer in layers:
        for x, y, surface in layer.tiles():
            if surface is None:
                continue

            pos = pg.Vector2(x * TILE_WIDTH, y * TILE_HEIGHT)
            tile = Tile(pos, surface, layer_name)
            if isinstance(targets, list):
                targets.append(tile)
            else:
                for target in targets:
                    target.append(tile)