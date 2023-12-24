import pygame as pg
import math
import settings as settings

class RayCasting:
    def __init__(self, game) -> None:
        self.game = game
    
    def ray_cast(self):
        ox, oy = self.game.player.pos
        x_map, y_map = self.game.player.map_pos
        ray_angle = self.game.player.angle - settings.HALF_FOV + 0.0001
        for ray in range (settings.NUM_RAYS):
            sin_a = math.sin(ray_angle)
            cos_a = math.cos(ray_angle)

            # horizontals
            y_hor, dy = (y_map+1, 1) if sin_a>0 else (y_map-1E-6, -1)
            depth_hor = (y_hor-oy)/sin_a
            x_hor = ox + depth_hor * cos_a
            delta_depth = dy / sin_a
            dx = delta_depth * cos_a
            for i in range(settings.MAX_DEPTH):
                tile_hor = int(x_hor), int(y_hor)
                if tile_hor in self.game.map.world_map:
                    break
                x_hor += dx
                y_hor += dy
                depth_hor += delta_depth



            # verticals
            x_vert, dx = (x_map+1,1) if cos_a>0 else (x_map-1E-6, -1)
            depth_vert = (x_vert - ox)/cos_a
            y_vert = oy + depth_vert * sin_a
            delta_depth = dx/cos_a
            dy = delta_depth*sin_a
            for i in range(settings.MAX_DEPTH):
                tile_vert = int(x_vert), int(y_vert)
                if tile_vert in self.game.map.world_map:
                    break
                x_vert += dx
                y_vert += dy
                depth_vert += delta_depth

            depth = min(depth_vert, depth_hor)
            
            pg.draw.line(
                surface=self.game.screen,
                color='yellow',
                start_pos=(100*ox,100*oy),
                end_pos=(100*(ox+depth*cos_a), 100*(oy+depth*sin_a)),
                width=2,
            )

            ray_angle += settings.DELTA_ANGLE


    def update(self):
        self.ray_cast()


def Main():
    pass

if __name__=="__main__":
    Main()