import pygame as pg
import settings as settings

class ObjectRenderer:
    def __init__(self, game) -> None:
        self.game = game
        self.screen = game.screen
        self.wall_textures = self.load_wall_textures()
    
    def draw(self):
        self.render_game_objects()

    def render_game_objects(self):
        list_objects = self.game.raycasting.objects_to_render
        for depth, image, pos in list_objects:
            self.screen.blit(image, pos)

    @staticmethod
    def get_texture(path, res=(settings.TEXTURE_SIZE, settings.TEXTURE_SIZE))->pg.Surface:
        texture = pg.image.load(path).convert_alpha()
        return pg.transform.scale(texture,res)
    
    def load_wall_textures(self):
        return {
            1: self.get_texture('ressources/textures/texture_1.png'),
            2: self.get_texture('ressources/textures/texture_2.png'),
            3: self.get_texture('ressources/textures/texture_3.png'),
        }


def Main():
    pass

if __name__=="__main__":
    Main()