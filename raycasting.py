import pygame as pg
import math
import settings as settings

class RayCasting:
    def __init__(self, game) -> None:
        self.game = game
        self.ray_casting_result = []
        self.objects_to_render = []
        self.textures = self.game.object_renderer.wall_textures

    def get_objects_to_render(self):
        self.objects_to_render = []
        for ray, values in enumerate(self.ray_casting_result):
            depth, proj_height, texture, offset = values
            if proj_height < settings.HEIGHT:
                wall_column = self.textures[texture].subsurface(
                    offset * (settings.TEXTURE_SIZE-settings.SCALE), 0, settings.SCALE, settings.TEXTURE_SIZE
                )
                wall_column = pg.transform.scale(wall_column, (settings.SCALE, proj_height))
                wall_pos = (ray*settings.SCALE, settings.HALF_HEIGHT - proj_height // 2)
            else:
                texture_height = settings.TEXTURE_SIZE * settings.HEIGHT / proj_height
                wall_column = self.textures[texture].subsurface(
                    offset * (settings.TEXTURE_SIZE-settings.SCALE), settings.HALF_TEXTURE_SIZE - texture_height // 2,
                    settings.SCALE, texture_height
                )
                wall_column = pg.transform.scale(wall_column, (settings.SCALE, settings.HEIGHT))
                wall_pos = (ray*settings.SCALE, 0)
            self.objects_to_render.append((depth, wall_column, wall_pos))
            
    
    def ray_cast(self):
        self.ray_casting_result = []
        ox, oy = self.game.player.pos
        x_map, y_map = self.game.player.map_pos
        ray_angle = self.game.player.angle - settings.HALF_FOV + 0.0001
        for ray in range (settings.NUM_RAYS):
            texture_hor, texture_vert = 1, 1
            sin_a = math.sin(ray_angle)
            cos_a = math.cos(ray_angle)
            # horizontals
            y_hor, dy = (y_map+1, 1) if sin_a>0 else (y_map-1E-6, -1)
            depth_hor = (y_hor - oy)/sin_a
            x_hor = ox + depth_hor * cos_a
            delta_depth = dy/sin_a
            dx = delta_depth*cos_a
            for _ in range(settings.MAX_DEPTH):
                tile = int(x_hor), int(y_hor)
                if tile in self.game.map.world_map:
                    texture_hor = self.game.map.world_map[tile]
                    break
                x_hor += dx
                y_hor += dy
                depth_hor += delta_depth

            # verticals
            x_vert, dx = (x_map+1,  1) if cos_a>0 else (x_map-1E-6, -1)
            depth_vert = (x_vert - ox)/cos_a
            y_vert = oy + depth_vert * sin_a
            delta_depth = dx/cos_a
            dy = delta_depth*sin_a
            for _ in range(settings.MAX_DEPTH):
                tile = int(x_vert), int(y_vert)
                texture_vert = 1
                if tile in self.game.map.world_map:
                    texture_vert = self.game.map.world_map[tile]
                    break
                x_vert += dx
                y_vert += dy
                depth_vert += delta_depth

            if depth_vert < depth_hor:
                depth, texture = depth_vert, texture_vert
                y_vert %= 1
                offset = y_vert if cos_a > 0 else (1 - y_vert)
            else:
                depth, texture = depth_hor, texture_hor
                x_hor %= 1
                offset = (1 - x_hor) if sin_a > 0 else x_hor

            # remove fishbowl effect
            depth *= math.cos(self.game.player.angle - ray_angle) 
            
            # projection
            proj_height = settings.SCREEN_DIST / (depth + 0.0001) 
            # draw walls

            # ray casting results
            self.ray_casting_result.append((depth, proj_height, texture, offset))

            ray_angle += settings.DELTA_ANGLE

    def update(self):
        self.ray_cast()
        self.get_objects_to_render()


def Main():
    pass

if __name__=="__main__":
    Main()