# from symtable import Symbol
from ecs.components.position import Position
from ecs.components.type import Type
from ecs.components.renderable import Renderable
import time

symbol={
    1:"~",
    0:".",
}

def render_map(world,terrain_layer,map_win):
    
    map_win.clear()
    map_win.border()
    for x in range(len(terrain_layer)):
        for y in range(len(terrain_layer[x])):
            map_win.addstr(x+1,y*3+1,symbol[terrain_layer[x][y]])

    for entity in world.get_entity_with(Position,Type):
        position=world.get_component(entity,Position)
        render_symbol=world.get_component(entity,Renderable)
        type=world.get_component(entity,Type)
        map_win.addstr(position.x+1,position.y*3+1,render_symbol.char)
        
    
    



    map_win.refresh()