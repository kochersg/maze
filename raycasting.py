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
            depth_hor = self.ray_cast_horizontal(ox, oy, y_map, sin_a, cos_a)
            # verticals
            depth_vert = self.ray_cast_vertical(ox, oy,x_map, sin_a, cos_a)
            depth = min(depth_vert, depth_hor)

            # remove fishbowl effect
            depth *= math.cos(self.game.player.angle - ray_angle) 
            
            # pg.draw.line(
            #     surface=self.game.screen,
            #     color='yellow',
            #     start_pos=(100*ox,100*oy),
            #     end_pos=(100*(ox+depth*cos_a), 100*(oy+depth*sin_a)),
            #     width=2,
            # )

            # projection
            proj_height = settings.SCREEN_DIST / (depth + 0.0001) 
            # draw walls

            wall_color = [230 / (1+depth**5*0.0003)] * 3
            pg.draw.rect(
                surface=self.game.screen,
                color = wall_color,
                rect=(
                    ray*settings.SCALE, 
                    settings.HALF_HEIGHT - proj_height // 2,
                    settings.SCALE,
                    proj_height
                )
            )

            ray_angle += settings.DELTA_ANGLE

    def calc_depth(self, x:float, y:float, dx: float, dy:float, depth: float, delta_depth:float) -> float:
        for _ in range(settings.MAX_DEPTH):
            tile_vert = int(x), int(y)
            if tile_vert in self.game.map.world_map:
                break
            x += dx
            y += dy
            depth += delta_depth
        return depth

    def ray_cast_vertical(self, ox:int, oy:int, x_map: int, sin_a: float, cos_a: float)->float:
        x_vert, dx = (x_map+1,1) if cos_a>0 else (x_map-1E-6, -1)
        depth_vert = (x_vert - ox)/cos_a
        y_vert = oy + depth_vert * sin_a
        delta_depth = dx/cos_a
        dy = delta_depth*sin_a
        return self.calc_depth(x_vert, y_vert, dx, dy, depth_vert, delta_depth)

    def ray_cast_horizontal(self, ox: float, oy: float, y_map:int, sin_a: float, cos_a: float)->float:
        y_hor, dy = (y_map+1, 1) if sin_a>0 else (y_map-1E-6, -1)
        depth_hor = (y_hor-oy)/sin_a
        x_hor = ox + depth_hor*cos_a
        delta_depth = dy/sin_a
        dx = delta_depth*cos_a
        return self.calc_depth(x_hor, y_hor, dx, dy, depth_hor, delta_depth)


    def update(self):
        self.ray_cast()


def Main():
    pass

if __name__=="__main__":
    Main()