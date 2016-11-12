#
# This file is where you make the display for your game
# Make changes and add functions as you need.
#

import pygame
import os
from config import *
from common.event import *
from client.base_display import BaseDisplay


class Display(BaseDisplay):
    """
    This class controls all of the drawing of the screen
    for your game.  The process of drawing a screen is
    to first draw the background, and then draw everything
    that goes on top of it.  If two items are drawn in the
    same place, then the last item drawn will be the one
    that is visible.

    The screen is a 2 dimensional grid of pixels, with the
    origin (0,0) located at the top-left of the screen, and
    x values increase to the right and y values increase as
    you go down.  The y values are opposite of what you learned
    in your math classes.

    Documentation on drawing in pygame is available here:
    http://www.pygame.org/docs/ref/draw.html

    The methods in this class are:
    __init__ creates data members (variables) that are used
        in the rest of the methods of this class.  This is
        useful for defining colors and sizes, loading image
        or sound files, creating fonts, etc.  Basically,
        any one time setup.

    paint_game controls the drawing of the screen while the
        game is in session.  This is responsible for making
        sure that any information, whether graphics, text, or
        images are drawn to the screen.

    paint_waiting_for_game controls the drawing of the screen
        after you have requested to join a game, but before
        the game actually begins.

    paint_game_over controls the drawing of the screen after
        the game has been won, but before the game goes away.
        This is a short (3-5 second) period.

    process_event controls handling events that occur in the
        game, that aren't represented by objects in the game
        engine.  This includes things like collisions,
        objects dying, etc.  This would be a great place to
        play an audio file when missiles hit objects.

    paint_pregame controls the drawing of the screen before
        you have requested to join a game.  This would usually
        allow the user to know the options available for joining
        games.

    Method parameters and data members of interest in these methods:
    self.width is the width of the screen in pixels.
    self.height is the height of the screen in pixels.
    self.* many data members are created in __init__ to set up
        values for drawing, such as colors, text size, etc.
    surface is the screen surface to draw to.
    control is the control object that is used to
        control the game using user input.  It may
        have data in it that influences the display.
    engine contains all of the game information about the current
        game.  This includes all of the information about all of
        the objects in the game.  This is where you find all
        of the information to display.
    event is used in process_event to communicate what
        interesting thing occurred.

    Note on text display:  There are 3 methods to assist
    in the display of text.  They are inherited from the
    BaseDisplay class.  See client/base_display.py.

    """

    def __init__(self, width, height):
        """
        Configure display-wide settings and one-time
        setup work here.
        """
        BaseDisplay.__init__(self, width, height)

        # There are other fonts available, but they are not
        # the same on every computer.  You can read more about
        # fonts at http://www.pygame.org/docs/ref/font.html
        self.font_size = 36
        self.font = pygame.font.SysFont("Courier New",self.font_size)

        # Colors are specified as a triple of integers from 0 to 255.
        # The values are how much red, green, and blue to use in the color.
        # Check out http://www.colorpicker.com/ if you want to try out
        # colors and find their RGB values.   Be sure to use the `R`, `G`,
        # `B` values at the bottom, not the H, S, B values at the top.
        self.player_color     = (0, 255, 0)
        #self.opponent_color   = (255, 0, 0)
        self.missile_color    = (0, 255, 255)
        self.npc_color        = (255, 255, 0)
        self.wall_color       = (255, 255, 255)
        self.text_color       = (255, 255, 255)
        self.background_color = (50, 0, 120)
       
        music_path = os.path.join('display', 'music', 'LukHash_-_ARCADE_JOURNEYS.wav')
        pygame.mixer.init()
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.play(-1)

        return

    def paint_pregame(self, surface, control):
        """
        Draws the display before the user selects the game type.
        """
        # background
        rect = pygame.Rect(0, 0, self.width, self.height)
        surface.fill(self.background_color, rect)
        
        # text message in center of screen
        s = "Press 'd' for dual player, 's' for single player,"
        self.draw_text_center(surface, s, self.text_color,
                              self.width/2, 450,
                              self.font)
        s = "'t' for tournament, 'esc' to quit."
        self.draw_text_center(surface, s, self.text_color,
                              self.width/2, 500,
                              self.font)
        s = "To Start-"
        self.draw_text_center(surface, s, self.text_color,
                              self.width/2, 400,
                              self.font)

        s = "Controls-"
        self.draw_text_center(surface, s, self.text_color,
                              self.width/2, 150,
                              self.font)
        s = "Press UP arrow to set player direction and missile_direction upward"
        self.draw_text_center(surface, s, self.text_color,
                              self.width/2, 200,
                              self.font)
        s = "Press DOWN arrow to set player direction and missile direction downward"
        self.draw_text_center(surface, s, self.text_color,
                              self.width/2, 250,
                              self.font)
        s = "Press RIGHT arrow to set player direction and missile direction right"
        self.draw_text_center(surface, s, self.text_color,
                              self.width/2, 300,
                              self.font)
        s = "Press LEFT arrow to set player direction and missile direction left"
        self.draw_text_center(surface, s, self.text_color,
                              self.width/2, 350,
                              self.font)
       
        s = "Press Z to start and stop SEIZURE MODE"
        self.draw_text_center(surface, s, self.text_color,
                              self.width/2, 550,
                              self.font)
        return

    def paint_waiting_for_game(self, surface, engine, control):
        """
        Draws the display after user selects the game type, before the game begins.
        This is usually a brief period of time, while waiting for an opponent
        to join the game.
        """
        # background
        rect = pygame.Rect(0, 0, self.width, self.height)
        surface.fill(self.background_color, rect)
        # text message in center of screen
        s = "Loading Game..."
        self.draw_text_center(surface, s, self.text_color,
                              self.width/2, self.height/2,
                              self.font)
        return

    def paint_game(self, surface, engine, control):
        """
        Draws the display after the game starts.
        """
        # background
        rect = pygame.Rect(0, 0, self.width, self.height)
        surface.fill(self.background_color, rect)

        if hasattr(control, 'background_color') and control.background_color != self.background_color:
            self.background_color = control.background_color

        # draw each object
        objs = engine.get_objects()
        for key in objs:
            obj = objs[key]
            if obj.is_wall():
                self.paint_wall(surface, engine, control, obj)
            elif obj.is_npc():
                self.paint_npc(surface, engine, control, obj)
            elif obj.is_missile():
                self.paint_missile(surface, engine, control, obj)
            elif obj.is_player():
                self.paint_player(surface, engine, control, obj)
            else:
                print "Unexpected object type: %s" % (str(obj.__class__))

        # draw game data
        if control.show_info:
            self.paint_game_status(surface, engine, control)

        return


    def paint_game_over(self, surface, engine, control):
        """
        Draws the display after the game ends.  This
        chooses to display the game, and add a game over
        message.
        """
        self.paint_game(surface, engine, control)

        s = "Game Over (Panzer Wins!)"
        self.draw_text_center(surface, s, self.text_color, int(self.width/2), int(self.height/2), self.font)
        return

    def process_event(self, surface, engine, control, event):
        """
        Should process the event and decide if it needs to be displayed, or heard.
        """
        return

    # The following methods draw appropriate rectangles
    # for each of the objects, by type.
    # Most objects have an optional text display to
    # demonstrate how to send information from the control
    # to the display.
    def paint_wall(self, surface, engine, control, obj):
        """
        Draws walls.
        """
        rect = self.obj_to_rect(obj)
        file_path = os.path.join('display', 'images', 'dat wall.png')
        image = pygame.image.load(file_path)
        surface.blit(image, rect)
  
        return

    def paint_npc(self, surface, engine, control, obj):
        """
        Draws living NPCs.
        """
        if obj.is_alive():
            rect = self.obj_to_rect(obj)
            
            file_path = os.path.join('display', 'images', 'badguy.gif')
            image = pygame.image.load(file_path)
            surface.blit(image, rect)

            pct = (obj.get_health() / obj.get_max_health()) * 10
            pct = int(round(pct))
            health = ''
            health = health.ljust(pct, chr(156))
            health = health.ljust(10)
            health = '|' + health + '|'
        else:
            oid = engine.get_player_oid()
            if oid > 0: 
                me = engine.get_object(oid)
                if me:
                    if me.get_experience() >= (15 * HEALTH_NPC):
                        health = 'MAX POWER!!!! :P'
                    # XP_LEVEL_MISSILE_MANA_RECHARGE_FAST = 14
                    elif me.get_experience() >= (14 * HEALTH_NPC):
                        health = 'Fast Missle Recharge UNLOCKED!!'
                    # XP_LEVEL_MOVE_MANA_RECHARGE_FAST = 13
                    elif me.get_experience() >= (13 * HEALTH_NPC):
                        health = 'Fast Mana Recharge UNLOCKED!!'
                    # XP_LEVEL_POWER_HIGH   = 12
                    elif me.get_experience() >= (12 * HEALTH_NPC):
                        health = 'High Missile Power UNLOCKED!!'
                        engine.set_missile_power_high()
                    # XP_LEVEL_MOVE_MANA_HIGH = 11
                    elif me.get_experience() >= (11 * HEALTH_NPC):
                        health = 'High Move Mana UNLOCKED!!'
                    # XP_LEVEL_RANGE_LONG   = 10
                    elif me.get_experience() >= (10 * HEALTH_NPC):
                        health = 'Long Range UNLOCKED!!'
                        engine.set_missile_range_long()
                    # XP_LEVEL_MISSILE_MANA_HIGH = 9
                    elif me.get_experience() >= (9 * HEALTH_NPC):
                        health = 'High Missile Mana UNLOCKED!!'
                    # XP_LEVEL_SPEED_FAST   = 8
                    elif me.get_experience() >= (8 * HEALTH_NPC):
                        health = 'Fast Speed UNLOCKED!!'
                        engine.set_player_speed_fast()
                        self.go_speed = 'fast'
                    # XP_LEVEL_MISSILE_MANA_RECHARGE_MEDIUM = 7
                    elif me.get_experience() >= (7 * HEALTH_NPC):
                        health = 'Medium Missile Recharge Mana UNLOCKED!!'
                    # XP_LEVEL_MOVE_MANA_RECHARGE_MEDIUM = 6
                    elif me.get_experience() >= (6 * HEALTH_NPC):
                        health = 'Medium Recharge Mana UNLOCKED!!'
                    # XP_LEVEL_POWER_MEDIUM = 5
                    elif me.get_experience() >= (5 * HEALTH_NPC):
                        health = 'Medium Missile Power UNLOCKED!!'
                        engine.set_missile_power_medium()
                    # XP_LEVEL_MOVE_MANA_MEDIUM = 4
                    elif me.get_experience() >= (4 * HEALTH_NPC):
                        health = 'Medium Move Mana UNLOCKED!!'
                    # XP_LEVEL_RANGE_MEDIUM = 3
                    elif me.get_experience() >= (3 * HEALTH_NPC):
                        health = 'Medium Range UNLOCKED!!'
                        engine.set_missile_range_medium()
                    # XP_LEVEL_MISSILE_MANA_MEDIUM = 2
                    elif me.get_experience() >= (2 * HEALTH_NPC):
                        health = 'Medium Missile Mana UNLOCKED!!'                        
                    # XP_LEVEL_SPEED_MEDIUM = 1
                    else:
                        health = 'Medium Speed UNLOCKED!!'
                        engine.set_player_speed_medium()
                        self.go_speed = 'medium'
        self.draw_text_center(surface, health, (200, 0, 0),
                              obj.get_x() + 2, obj.get_y() + 3.5,
                              self.font)
        return

    def paint_missile(self, surface, engine, control, obj):
        """
        Draws living missiles.
        """
        if obj.is_alive():
            obj.set_w(1.8)
            obj.set_h(1.8)
            rect = self.obj_to_rect(obj)
            file_path = os.path.join('display', 'images', 'missle.png')
            image = pygame.image.load(file_path)
            surface.blit(image, rect)
        return

    def paint_player(self, surface, engine, control, obj):
        """
        Draws living players.
        My player is my opponent are in different colors
        """
        missile_count = int(math.floor(obj.get_missile_mana()))
        missiles = ''
        missiles = missiles.ljust(missile_count, '>')
        self.draw_text_center(surface, missiles, (0, 0, 200),
                              obj.get_x() + 40, obj.get_y(),
                              self.font)

        pct = (obj.get_health() / obj.get_max_health()) * 10
        pct = int(round(pct))
        health = ''
        health = health.ljust(pct, chr(156))
        health = health.ljust(10)
        health = '|' + health + '|'
        self.draw_text_center(surface, health, (200, 0, 0),
                              obj.get_x() + 40, obj.get_y() - self.font_size,
                              self.font)
        if obj.is_alive():
            rect = self.obj_to_rect(obj)
            if obj.get_oid() == engine.get_player_oid():
 
  
                file_path = os.path.join('display', 'images', control.player_image)
                image = pygame.image.load(file_path)
                image = image.convert_alpha()
                image = pygame.transform.scale(image, (obj.get_pw(), obj.get_ph()))

                surface.blit(image, rect)

            else:

                file_path = os.path.join('display', 'images', 'panzer.gif')
                image = pygame.image.load(file_path)
                image = image.convert_alpha() # might not be nessesary depending on OS
                image = pygame.transform.scale(image, (obj.get_pw(), obj.get_ph()))

                rect = self.obj_to_rect(obj)
                surface.blit(image, rect)

            (x, y) = obj.get_center()
            x = int( round(x) )
            y = int (round(y) )

            missle_range = int( round(obj.get_missile_range() ))
            pygame.draw.circle(surface, (255, 255, 255), (x,y), missle_range, 1)

        return

    def paint_game_status(self, surface, engine, control):
        """
        This method displays some text in the bottom strip
        of the screen.  You can make it do whatever you want,
        or nothing if you want.
        """

        # display my stats
        oid = engine.get_player_oid()
        if oid > 0:
            obj = engine.get_object(oid)
            if obj:
                s = "Me: %s  HP: %.1f  XP: %.1f Mv: %.1f Ms: %.1f" % \
                    (engine.get_name(),
                     obj.get_health(),
                     obj.get_experience(),
                     obj.get_move_mana(),
                     obj.get_missile_mana())
                position_x = 20
                position_y = self.height - STATUS_BAR_HEIGHT + 3 * self.font_size / 2
                self.draw_text_left(surface, s, self.text_color, position_x, position_y, self.font)

        # display opponent's stats
        oid = engine.get_opponent_oid()
        if oid > 0:
            obj = engine.get_object(oid)
            if obj:
                s = "Opponent: %s  HP: %.1f  XP: %.1f Mv: %.1f Ms: %.1f" % \
                    (engine.get_opponent_name(),
                     obj.get_health(),
                     obj.get_experience(),
                     obj.get_move_mana(),
                     obj.get_missile_mana())
                position_x = 20
                position_y = self.height - STATUS_BAR_HEIGHT + 6 * self.font_size / 2
                self.draw_text_left(surface, s, self.text_color, position_x, position_y, self.font)
        return

