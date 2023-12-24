import pygame as pg
import settings as settings
import map as map
import raycasting as raycasting
import object_renderer as object_renderer
import player as player
import sys

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode(size=settings.RES)
        self.clock = pg.time.Clock()
        self.delta_time = 1
        self.new_game()

    def new_game(self):
        self.map = map.Map(game=self)
        self.player = player.Player(game=self)
        self.object_renderer = object_renderer.ObjectRenderer(game=self)
        self.raycasting = raycasting.RayCasting(game=self)

    def update(self):
        self.player.update()
        self.raycasting.update()
        pg.display.flip()
        self.delta_time = self.clock.tick(settings.FPS)
        pg.display.set_caption(title = f'MY MAZE, framerate: {self.clock.get_fps():0.1f}')
    
    def draw(self):
        self.screen.fill(color='black')
        self.object_renderer.draw()
        # self.map.draw()
        # self.player.draw()

    def check_events(self):
        for event in pg.event.get():
            if (event.type == pg.QUIT) or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()

    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()

def Main():
    game = Game()
    game.run()

if __name__=="__main__":
    Main()