"""
Kaushal Bhingaradia
February 18, 2024

This file contains all the constants and config variables that are
accessed by the main game. These settings can be customized for
further tuning or making it challenging.
"""

# SCREEN SETUP
screen_width = 800
screen_height = 600
WHITE = (255, 255, 255)  # white colour
BLACK = (0, 0, 0)  # black colour
RED = (255, 0, 0)  # RED COLOUR
GREEN = (0, 255, 0)  # GREEN COLOUR
BACKGROUND = 'space.png'  # background image
default_font = "Arial" # font for game text

# AUDIO. NAMES ARE SELF-EXPLANATORY
player_laser_sound = 'star-wars-x-wing-sound-blaster.mp3'
enemy_laser_sound = 'Tie-fighter-blaster-sfx.mp3'
boss_laser_sound = 'death-star-laser.mp3'
background_music = 'The-Imperial-March-8-bit.mp3'
boss_fight_music = 'StarWar DarthNihilusTheme.mp3'
big_explosion = 'explosion.mp3'
small_explosion = 'explosion_from_low_hp.mp3'
health_pickup = "health_pickup.mp3"
victory_sound = "game_win.mp3"
losing_sound = "game_lost.mp3"

# PLAYER CONFIG
lives = 10  # number of player lives
player_size = 60  # change size of player block
ship_image = 'x-wing.png'  # player block sprite
ship_laser_sprite = 'player-laser.png'
player_move_speed = 6  # how fast the player moves
grace_period = 2  # the number enemy hits you can take before it affects score.

# GAME TRACKING
game_history = ['Game Start']  # keeps a track of the game progress and score.
boss_active = False  # Check if boss is active or not. Boss Fight Toggle.
game_lost = False  # check if game over with a loss
game_won = False  # check if game over with a win

# ENEMY CONFIG
enemy_image = 'tie-fighter.png'  # enemy TIE-fighter sprite
enemy_laser_sprite = 'enemy-laser.png'  # enemy projectile
damaged_enemy = 'damaged_tie-fighter.png'  # damaged enemy TIE-fighter sprite
enemy_hp_value = 5  # enemy health
enemy_size = 70  # change the block size of enemies
enemy_horizontal_movement_speed = 3  # the sideways movement speed of enemy block
enemy_downward_movement_distance = enemy_size  # downward distance for the enemy
enemy_fire_back_chance = 0.07  # the chance for the enemy to attack back
number_of_enemy_rows = 3  # 3 rows of enemies are created
number_of_enemy_columns = 10  # 10 columns of enemies are created
row_spacing = number_of_enemy_rows * enemy_size  # calculate the row gap
column_spacing = number_of_enemy_columns * enemy_size  # calculate column gap
enemy_give_health_chance = 0.009  # low chance of enemy dropping health
health_object_sprite = 'health.png'  # health drop sprite
enemy_health_object_size = 30  # size of health drop sprite from an enemy

# BOSS CONFIG
boss_image = 'deathstar.png'  # boss image sprite
boss_laser_sprite = 'death-star-laser.png'  # boss projectile sprite
damaged_deathstar = 'damaged_deathstar.png'  # damaged enemy deathstar sprite
boss_size = 300  # size of boss sprite
boss_hp_value = 80  # the max health for the boss
boss_horizontal_movement_speed = 2  # speed for boss to move horizontally
boss_fire_rate = 5  # the random rate (chance) for the boss to shoot laser
boss_give_health_chance = 0.2  # some chance of boss dropping health
boss_health_object_size = 100  # size of health drop sprite from boss

