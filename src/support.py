from os import walk
from settings import *
import pygame.image


def import_folder(path):
    surface_list = []

    for _,_,img_files in walk(path):
        for image in img_files:
            full_path = path + '/' + image

            image_surface = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surface)

    return surface_list


def draw_background(screen, vertical_offset, img_path=background_image):
    vertical_offset = int(vertical_offset)
    img = pygame.image.load(img_path)
    screen.fill('black')

    width = 64
    height = 64
    for x in range(int(screen_width / width) + 1):
        for y in range(int(screen_height / height + 2)):
            screen.blit(img, (x * width, y * height + vertical_offset - 64))


def draw_background_horizontal(screen, horizontal_offset, img_path=blue_background):
    horizontal_offset = int(horizontal_offset)
    img = pygame.image.load(img_path)
    screen.fill('black')

    width = 64
    height = 64
    for x in range(int(screen_width / width) + 2):
        for y in range(int(screen_height / height) + 1):
            screen.blit(img, (x * width + horizontal_offset - 64, y * height))


