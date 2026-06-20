from libtcodpy import CHAR_UMLAUT
import time
from interface.curse_render import render_sim
from simulation.update_all import update_all
from simulation.update_world.update_time import game_time
import logging

start=time.time()
def gameloop():
    global start
    current_time=time.time()
    if current_time- start>=1:
      update_all()
      start=time.time()

    render_sim()