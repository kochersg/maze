import pygame as pg
import settings as settings
import math

class MapView:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.map = game.map
        self.player = game.player

    def draw(self):
        self.draw_map_canvas()
        self.draw_walls()
        self.draw_player()

    def draw_player(self):
        player_map_pos = (
                self.player.pos[0]*settings.MAP_VIEW_TILE_SCALE + settings.MAP_VIEW_XO,
                self.player.pos[1]*settings.MAP_VIEW_TILE_SCALE + settings.MAP_VIEW_YO
            )
        r_sin_a = settings.MAP_VIEW_PLAYER_RAY_LENGTH * math.sin(self.player.angle)
        r_cos_a = settings.MAP_VIEW_PLAYER_RAY_LENGTH * math.cos(self.player.angle)
        ray_end_pos = (
            player_map_pos[0]+r_cos_a,
            player_map_pos[1]+r_sin_a
        )
        pg.draw.circle(
            surface=self.screen,
            color='yellow',
            center= player_map_pos,
            radius=settings.MAP_VIEW_TILE_SCALE//4
        )
        pg.draw.line(
            surface=self.screen,
            color='red',
            start_pos= player_map_pos,
            end_pos=ray_end_pos
        )


    def draw_walls(self):
        for tile in self.map.world_map:
            pg.draw.rect(
                surface=self.screen,
                color='darkgray',
                rect=(
                    tile[0]*settings.MAP_VIEW_TILE_SCALE+settings.MAP_VIEW_XO,
                    tile[1]*settings.MAP_VIEW_TILE_SCALE+settings.MAP_VIEW_YO,
                    settings.MAP_VIEW_TILE_SCALE,
                    settings.MAP_VIEW_TILE_SCALE
                ),
                width=1
            )

    def draw_map_canvas(self):
        pg.draw.rect(
            surface=self.screen,
            color = (200,200,255),
            rect = (
                settings.MAP_VIEW_XO-2,
                settings.MAP_VIEW_YO-2,
                settings.MAP_VIEW_XS+4,
                settings.MAP_VIEW_YS+4
            ),
            width=2
        )
        pg.draw.rect(
            surface=self.screen,
            color = (0, 0, 50),
            rect = (
                settings.MAP_VIEW_XO,
                settings.MAP_VIEW_YO,
                settings.MAP_VIEW_XS,
                settings.MAP_VIEW_YS
            ),
        )
        



def Main():
    pass

if __name__=="__main__":
    Main()