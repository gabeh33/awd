main_level = [

    '                        ',
    '                        ',
    '                        ' + ' '*282             + '              GGGG         GGGGGGG    GGGGGGGGG                                                   GGGGGGGGGG GGGGG                                  ',
    '                        ' + ' '*282             + '               GGGG              GGGGGG          GGGGGGG                    GGGGGGG              GG               GGGG                           ',
    '                        ' + ' '*282             + '           GGGGGG GGGGG                     GGGGGG          GGGGG        GGGGG                GGGGG                     GGG                  ',
    '                        ' + ' '*282             + '                     GGGGG            GGGGGGG            GGGGGG         GGG            GGGGGGGGG                     GGGGGGGGG  GGGGGGGG                                     ',
    '                        ' + ' '*282             + '                              GGGG                            GGG     GGGGG     GGGGGG      GGGGGGG                GGGG                   ',
'                        ' + ' '*282             +     '     G                     GGGGGGGGGGGGGGG        GGGGG            GGGGG    GGGGG                               GGGG  ',
    '                        ' + ' '*282             + '       GGGGG            G        GGGGGGGG    GGG                GGGGGG              GGGGG                  GGGGGGGGGGGG                                      G',
    'X            ' + ' '*145 + ' XXX  ' + ' '*142 +   '    GGGGG  GGG      GGGGGG               GGGGGGGG         GGGG          GGGG              GGG            GGGGGGGGGG                                          G',
    'X          P ' + ' '*145 + 'XX      ' + ' '*140 + 'GGGGGGG        GGGGG     GGGGGGG                     GGGGG    GGG   GGGGGGGGG          GGGGGg     GGGGGGG                                                    G',
    'X'*158 + 'XX     X' + 'X'*100 + 'G'*40 +          'GGGGGGGGG  GGGGGGG GGGGGG   GGGGGGGGGGGGGGGGGGGGGGGGGG    GGGGG GGGGG      GGGGGGGGGGGGGGGGGGGGGGGGGGG' + 'G'*40,
]

tile_size = 64
# screen_width = len(basic_level[0]) * tile_size
screen_width = 1200
screen_height = min(tile_size * len(main_level), 800)
player_speed = 5
jump_cooldown = 0.75
background_scroll_speed = 0.5
gui_height = 160

background_image = '../res/main/Background/Brown.png'
blue_background = '../res/main/Background/Blue.png'
purple_background = '../res/main/Background/Purple.png'
yellow_background = '../res/main/Background/Yellow.png'

gui_image = '../res/main/Background/Gray.png'
character_info = '../res/main/Main Characters/Virtual Guy/'

# Layout information for the gui
left_right_center_offset = 150
distance_from_screen_height = 84
square_size = 64
dimensions = (square_size, square_size)
space_button_width = 128
left_pos = (screen_width / 2 - left_right_center_offset,
            screen_height - distance_from_screen_height)
space_pos = (screen_width / 2, screen_height - distance_from_screen_height)
right_pos = (screen_width / 2 + left_right_center_offset, screen_height - distance_from_screen_height)

# Menu layout dimensions
top_button_to_top_screen = 300
center_x = screen_width / 2
menu_button_width = 400
menu_button_height = 80
button_spacing = 150
