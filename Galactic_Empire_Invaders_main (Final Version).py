"""
    Game: Galactic Empire Invaders
    By: Kaushal Bhingaradia
    Date: February 18, 2024

    You are a lone Jedi in your reliable X-wing tasked
    with defeating the Empire.
    On your journey, you are ambushed
    by Empirical fighters and ultimately the death star.

    Note: - Left & Right arrow to move left or right respectively.
            Space-bar to shoot.
    - You can take two hits from enemy (grace period) before it starts to
      affect your score.
    - Enemies have a specific health set (default is 5 HP so 5 shots to kill)
    - After game over, re-run program to start again.
    - Collect health along the way to live longer.
    - Be sure not to get hit by lasers since that reduces score by 1.
    If you
      get less than 0, you lose.
    - Defeat the final boss (Deathstar) to win the game.
    -
    There is a 5-second wait time
    for the program to close on game over screen

    Credit to: Prof. Michael Nixon for the original space invader
    template from lab 3.
    Sources for assets in local directory source.txt

    Fixes: -Game can now run without any sprites by implementing error handling.
"""
import pygame
import random
from game_config import *  # all the game configurations in a separate file


class Bullet(pygame.sprite.Sprite):
    """
    This class represents the bullet.
    The colour depends on if its player or the enemy.
    Green for the enemy and boss, Red for the player.
    """

    def __init__(self, bullet_direction, sprite, size_width, size_height):
        # Call the parent class (Sprite) constructor
        super().__init__()

        try:
            self.image = pygame.image.load(
                sprite).convert_alpha()  # load sprite
            # convert pixels to format supporting transparency

            self.image = pygame.transform.scale(self.image, (
                size_width, size_height))  # scale Sprite image
            self.image.set_colorkey(
                BLACK)  # make black background pixels transparent
        # if there is an error during loading, print error message and create
        # blue rectangle as placeholder image
        except Exception as e:
            print(
                f"FAILED TO LOAD SPRITE. ERROR:{e}")  # display that sprite
            # has failed to load
            self.image = pygame.Surface(
                [size_width - 10, size_height - 10])  # create rectangular
            # surface
            self.image.fill(
                pygame.color.THECOLORS['blue'])
            # fill the surface with the colour blue

        self.rect = self.image.get_rect()

        self.bullet_direction = bullet_direction

    def update(self):
        """ Move the bullet. """
        self.rect.y += 3 * self.bullet_direction  # move the bullet upwards for
        # the player and downwards for the enemy.
        # Positive is down, negative is up


class Health(pygame.sprite.Sprite):
    """
    This class represents the health object dropped by both the enemy
    TIE-fighters and the boss.
    It falls slower than a regular bullet, and when
    the player touches it, They get an added life by 1.
    """

    def __init__(self, sprite, size_width, size_height):
        # Call the parent class (Sprite) constructor
        super().__init__()

        try:
            self.image = pygame.image.load(
                sprite).convert_alpha()  # load sprite
            # convert pixels to format supporting transparency

            self.image = pygame.transform.scale(self.image, (
                size_width, size_height))  # scale Sprite image
            self.image.set_colorkey(
                BLACK)  # make black background pixels transparent
        # if there is an error during loading, print error message and create
        # blue rectangle as placeholder image
        except Exception as e:
            print(
                f"FAILED TO LOAD SPRITE. ERROR:{e}")  # display that sprite
            # has failed to load
            self.image = pygame.Surface(
                [size_width - 10,
                 size_height - 10])  # create rectangular surface
            self.image.fill(
                pygame.color.THECOLORS['yellow'])
            # fill the surface with the colour yellow

        self.rect = self.image.get_rect()

    def update(self):
        """ Move the health object downward slower than a bullet."""
        self.rect.y += 2


class Enemy(pygame.sprite.Sprite):
    """
    This class represents the enemy TIE-fighters which attack the player.
    The enemy will move side to side while going downwards.
    The goal for
    the enemy is to destroy the player by reducing the number of lives or
    the score to be less than 0.
    """

    def __init__(self):
        # Call the parent class (Sprite) constructor
        super().__init__()

        try:
            self.image = pygame.image.load(enemy_image).convert()
            self.image = pygame.transform.scale(self.image, (
                enemy_size, enemy_size))  # scale Sprite image
            self.image.set_colorkey(
                BLACK)  # make black background pixels transparent
        # if there is an error during loading, print error message and create
        # rectangle as placeholder image
        except Exception as e:
            print(
                f"FAILED TO LOAD SPRITE. ERROR:{e}")  # display that sprite has
            # failed to load
            self.image = pygame.Surface(
                [enemy_size - 30,
                 enemy_size - 30])  # create rectangular surface
            self.image.fill(
                pygame.color.THECOLORS['black'])  # fill the surface with the
            # colour black

        self.rect = self.image.get_rect()

        self.x_movement = enemy_horizontal_movement_speed  # horizontal movement
        # speed
        self.downward_movement = enemy_downward_movement_distance  # downward
        # movement
        self.touched_bottom = False  # check if enemy touched bottom of screen
        self.enemy_hp = enemy_hp_value  # the amount of HP for each enemy

    def update(self):
        """
        Update the movement of enemy both horizontally and vertically.
        """
        self.rect.x += self.x_movement  # move enemy towards side, according to
        # movement value

        # Same border collision logic from lab 1 which takes account the size
        # of the enemy block and window size.
        # Bounce the enemy off the wall if
        # the enemy touches the side of the screen,
        # reverse the movement speed
        # to change its direction
        if self.rect.x > screen_width - enemy_size or self.rect.x < 0:
            self.x_movement = -self.x_movement

        # if enemy block touches a left window border, move down by value
        if self.rect.x < 0:
            self.rect.y += self.downward_movement

        # if the enemy reaches bottom, change touched_bottom variable to true
        # and false otherwise
        if self.rect.bottom >= screen_height:
            self.touched_bottom = True
        else:
            self.touched_bottom = False

    def attack(self):
        """
        The enemy will fire bullets at the player when this function is called.
        """
        # Laser fire sounds. No sound will play if the sound file is missing.
        try:
            sound = pygame.mixer.Sound(enemy_laser_sound)
            sound.set_volume(0.2)
            sound.play()
        except Exception as e:
            print(f"NO SOUND-FX: {e}")

        # enemy bullet object is created
        hostile_bullet = Bullet(1, enemy_laser_sprite, 30,
                                40)  # create a downward enemy bullet object
        # enemies will have a red bullet
        hostile_bullet.rect.x = self.rect.centerx  # center bullet on enemy
        hostile_bullet.rect.y = self.rect.bottom  # position bullet under enemy
        return hostile_bullet

    def low_health(self):
        """
        Changes sprite image to a damaged TIE-fighter when the health is low
        (equal to 2) while handling error.
        :return:
        """
        try:
            self.image = pygame.image.load(damaged_enemy).convert()
            self.image = pygame.transform.scale(self.image, (
                enemy_size, enemy_size))  # scale Sprite image
            self.image.set_colorkey(
                BLACK)  # make black background pixels transparent

            # if there is an error during loading,
            # print error message and create
            # rectangle as placeholder image
        except Exception as e:
            print(
                f"FAILED TO LOAD SPRITE. ERROR:{e}")  # display that sprite has
            # failed to load
            self.image = pygame.Surface(
                [enemy_size - 30,
                 enemy_size - 30])  # create rectangular surface
            self.image.fill(
                pygame.color.THECOLORS[
                    'red'])  # fill the surface with red


class Boss(pygame.sprite.Sprite):
    """
    This class represents the Boss which is the final enemy in the game. The
    deathstar will shoot a barrage of laser which the player must dodge as
    well as dropping some larger health objects to heal. It will have an
    entrance by moving down from the screen then staying at the specific
    height and only moving side to side.
    """

    def __init__(self):
        # Call the parent class (Sprite) constructor
        super().__init__()

        try:
            self.image = pygame.image.load(boss_image).convert()
            self.image = pygame.transform.scale(self.image, (
                boss_size, boss_size))  # scale Sprite image
            self.image.set_colorkey(
                BLACK)  # make black background pixels transparent

        # if there is an error during loading, print error message and create
        # rectangle as placeholder image
        except Exception as e:
            print(
                f"FAILED TO LOAD SPRITE. ERROR:{e}")  # display that sprite has
            # failed to load
            self.image = pygame.Surface(
                [boss_size, boss_size])  # create rectangular surface
            self.image.fill(
                pygame.color.THECOLORS['white'])  # fill the surface with white

        self.rect = self.image.get_rect()

        self.active = False
        self.boss_hp = boss_hp_value

        # ENEMY MOVEMENT VARIABLES
        self.x_movement = boss_horizontal_movement_speed  # horizontal movement
        # speed
        self.y_movement = 0.55  # vertical movement speed
        self.rect.y = -400  # position boss out of view initially
        self.follow_speed = 3

    def update(self):
        """
        Manage and update the movement of the enemy blocks.
        """

        self.rect.x += self.x_movement  # update boss position according to
        # movement

        # Move Boss down vertically into view
        if self.rect.y - boss_size <= 0:
            self.rect.y += self.y_movement
        if self.rect.y >= 0:
            self.rect.y = 0

        # Same border collision logic from lab 1 which takes account the
        # size of the enemy rectangle and window size.
        # Bounce the enemy off the wall
        if self.rect.x > screen_width - boss_size or self.rect.x < 0:
            self.x_movement *= -1

    def attack(self):
        """
        The boss will fire at the player.
        Boss laser sound that plays upon this
        function being called.
        """
        # Sound will not play if the file is not detected, otherwise it will
        # work fine if the file is detected.
        try:
            sound = pygame.mixer.Sound(boss_laser_sound)  # add sound for boss
            # lasers
            sound.set_volume(0.6)
            sound.play()
        except Exception as e:
            print(f"NO SOUND-FX: {e}")

        hostile_bullet = Bullet(1, boss_laser_sprite, 60,
                                300)  # create a downward enemy bullet object
        hostile_bullet.rect.x = self.rect.centerx - 80  # center bullet on an
        # enemy
        hostile_bullet.rect.y = self.rect.bottom - 270  # position under an
        # enemy

        return hostile_bullet

    def low_health(self):
        """
        Changes sprite image to a damaged deathstar when the health is low
        (half health) while handling error.
        :return:
        """
        try:
            self.image = pygame.image.load(damaged_deathstar).convert()
            self.image = pygame.transform.scale(self.image, (
                boss_size, boss_size))  # scale Sprite image
            self.image.set_colorkey(
                BLACK)  # make black background pixels transparent

            # if there is an error during loading, print error message and
            # create rectangle as placeholder image
        except Exception as e:
            print(
                f"FAILED TO LOAD SPRITE. ERROR:{e}")  # display that sprite has
            # failed to load
            self.image = pygame.Surface(
                [boss_size, boss_size])  # create rectangular surface
            self.image.fill(
                pygame.color.THECOLORS[
                    'red'])  # fill the surface with red


class Player(pygame.sprite.Sprite):
    """ This class represents the Player x-wing.
        Can move side to side like in
        the original space invaders as well as attack
        by firing lasers to
        defeat enemy tie-fighters and the deathstar.
    """

    def __init__(self):
        # Call the parent class (Sprite) constructor
        super().__init__()
        try:
            self.image = pygame.image.load(ship_image).convert()
            self.image = pygame.transform.scale(self.image, (
                player_size, player_size))  # scale Sprite image
            self.image.set_colorkey(
                BLACK)  # make black background pixels transparent
        # if there is an error during loading, print error message and create
        # rectangle as placeholder image
        except Exception as e:
            print(
                f"FAILED TO LOAD SPRITE. ERROR:{e}")  # display that sprite has
            # failed to load
            self.image = pygame.Surface(
                [player_size - 30, player_size - 30])  # create rectangular
            # surface
            self.image.fill(
                pygame.color.THECOLORS['green'])  # fill the surface with green

        self.rect = self.image.get_rect()
        self.direction = 1  # set the initial player direction to the right
        self.move_speed = player_move_speed

    def update(self):
        """ Update the player's position. """
        self.rect.x += self.direction * self.move_speed  # move player towards
        # a sideways direction at a defined speed

        # Bounce off side of screen if boundary is touched
        if self.rect.left < 0:
            self.rect.x = 0
        if self.rect.x >= screen_width - player_size:
            self.rect.x = screen_width - player_size

    def attack(self):
        """
        The player fires a bullet upwards.
        Player x-wing laser fire sound gets
        played upon this function being called.
        Will not play sound if no sound
        file is detected.
        """
        try:
            sound = pygame.mixer.Sound(player_laser_sound)
            sound.set_volume(0.35)
            sound.play()
        except Exception as e:
            print(f"NO SOUND-FX: {e}")

        player_bullet = Bullet(-1, ship_laser_sprite, 20,
                               40)  # create a downward enemy bullet object

        # Position bullet
        player_bullet.rect.x = self.rect.x + 20  # center of x-wing
        player_bullet.rect.y = self.rect.y - 10  # Set laser slightly above
        # player cannon

        return player_bullet


class Game:
    """ Represents the core of the game, containing all game objects and logic
        in order for the game to work and handle events.
    """

    def __init__(self):
        # Initialize Pygame
        pygame.init()
        # Create a game window, setting the screen width and height
        try:
            self.screen = pygame.display.set_mode(
                [screen_width, screen_height])
            pygame.display.set_caption("Galactic Empire Invaders", enemy_image)
        except Exception as e:
            print(f"FAILED TO SET UP SCREEN: {e}")

        self.running = False
        # Sprite lists
        self.all_sprites_list = pygame.sprite.Group()  # list of every sprite
        self.enemy_list = pygame.sprite.Group()  # list of enemy TIE fighters
        self.bullet_list = pygame.sprite.Group()  # list of each bullet
        self.hostile_bullet_list = pygame.sprite.Group()  # list of each enemy
        # bullet that can hurt the player
        self.boss_list = pygame.sprite.Group()  # boss list which contains the
        # final boss that player will fight.
        self.health_list = pygame.sprite.Group()  # list containing the
        # health objects that randomly are given.

        # calculate gap between enemies accounting for screen dimensions and
        # number of enemies
        space_horizontally = (screen_width - column_spacing) // (
                number_of_enemy_columns + 1)
        space_vertically = (screen_height // 2 - row_spacing) // (
                number_of_enemy_rows + 1)

        # Create a grid pattern for the Enemy Tie-Fighters
        # Code
        # revised and borrowed from Codersports.com as well as lab 3 old
        # code.
        # All space invader games share a similar pattern of setting up a
        # grid pattern for the enemy.
        for row in range(number_of_enemy_rows):
            for column in range(number_of_enemy_columns):
                # create an enemy object
                enemy = Enemy()
                # enemy x pos and y pos based on grid spacing
                enemy.rect.x = space_horizontally + enemy_size * column + \
                               space_horizontally
                enemy.rect.y = space_vertically + enemy_size * row + \
                               space_vertically

                # add enemies to the sprite groups
                self.enemy_list.add(enemy)
                self.all_sprites_list.add(enemy)

        # Create a player block and add to list of all sprites
        self.player = Player()
        self.all_sprites_list.add(self.player)

        self.score = 0  # the score variable
        self.player.rect.y = screen_height - self.player.rect.height * 2
        # position player close to bottom of screen

    # player events handling
    def poll(self):
        """
        Handles the events regarding the controls, movement, and attacks for
        the player.
        :return:
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYDOWN:
                # if space bar is pressed, fire a laser and play x-wing
                # laser sound effect
                if event.key == pygame.K_SPACE:
                    # Create a friendly laser bullet object
                    bullet = self.player.attack()
                    self.all_sprites_list.add(bullet)
                    self.bullet_list.add(bullet)
                # change the direction of the player when pressing either left
                # or right arrow keys
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    self.player.direction *= -1

    def score_board(self, score):
        """
        Display the score and number of enemies remaining in console.
        """
        game_history.append(score)
        print(f"======================================\n"
              f"           GAME SCOREBOARD\n"
              f"======================================\n"
              f"Enemies Remaining: {len(self.enemy_list)}\n"
              f"Current Score: {score}\n"
              f"______________________________________\n")

    # -- OTHER SOUND EFFECTS USED BY GAME --
    @staticmethod
    def normal_background_music():
        """
        This function handles the background music before the boss fight!
        It will handle errors like the file missing to prevent the game
        from crashing
        :return:
        """

        try:
            pygame.mixer.music.load(background_music)
            pygame.mixer.music.play(-1)
        except Exception as e:
            print(f"NO MUSIC: {e}")

    @staticmethod
    def boss_background_music():
        """
        This function handles the background music during the boss fight!
        It will handle errors like the file missing to prevent the game
        from crashing
        :return:
        """
        try:
            pygame.mixer.music.stop()
            pygame.mixer.music.load(boss_fight_music)
            pygame.mixer.music.play(-1)
        except Exception as e:
            print(f"NO MUSIC: {e}")

    @staticmethod
    def big_explosion_soundfx():
        """
        This function handles the sound-FX for a big explosion!
        It will handle
        errors like the file missing to prevent the game from crashing
        :return:
        """
        try:
            sound = pygame.mixer.Sound(big_explosion)
            sound.set_volume(0.4)
            sound.play()
        except Exception as e:
            print(f"NO SOUND-FX: {e}")

    @staticmethod
    def small_explosion_soundfx():
        """
        This function handles the sound-FX for a small explosion!
        It will
        handle errors like the file missing
        to prevent the game from crashing
        :return
        """
        try:
            sound = pygame.mixer.Sound(small_explosion)
            sound.set_volume(0.7)
            sound.play()
        except Exception as e:
            print(f"NO SOUND-FX: {e}")

    @staticmethod
    def health_pickup_soundfx():
        """
        This function handles the sound-FX for a health pickup!
        It will
        handle errors like the file missing
        to prevent the game from crashing
        :return
        """
        try:
            sound = pygame.mixer.Sound(health_pickup)
            sound.set_volume(1)
            sound.play()
        except Exception as e:
            print(f"NO SOUND-FX: {e}")

    @staticmethod
    def game_lost_soundfx():
        """
        This function handles the sound-FX for losing the game!
        It will
        handle errors like the file missing
        to prevent the game from crashing
        :return
        """
        try:
            sound = pygame.mixer.Sound(losing_sound)
            sound.set_volume(0.7)
            sound.play()
        except Exception as e:
            print(f"NO SOUND-FX: {e}")

    @staticmethod
    def game_win_soundfx():
        """
        This function handles the sound-FX for winning the game!
        It will
        handle errors like the file missing
        to prevent the game from crashing
        :return
        """
        try:
            sound = pygame.mixer.Sound(victory_sound)
            sound.set_volume(0.7)
            sound.play()
        except Exception as e:
            print(f"NO SOUND-FX: {e}")

    # -- BACKGROUND IMAGE MANAGEMENT --
    @staticmethod
    def set_background_image(background):
        """
        Sets the background image for the game while handling exceptions.
        :param background:
        :return:
        """
        try:
            background_image = pygame.image.load(background).convert()
            background_image = pygame.transform.scale(background_image,
                                                      (screen_width,
                                                       screen_height))
            return background_image
        except Exception as e:
            print(f"FAILED TO LOAD BACKGROUND: {e}")
            background_image = pygame.Surface(
                [screen_width, screen_height])  # create rectangular surface
            background_image.fill(pygame.color.THECOLORS['grey'])
            return background_image

    # -- GAME UPDATE AND EVENTS--

    def update(self):
        """
        Update events, detect collisions and handle game win or loss logic.
        """
        # Global variables for boss, player lives, and game events
        # that can be accessed and updated by this function.
        global boss_active
        global lives
        global boss_hp_value
        global boss_fire_rate
        global game_lost
        global game_won
        global grace_period

        # update all sprites
        self.all_sprites_list.update()

        # bullet mechanics
        for bullet in self.bullet_list:

            # check if the bullet hit an enemy
            enemy_hit_list = pygame.sprite.spritecollide(
                bullet, self.enemy_list, False)

            # for each enemy that gets hit, subtract 1 HP from their total HP
            for enemy in enemy_hit_list:
                enemy.enemy_hp -= 1
                # remove each bullet that hits
                self.bullet_list.remove(bullet)
                self.all_sprites_list.remove(bullet)

                # if enemy health is equal to half, then change the sprite to a
                # damaged TIE-fighter
                enemy_half_health = enemy_hp_value // 2
                if enemy.enemy_hp == enemy_half_health:
                    enemy.low_health()

                # if the enemy HP is 0 or less, remove the enemy and add a point
                # to the score board
                elif enemy.enemy_hp <= 0:
                    enemy_hit_list.remove(enemy)
                    self.all_sprites_list.remove(enemy)
                    self.enemy_list.remove(enemy)
                    self.score += 1
                    self.score_board(self.score)

                    # play big explosion sound effect upon the enemy death
                    self.big_explosion_soundfx()

            # Remove the bullet if it flies up off the screen
            if bullet.rect.y < (0 - bullet.rect.height):
                self.bullet_list.remove(bullet)
                self.all_sprites_list.remove(bullet)

            # check if boss got hit
            boss_hit_list = pygame.sprite.spritecollide(
                bullet, self.boss_list, False)
            # Each time boss is hit, remove the bullet and add to score
            for boss in boss_hit_list:

                # play big sound effect
                self.big_explosion_soundfx()

                # Remove the bullet object from both sprite group lists.
                self.bullet_list.remove(bullet)
                self.all_sprites_list.remove(bullet)

                # add to the score
                self.score += 1
                self.score_board(self.score)

                # remove health from boss
                boss.boss_hp -= 1
                print(f"boss HP: {boss.boss_hp}")  # print boss HP

                # if the boss has low health (half health) then change the
                # sprite to a damaged version of the deathstar
                half_health = boss_hp_value // 2
                if boss.boss_hp == half_health:
                    boss.low_health()

                # remove boss after HP is less than or equal to 0 and end game
                elif boss.boss_hp <= 0:
                    self.boss_list.empty()
                    self.all_sprites_list.empty()

        # -- enemy logic --
        for enemy in self.enemy_list:
            # check if enemy touches the bottom of the screen and if true,
            # delete it and subtract 1 point from score
            if enemy.touched_bottom:
                self.enemy_list.remove(enemy)
                self.all_sprites_list.remove(enemy)
                self.score -= 1
                self.score_board(self.score)

            # enemy has random chance of firing hostile laser
            elif random.random() < (
                    enemy_fire_back_chance / 100):  # random percent
                enemy_bullet = enemy.attack()
                self.all_sprites_list.add(enemy_bullet)
                self.hostile_bullet_list.add(enemy_bullet)

            # enemy has random chance of dropping health hearts which give
            # players an extra life
            elif random.random() < (
                    enemy_give_health_chance / 100):  # random percent
                # calculated to determine when to create a health object
                health_drop = Health(health_object_sprite,
                                     enemy_health_object_size,
                                     enemy_health_object_size)
                # position health
                health_drop.rect.x = enemy.rect.centerx + 20  # offset from
                # center of TIE Fighter, so it doesn't overlap hostile laser.
                health_drop.rect.y = enemy.rect.bottom  # position at the
                # bottom of the TIE fighter enemy

                # add to the sprite group lists, so it can be checked
                self.all_sprites_list.add(health_drop)
                self.health_list.add(health_drop)

        # --health collision with player logic--
        # check if player sprite touches the health sprite object
        health_hit_list = pygame.sprite.spritecollide(self.player,
                                                      self.health_list, False)

        # iterate through the health sprite group to get the specific colliding
        # health object
        for health_object in health_hit_list:
            # remove the object when collision occurs
            self.health_list.remove(health_object)
            self.all_sprites_list.remove(health_object)
            lives += 1

            # play health pickup sound effect
            self.health_pickup_soundfx()

        # -- Boss Battle --
        # if no enemies remain and boss is not active, trigger boss
        if len(self.enemy_list) <= 0 and not boss_active:
            # The boss is now active.
            boss_active = True

            # play boss music.
            self.boss_background_music()

            # add boss to the boss sprite group, by creating a boss object.
            boss = Boss()
            self.boss_list.add(boss)

        # Boss firing random lasers and giving health to player.
        # Reusing logic from enemies.
        for boss in self.boss_list:
            boss.update()
            # boss has a random chance of shooting laser
            if random.random() < (boss_fire_rate / 100):  # random percent
                # create a boss bullet object using boss class
                boss_bullet = boss.attack()
                # add to the group list of all sprites and hostile bullets
                self.all_sprites_list.add(boss_bullet)
                self.hostile_bullet_list.add(boss_bullet)

            elif random.random() < (
                    boss_give_health_chance / 100):  # random percent is
                # calculated to determine when to create the health object
                boss_health_drop = Health(health_object_sprite,
                                          boss_health_object_size,
                                          boss_health_object_size)
                boss_health_drop.rect.x = boss.rect.centerx + 100  # x offset
                boss_health_drop.rect.y = boss.rect.bottom - 300  # set the
                # health drop to be positioned above the bottom of the boss

                # add to group sprites
                self.all_sprites_list.add(boss_health_drop)
                self.health_list.add(boss_health_drop)

        # if the player gets hit by any hostile laser, subtract one life then
        # after a two-hit grace period,
        # begin to subtract the score by 1 each
        # time the laser hits the player.
        if pygame.sprite.spritecollide(self.player, self.hostile_bullet_list,
                                       True):
            lives -= 1
            grace_period -= 1

            print(grace_period)
            if grace_period < 0:
                self.score -= 1
                self.score_board(self.score)

                # play small explosion sound effect
                self.small_explosion_soundfx()

                # notify player, that they have been hit and display score
                print(f'\nYou got hit. Lives Remaining: {lives}\n')
                print(f"Score History: {game_history}\n"
                      f"\nTotal Score: {self.score}\n")

        # if the enemy collides with the player x-wing, then subtract 1 life
        # and 1 point,
        # as well as destroy the enemy from the collision.
        elif pygame.sprite.spritecollide(self.player, self.enemy_list, True):
            lives -= 1
            self.score -= 1
            self.score_board(self.score)

            # play big collision impact sound-fx.
            self.big_explosion_soundfx()

            # remove the enemy from both lists when hit
            self.enemy_list.remove(enemy)
            self.all_sprites_list.remove(enemy)
            # display message
            print(f'\nYou got hit. Lives Remaining: {lives}\n')
            print(f"Score History: {game_history}\n"
                  f"\nTotal Score: {self.score}\n")

        # end game if the player runs out of lives
        elif lives <= 0:
            game_lost = True

            # stop all sounds
            pygame.mixer.stop()

            # stop music
            pygame.mixer.music.stop()

            # clear all sprite groups after the game ends
            self.all_sprites_list.empty()
            self.boss_list.empty()
            self.hostile_bullet_list.empty()
            self.bullet_list.empty()

        # Check if the score is less than 0. If it is than end the game
        # Show score history after
        elif self.score < 0:
            # self.running = False
            game_lost = True

            # stop all sounds
            pygame.mixer.stop()

            # stop music
            pygame.mixer.music.stop()

            # clear every sprite group after the game is over
            self.all_sprites_list.empty()
            self.boss_list.empty()
            self.hostile_bullet_list.empty()
            self.bullet_list.empty()


        # if the boss sprite group is empty, this means the boss has been
        # defeated and the player wins.
        elif boss_active and len(self.boss_list) <= 0:
            game_won = True

            # stop sounds
            pygame.mixer.stop()

            # stop music
            pygame.mixer.music.stop()

            # clear every sprite group after the game is over
            self.all_sprites_list.empty()
            self.boss_list.empty()
            self.hostile_bullet_list.empty()
            self.bullet_list.empty()

            # game won sound effect
            self.game_win_soundfx()

    def draw(self):
        """
        Draws on screen.
        :return:
        """
        # create background image for the game
        background_image = self.set_background_image(BACKGROUND)

        # font setup
        font = pygame.font.SysFont(default_font, 28)
        boss_font = pygame.font.SysFont(default_font, 48)
        game_over_font = pygame.font.SysFont(default_font, 70)

        # Rendering for on screen text such as color.
        lives_remaining_text = font.render(f"Lives Remaining: {lives}", True,
                                           WHITE)
        score_text = font.render(f"Score: {self.score}", True, WHITE)
        enemies_remaining_text = font.render(f"Enemies Remaining: "
                                             f"{len(self.enemy_list)}", True,
                                             WHITE)
        you_win_text = game_over_font.render(f"You Win! Your High Score: "
                                             f"{self.score}", True, GREEN)
        you_lose_text = game_over_font.render(f"You Lost! Your High Score: "
                                              f"{self.score}", True, RED)
        grace_period_text = font.render(f"Grace Period", True, GREEN)

        # Clear screen
        self.screen.blit(background_image, (0, 0))

        # Draw all the sprites
        self.all_sprites_list.draw(self.screen)
        self.boss_list.draw(self.screen)
        self.hostile_bullet_list.draw(self.screen)

        # draw lives remaining text on screen
        self.screen.blit(lives_remaining_text, (10, 10))
        # draw score text on screen
        self.screen.blit(score_text, ((screen_width // 2) - 50, 10))

        # draw grace period text on screen when active (as long as it is
        # not <= 0)
        if not grace_period <= 0:
            self.screen.blit(grace_period_text, (10, screen_height - 150))

        # only display the number of enemies remaining while boss is inactive
        if not boss_active:
            self.screen.blit(enemies_remaining_text, (screen_width - 250, 10))

        # display boss text when boss is active
        for boss in self.boss_list:
            if boss_active:
                boss_text = boss_font.render(f"Boss HP: {boss.boss_hp}", True,
                                             RED)
                self.screen.blit(boss_text, (screen_width - 250, 10))

        # display text if player wins game
        if game_won:
            self.screen.blit(you_win_text, (10, screen_height // 2 - 50))
            pygame.display.flip()  # update the screen

            # play victory sound effect
            self.game_win_soundfx()
            # wait 5 seconds before closing game
            pygame.time.wait(5000)
            self.running = False


        # display text is player loses game
        elif game_lost:
            self.screen.blit(you_lose_text, (10, screen_height // 2 - 50))
            pygame.display.flip()  # update the screen

            # play game lost sound effect
            self.game_lost_soundfx()
            # wait 5 seconds before closing game
            pygame.time.wait(5000)
            self.running = False

    def run(self):
        """
        Runs the game by calling all the other functions contained in Game
        class and keeps them running with the mainloop.
        :return:
        """
        self.running = True
        # Used to manage screen update speed
        clock = pygame.time.Clock()

        # Play background music.
        self.normal_background_music()

        # ------- Main Program Loop --------
        while self.running:
            # Process events
            self.poll()

            # Handle game logic
            self.update()
            # Draw a frame
            self.draw()

            # Update the screen with what we've drawn.
            pygame.display.flip()

            # Limit frames per second to 60
            clock.tick(60)


if __name__ == '__main__':
    g = Game()
    print("Starting game...")
    g.run()
    print("Shutting down... Thanks for playing!")
    pygame.quit()
