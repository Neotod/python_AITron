# -*- coding: utf-8 -*-

# python imports
import random

# chillin imports
from chillin_client import RealtimeAI

# project imports
from ks.models import ECell, EDirection, Position
from ks.commands import ChangeDirection, ActivateWallBreaker

# chillncode imports
from cnc.chillncode import Chillncode

class AI(RealtimeAI):

    def __init__(self, world):
        super(AI, self).__init__(world)

    def initialize(self):
        global chillncode
        chillncode = Chillncode()
        chillncode.say_welcome()
        
        board = self.world.board
        agent = self.world.agents[self.my_side]
        
        chillncode.set_requirements(agent, board, self.my_side)
        chillncode.make_squares()
        chillncode.find_near_squares()
        chillncode.set_entry_positions()
        chillncode.find_next_square()
        chillncode.find_new_reaching_path()

    def decide(self):
        board = self.world.board
        agent = self.world.agents[self.my_side]
        
        chillncode.set_requirements(agent, board, self.my_side)
        
        new_square = chillncode.is_new_square()
        if new_square == True:
            chillncode.update_curr_square_index()
            chillncode.find_next_square()
            chillncode.find_new_reaching_path()
        
        new_square_changed = chillncode.is_next_square_changed()
        if new_square_changed == True:
            chillncode.find_next_square()
            chillncode.find_new_reaching_path()
        
        wallbreaker_needed = chillncode.is_wallbreaker_needed()
        if wallbreaker_needed == True:
            self.send_command(ActivateWallBreaker())

        next_direction = chillncode.next_dir()
        self.send_command(ChangeDirection(next_direction))
            
