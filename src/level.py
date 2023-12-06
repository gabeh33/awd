"""
Represents one level the player can play. Stores information about the player,
tiles on the screen, and GUI information. Takes in level information from
settings.py to create the level
"""
# TODO Add more of the actual informative information
# Bring back jumping
# Add in traps that relate to the content
#   - Normal Fault
#   - Glacier to climb
#   - Volcano

import enum
import sys

import pygame.freetype
from settings import *
from tiles import *
from player import Player, Guide
from support import import_folder, draw_background


class Level:
    def __init__(self, level_data, surface):
        pygame.init()
        self.player = None
        self.guide = None
        self.tiles = None
        self.goal_tile = None

        # Basic level setup
        self.display_surface = surface
        self.level_data = level_data

        self.world_shift = 0
        self.world_shift_y = 0

        self.graphics = {}
        self.vertical_offset = 0

        self.init_level(level_data)

        self.c_move_down = True
        self.c_move_up = True
        self.c_move_left = True
        self.c_move_right = True

        # Font stuff
        pygame.font.init()
        self.distance_travelled_right = 0
        self.font = pygame.font.Font("../res/fonts/joystix monospace.otf", 40)

    def init_level(self, layout):
        """
        Draws the tiles that make up the level according to the given layout
        :param layout: Array of strings that describe the layout of the level
        """
        self.tiles = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        self.guide = pygame.sprite.GroupSingle()

        for row_index, row in enumerate(layout):
            for col_index, cell in enumerate(row):

                x = col_index * tile_size
                y = row_index * tile_size
                if cell == 'X':
                    tile = Tile((x, y))
                    self.tiles.add(tile)
                elif cell == 'P':
                    player = Player((x, y))
                    self.player.add(player)
                elif cell == 'G':
                    ice = Tile((x,y), tile_type="goal")
                    self.tiles.add(ice)

    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x
        normal_speed = 5
        testing_speed = 30
        if player_x < screen_width / 4 and direction_x < 0:
            self.world_shift = normal_speed
            self.distance_travelled_right -= normal_speed
            player.speed = 0
        elif player_x > screen_width - (screen_width / 4) and direction_x > 0:
            self.world_shift = -normal_speed
            self.distance_travelled_right += normal_speed
            player.speed = 0
        else:
            self.world_shift = 0
            player.speed = normal_speed

    def scroll_y(self):
        player = self.player.sprite
        player_y = player.rect.centery
        direction_y = player.direction.y

        if direction_y < 0 and player_y >= 500:
            self.world_shift_y = -5
            player.speed = 0
        elif direction_y > 0 and player_y <= 100:
            self.world_shift_y = 5
            player.speed = 0
        else:
            self.world_shift_y = 0
            self.player.speed = 5

    def horizontal_movement_collision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                # If our player collides with any tile in the level, check its direction first
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left

    def vertical_movement_collision(self):
        player = self.player.sprite
        player.apply_gravity()

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                # If our player collides with any tile in the level, check its direction first
                if player.direction.y > 0:
                    # Standing on top of a tile
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0

                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0

    def horizontal_movement_collision_old(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed
        player.rect.y += player.direction.y * -1 * player.speed
        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                # If our player collides with any tile in the level, check its direction first
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left
                elif player.direction.y > 0:
                    player.rect.top = sprite.rect.bottom
                elif player.direction.y < 0:
                    player.rect.bottom = sprite.rect.top

    def import_character_assets(self):
        character_path = '../res/main/Menu/'  # ../res/character/
        self.graphics = {'gui': [],
                         'gui_background': []}

        for animation in self.graphics.keys():
            full_path = character_path + animation
            self.graphics[animation] = import_folder(full_path)

    def draw_messages(self):
        # This is going to display a series of messages, based on how far right the player has moved
        title_size = 40
        white = (255, 255, 255)

        # Title screen, from start to 2000
        # "Gabe's Iceland Game", black)
        '''        
        if self.distance_travelled_right < 1200:
            self.draw_message_helper("Thanks for coming along on this adventure!", -65, text_size=28)
            self.draw_message_helper("Hope to see you again soon...", -37, text_size=28)
            self.draw_message_helper("In the meantime feel free to explore the glacier!", -9, text_size=28)
        '''

        if self.distance_travelled_right < 1200:
            self.draw_message_helper("Gabe's Iceland Adventure", text_size=title_size)
        elif self.distance_travelled_right < 1900:
            self.draw_message_helper("Keep traveling right to arrive in Iceland!!")
        elif self.distance_travelled_right < 2600:
            self.draw_message_helper("But first we need to learn a")
            self.draw_message_helper("little about the land of fire and ice", 25)
        elif self.distance_travelled_right < 3300:
            self.draw_message_helper("Iceland sits on the mid-atlantic ridge, between the", -30)
            self.draw_message_helper("North American tectonic plate and Eurasian tectonic plate", -5)
            self.draw_image_helper("../res/diagrams/ride_diagram.png", scale_by=(0.4, 0.34))
        elif self.distance_travelled_right < 4000:
            self.draw_message_helper("When two plates are separating like this,", -60)
            self.draw_message_helper("it is called a divergent plate boundary", -35)
            self.draw_image_helper("../res/diagrams/divergent_plates.png", scale_by=(1.2, 1.2), vertical_addon=-80)
            self.draw_message_helper("This can lead to large amounts of volcanic activity", 360)
            self.draw_message_helper("as magma is able to reach the surface more easily", 385)
        elif self.distance_travelled_right < 4700:
            self.draw_message_helper("This type of plate movement also leads to faults... NORMAL FAULTS!!", -60,
                                     text_size=22)
            self.draw_message_helper("(Normal faults are very exciting)", -35, text_size=22)
            self.draw_image_helper("../res/diagrams/nomal_fault_1.jpeg", scale_by=(0.4), vertical_addon=-80,
                                   x_shift=-375)
            self.draw_image_helper("../res/diagrams/normal_fault_2.jpeg", scale_by=(0.35), vertical_addon=-80,
                                   x_shift=375)
            self.draw_image_helper("../res/diagrams/normal_fault_diagram.pbm", scale_by=(0.6), vertical_addon=-80,
                                   x_shift=0)
            self.draw_message_helper("Normal faults happen when one plate slides down and away from another", 360,
                                     text_size=20)
            self.draw_message_helper("Make sure to remember not to get stuck in one on your journey!!", 385,
                                     text_size=20)
        elif self.distance_travelled_right < 5400:
            self.draw_message_helper("But that's enough learning for now...", text_size=35)
            self.draw_message_helper("lets get on a plane and travel there!!", 35, text_size=35)
        # 5400 to 6000 take off
        # 6000 to 6600 landing
        elif 6600 < self.distance_travelled_right < 7300:
            self.draw_message_helper("Welcome to Iceland!!", 50)
            self.draw_message_helper("We will start our journey on the Reykjanes Peninsula", 75)
            self.draw_message_helper("This is where all travelers start their journey,", 100)
            self.draw_message_helper("and is a very geologically active zone", 125)
        elif 7300 < self.distance_travelled_right < 8000:
            self.draw_message_helper("We will be traveling to the town of Grindivik", 100)
            self.draw_message_helper("There has been a lot of seismic activity there recently", 125)
            self.draw_message_helper("Remember normal faults??", 150)
            self.draw_message_helper("(Accurate as of December 2023)", 175)
        elif 8000 < self.distance_travelled_right < 8700:
            self.draw_message_helper("Grindivik is currently facing an imminent threat of volcanic eruption", 48,
                                     text_size=20, color=(255, 255, 255))
            self.draw_message_helper("On November 10th, residents were forced to evacuate", 68, text_size=20,
                                     color=(255, 255, 255))
        elif 8700 < self.distance_travelled_right < 9185:
            self.draw_message_helper("Seismic activity such as earthquakes and fissures are", -65,
                                     text_size=20)
            self.draw_message_helper("signs that an eruption could happen soon ", -45,
                                     text_size=20)
            self.draw_message_helper("These fissures are caused by plates moving away from each other", -25,
                                     text_size=20)
            self.draw_message_helper("allowing room for magma to reach the surface...", -5,
                                     text_size=20)
            self.draw_message_helper("Remember what that is called?", 15,
                                     text_size=20)
        elif 9185 <= self.distance_travelled_right < 9875:
            self.draw_message_helper("Jump over the normal fault!!", text_size=40)
        elif 9875 <= self.distance_travelled_right < 11000:
            self.draw_message_helper("Nice job!")
            self.draw_message_helper("That wraps up our time on the Reykjanes Peninsula", 25)
            self.draw_message_helper("We will now be heading along the southern cost", 50)
            self.draw_message_helper("To Iceland's biggest glacier...", 75)
        elif 11000 <= self.distance_travelled_right <= 11700:
            self.draw_message_helper("Vatnajökull!!", text_size=60)
        elif 11700 <= self.distance_travelled_right <= 12400:
            self.draw_message_helper("Vatnajökull is the not only the largest glacier", -85)
            self.draw_message_helper("in Iceland, but the largest in Europe!!", -60)
            self.draw_message_helper("Ice tours provide a significant source of", -35)
            self.draw_message_helper("revenue for the locals", -10)
        elif 12400 <= self.distance_travelled_right <= 13100:
            self.draw_message_helper("But this may not always be possible", -65)
            self.draw_message_helper("Climate change has accelerated the rate at which", -40)
            self.draw_message_helper("Vatnajökull loses mass through melting", -15)
            self.draw_message_helper("(Pictures here is one of its glacial lagoons)", 10)
        elif 13100 <= self.distance_travelled_right <= 13800:
            self.draw_message_helper("Here is a diagram showing the ice line in 1973 (dark blue)", -65, text_size=22,
                                     color=white)
            self.draw_message_helper("Compared to the ice line in 2016 (light blue)", -40, text_size=22, color=white)
        elif 13800 <= self.distance_travelled_right <= 14500:
            self.draw_message_helper("That means we need to enjoy the beauty", -65, text_size=22, color=white)
            self.draw_message_helper("and not contribute to speeding up the rate of melting", -40, text_size=22,
                                     color=white)
        elif 14500 < self.distance_travelled_right:
            self.draw_message_helper("Thanks for coming along on this adventure!", -65, text_size=28)
            self.draw_message_helper("Hope to see you again soon...", -37, text_size=28)
            self.draw_message_helper("In the meantime feel free to explore the glacier!", -9, text_size=28)

    def draw_message_helper(self, text_string, vertical_addon=0, text_size=25, color=(0, 0, 0, 0)):
        # Draws the given message on the screen in the correct location
        # Default color is black
        center = (screen_width / 2, 100 + vertical_addon)
        self.font = pygame.font.Font("../res/fonts/joystix monospace.otf", text_size)
        surface = self.font.render(text_string, False, color)
        text_rect = surface.get_rect()
        text_rect.center = center
        self.display_surface.blit(surface, text_rect)

    def draw_image_helper(self, image_location, vertical_addon=0, scale_by=1, x_shift=0):
        center = ((screen_width / 2) + x_shift, 340 + vertical_addon)
        image = pygame.image.load(image_location).convert()
        image = pygame.transform.scale_by(image, scale_by)
        image_rect = image.get_rect()
        image_rect.center = center
        self.display_surface.blit(image, image_rect)

    def draw_background(self, img_path=background_image):
        img = pygame.image.load(img_path)
        self.display_surface.fill('black')

        width = 64
        height = 64
        for x in range(int(screen_width / width) + 1):
            for y in range(int(screen_height / height + 2)):
                self.display_surface.blit(img, (x * width, y * height + self.vertical_offset - 64))

    def run(self):
        # Background
        '''
        if self.distance_travelled_right < 8700:
            image = pygame.image.load("../res/backgrounds/vaten_beauty.jpeg").convert()
            image = pygame.transform.scale(image, (1200, 750))
            self.display_surface.blit(image, (0, 0))
        '''
        if self.distance_travelled_right < 5400 or (9875 <= self.distance_travelled_right < 11100):
            self.draw_background()
            self.vertical_offset = self.vertical_offset + background_scroll_speed if self.vertical_offset < 64 else 0
        elif self.distance_travelled_right < 6000:
            image = pygame.image.load("../res/backgrounds/airport_leaving.jpeg").convert()
            image = pygame.transform.scale(image, (1200, 750))
            self.display_surface.blit(image, (0, 0))
        elif self.distance_travelled_right < 6600:
            image = pygame.image.load("../res/backgrounds/airport_landing.png").convert()
            image = pygame.transform.scale(image, (1200, 750))
            self.display_surface.blit(image, (0, 0))
        elif self.distance_travelled_right < 7300:
            image = pygame.image.load("../res/backgrounds/rey_pen.png").convert()
            image = pygame.transform.scale(image, (1200, 750))
            self.display_surface.blit(image, (0, 0))
        elif self.distance_travelled_right < 8000:
            image = pygame.image.load("../res/backgrounds/grindivik_onmap.png").convert()
            image = pygame.transform.scale(image, (1200, 750))
            self.display_surface.blit(image, (0, 0))
        elif self.distance_travelled_right < 8700:
            image = pygame.image.load("../res/backgrounds/grindivik_fissure.jpeg").convert()
            image = pygame.transform.scale(image, (1200, 750))
            self.display_surface.blit(image, (0, 0))
        elif self.distance_travelled_right < 9875:
            image = pygame.image.load("../res/backgrounds/grin_fissure_2.jpeg").convert()
            image = pygame.transform.scale(image, (1200, 750))
            self.display_surface.blit(image, (0, 0))
        elif 11000 < self.distance_travelled_right < 11700:
            image = pygame.image.load("../res/backgrounds/vaten_map.jpeg").convert()
            image = pygame.transform.scale(image, (1200, 750))
            self.display_surface.blit(image, (0, 0))
        elif 11700 < self.distance_travelled_right < 12400:
            image = pygame.image.load("../res/backgrounds/vaten_ice.jpeg").convert()
            image = pygame.transform.scale(image, (1200, 750))
            self.display_surface.blit(image, (0, 0))
        elif 12400 < self.distance_travelled_right < 13100:
            image = pygame.image.load("../res/backgrounds/vaten_lagoon.jpeg").convert()
            image = pygame.transform.scale(image, (1200, 750))
            self.display_surface.blit(image, (0, 0))
        elif 13100 < self.distance_travelled_right <= 13800:
            image = pygame.image.load("../res/backgrounds/vaten_academic.png").convert()
            image = pygame.transform.scale(image, (1200, 750))
            self.display_surface.blit(image, (0, 0))
        elif 13800 < self.distance_travelled_right <= 14500:
            image = pygame.image.load("../res/backgrounds/vaten_beauty.jpeg").convert()
            image = pygame.transform.scale(image, (1200, 750))
            self.display_surface.blit(image, (0, 0))
        elif 14500 < self.distance_travelled_right:
            image = pygame.image.load("../res/backgrounds/vaten_beauty.jpeg").convert()
            image = pygame.transform.scale(image, (1200, 750))
            self.display_surface.blit(image, (0, 0))

        # Level Tiles
        self.tiles.update(self.world_shift, self.world_shift_y)
        self.tiles.draw(self.display_surface)
        # GUI Stuff

        # PLayer Group
        self.player.update()  # Updates to check if the player should move
        # self.guide.sprite.update_pos(self.player.sprite.pos)
        self.horizontal_movement_collision()  # Check for horizontal collisions
        self.vertical_movement_collision()  # Check for vertical collisions
        # self.collision_detection()
        self.player.draw(self.display_surface)  # Draw the player
        self.draw_messages()

        # self.guide.draw(self.display_surface)
        # 879, 641 is the rect pos of the player before jump over fault

        # print(f"Distance right: {self.distance_travelled_right}")
        # print(f"position: {self.player.sprite.rect.x}, {self.player.sprite.rect.y}")
        if self.player.sprite.rect.y > 700:
            self.player.sprite.rect.x = 879
            self.player.sprite.rect.y = 641
            print("fell")
        #sys.exit()
        self.scroll_x()


class ButtonType(enum.Enum):
    Left = 1
    Space = 2
    Right = 3
