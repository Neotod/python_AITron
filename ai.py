# -*- coding: utf-8 -*-

# python imports
import random

# chillin imports
from chillin_client import RealtimeAI

# project imports
from ks.models import ECell, EDirection, Position
from ks.commands import ChangeDirection, ActivateWallBreaker

# chillncode imports
from covid.covid import Covid_404

class AI(RealtimeAI):

    def __init__(self, world):
        super(AI, self).__init__(world)

    def initialize(self):
        global covid
        covid = Covid_404()
        covid.say_welcome()
        
        board = self.world.board
        agent = self.world.agents[self.my_side]
        
        covid.set_requirements(agent, board, self.my_side)
        covid.make_squares()
        covid.find_near_squares()
        covid.set_entry_positions()
        covid.find_next_square()
        covid.find_new_reaching_path()

    def decide(self):
        global covid
        board = self.world.board
        agent = self.world.agents[self.my_side]
        
        covid.set_requirements(agent, board, self.my_side)
        
        new_square = covid.is_new_square()
        if new_square == True:
            covid.update_curr_square_index()
            covid.find_next_square()
            covid.find_new_reaching_path()
        
        new_square_changed = covid.is_next_square_changed()
        if new_square_changed == True:
            covid.find_next_square()
            covid.find_new_reaching_path()
        
        wallbreaker_needed = covid.is_wallbreaker_needed()
        if wallbreaker_needed == True:
            self.send_command(ActivateWallBreaker())

        next_direction = covid.next_dir()
        self.send_command(ChangeDirection(next_direction))
            
