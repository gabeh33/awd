import pygame
from support import import_folder
from settings import tile_size


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, tile_type='grass', is_goal=False):
        super().__init__()
        self.graphics = {}
        self.import_character_assets()
        self.image = self.graphics[tile_type][0]

        self.image = pygame.transform.scale(self.image, (tile_size, tile_size))
        self.rect = self.image.get_rect(topleft=pos)
        self.isGoal = is_goal

    def import_character_assets(self):
        character_path = '../res/main/Terrain/'  # /res/main/Main Characters/Virtual Guy/
        self.graphics = {'grass': [],
                         'goal': []}

        for img in self.graphics.keys():
            full_path = character_path + img
            self.graphics[img] = import_folder(full_path)

    def update(self, x_shift, y_shift):
        """
        Shifts this given tile to the left or right
        :param x_shift: The direction and amount to shift the Tile
        """
        self.rect.x += x_shift
        self.rect.y += y_shift

