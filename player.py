import settings as settings
import pygame as pg
import math

class Player:
    def __init__(self, game):
        self.game = game
        self.x, self.y = settings.PLAYER_POS
        self.angle = settings.PLAYER_ANGLE
    
    def movement(self):
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        dx, dy = 0, 0
        speed = settings.PLAYER_SPEED * self.game.delta_time
        speed_sin = speed * sin_a
        speed_cos = speed * cos_a
        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            dx += speed_cos
            dy += speed_sin
        if keys[pg.K_s]:
            dx += -speed_cos
            dy += -speed_sin
        if keys[pg.K_a]:
            dx += speed_sin
            dy += -speed_cos
        if keys[pg.K_d]:
            dx += -speed_sin
            dy += +speed_cos
        
        # self.x += dx
        # self.y += dy
        self.update_pos_with_collision_check(dx, dy)

        if keys[pg.K_LEFT]:
            self.angle -= settings.PLAYER_ROT_SPEED*self.game.delta_time
        if keys[pg.K_RIGHT]:
            self.angle += settings.PLAYER_ROT_SPEED*self.game.delta_time

        self.angle %= math.tau #math.tau = 2*math.pi

    def check_collision(self, x, y):
        return (x, y) in self.game.map.world_map
    
    def update_pos_with_collision_check(self, dx, dy):
        if not self.check_collision(int(self.x+dx), int(self.y)):
            self.x += dx
        if not self.check_collision(int(self.x), int(self.y+dy)):
            self.y += dy


    def draw(self):
        # pg.draw.line(
        #     surface=self.game.screen,
        #     color='green',
        #     start_pos=(self.x*100, self.y*100),
        #     end_pos=(self.x*100+settings.WIDTH*math.cos(self.angle), self.y*100+settings.WIDTH*math.sin(self.angle)),
        #     width=2,
        # )
        pg.draw.circle(
            surface=self.game.screen,
            color='yellow',
            center=(self.x*100, self.y*100),
            radius = 10,
            width = 10
        )


    def update(self):
        self.movement()

    @property
    def pos(self):
        return self.x, self.y
    
    @property
    def map_pos(self):
        return int(self.x), int(self.y)


def Main():
    pass

if __name__=="__main__":
    Main()