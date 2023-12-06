#  A simple platformer game built by Gabe Holmes
#  This is the main event loop, run this file to run the game
#
from controller import *
from level import Level
from settings import *
import pygame

# Level strings
main = main_level

main_controller = Controller([main])
main_controller.run()

